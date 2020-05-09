import datetime as dt
from urllib.parse import urlencode
import requests
import pyshorteners
import requests_cache
import pandas as pd
import io
import sys
from contextlib import redirect_stdout


def download_data(apikey, api, parameters, cache_expire_after=3600):
    inputs_str = urlencode(parameters)
    url = api + 'apikey=' + apikey + '&' + inputs_str
    print("Getting the data...")
    requests_cache.install_cache(cache_name='kiwi_cache', backend='sqlite', expire_after=cache_expire_after)
    response = requests.get(url)

    if response.from_cache:
        print("Data loaded from cache")
        response_json = response.json()
    elif response.status_code == 200:
        print("Request was successful, data was downloaded from kiwi")
        response_json = response.json()
    else:
        print("Request was not successful")
        response_json = None

    # print("Printing response headers: ", response.headers)

    return response_json


class Flight:
    """
    TODO: Documentation
    """

    def __init__(self, flight_d):
        for key in flight_d:
            setattr(self, key, flight_d[key])


class Outbound:
    """
    TODO: Documentation
    """

    def __init__(self, flights_list):
        flight_list_outbound = list(filter(lambda d: d['return'] == 0, flights_list))

        self.flights = []

        for flight_d in flight_list_outbound:
            self.flights.append(Flight(flight_d))


class Inbound:
    """
    TODO: Documentation
    """

    def __init__(self, flights_list):
        flight_list_inbound = list(filter(lambda d: d['return'] == 1, flights_list))

        self.flights = []

        for flight_d in flight_list_inbound:
            self.flights.append(Flight(flight_d))


class Option:
    """
    TODO: Documentation
    """

    def __init__(self, option_d):
        #         TODO: use the first way only for first-level dictionary

        #         For all data on option level:
        #         for key in option_d:
        #             setattr(self, key, option_d[key])

        # For selection of data on option level:

        self.id = option_d['id']
        self.deep_link = option_d['deep_link']
        self.price = option_d['price']
        self.duration_total = option_d['duration']['total']
        self.duration_outbound = option_d['duration']['departure']
        self.duration_inbound = option_d['duration']['return']

        flights_list = option_d['route']

        self.outbound = Outbound(flights_list)
        self.inbound = Inbound(flights_list)


class ResponseData:
    """
    TODO: Documentation
    """

    def __init__(self, data):
        self.options = []

        for option_d in data:
            self.options.append(Option(option_d))


def to_hm(s):
    """
    Transform seconds to hours:mins
    """
    hours = int(s / 60 // 60)
    mins = int(s / 60 - hours * 60)
    return f'{hours}h{mins:02d}m'


def airline_name(airline_code):
    """
    Maps airline operator code to its name
    """
    try:
        df_operating_carriers = pd.read_csv('data/airlines.dat')  # https://github.com/jpatokal/openflights

        df_operating_carriers.columns = ['ind', 'full_name', 'full_name2', 'two_digit_code', 'three_digit_code',
                                         'name_in_capital', 'country', 'yesno']

        try:
            air_name = df_operating_carriers.loc[
                df_operating_carriers['two_digit_code'] == airline_code]['full_name'].unique()[0]
        except IndexError:
            try:
                air_name = df_operating_carriers.loc[df_operating_carriers['three_digit_code'] == airline_code][
                    'full_name'].unique()[0]
            except IndexError:
                air_name = airline_code

    except FileNotFoundError:
        print("Airline mapping table was not found")
        air_name = airline_code

    if air_name == '':
        air_name = airline_code

    return air_name


def print_n_options(flight_type, options, n, apikey):
    d = dict()
    for i in range(1, min(len(options), n + 1)):
        d[i] = dict()
        d[i]['option'] = i
        print('--OPTION ', i)
        d[i]['link'] = pyshorteners.Shortener().tinyurl.short(options[i].deep_link)
        print('link: ', d[i]['link'])
        d[i]['price'] = options[i].price
        print('price: ', d[i]['price'])
        d[i]['duration_total'] = to_hm(options[i].duration_total)
        print('total duration: ', d[i]['duration_total'])
        print('\n')

        if flight_type == 'round':

            for x, y, z in zip(['outbound', 'inbound'],
                               [options[i].duration_outbound, options[i].duration_inbound],
                               [options[i].outbound, options[i].inbound]
                               ):

                d[i][x] = dict()
                d[i][x]['duration'] = to_hm(y)
                print('{} (duration: {})'.format(x, d[i][x]))

                d[i][x]['lst_airlines'] = []
                for j in range(len(z.flights)):
                    a_n = airline_name(z.flights[j].airline)
                    d[i][x]['lst_airlines'].append(a_n) if a_n not in d[i][x]['lst_airlines'] else d[i][x][
                        'lst_airlines']

                print('airlines: ', d[i][x]['lst_airlines'])

                d[i][x]['from'] = z.flights[0].flyFrom
                print('from: ', d[i][x]['from'])

                d[i][x]['lst_stops'] = []
                for v in range(len(z.flights[:-1])):  # ignore first and last
                    d[i][x]['lst_stops'].append(
                        to_location_name(apikey,
                                         z.flights[v].flyTo
                                         )
                    )

                print('via {} stop(s): {}'.format(len(d[i][x]['lst_stops']), d[i][x]['lst_stops']))

                d[i][x]['to'] = z.flights[-1].flyTo
                print('to: ', d[i][x]['to'])

                d[i][x]['departure_time'] = \
                    dt.datetime.strftime(
                        dt.datetime.strptime(
                            z.flights[0].local_departure,  # first departure time
                            '%Y-%m-%dT%H:%M:%S.000Z'
                        ),
                        '%a %d-%b-%Y %H:%M')

                print('departure time: ', d[i][x]['departure_time'])

                d[i][x]['arrival_time'] = \
                    dt.datetime.strftime(
                        dt.datetime.strptime(
                            z.flights[-1].local_arrival,  # last arrival time
                            '%Y-%m-%dT%H:%M:%S.000Z'
                        ),
                        '%a %d-%b-%Y %H:%M')

                print('arrival time: ', d[i][x]['arrival_time'])

            print('\n')
            print('\n')

        elif flight_type == 'oneway':

            for x, y, z in zip(['outbound'],
                               [options[i].duration_outbound],
                               [options[i].outbound]
                               ):

                # TODO remove duplicated code
                d[i][x] = dict()
                d[i][x]['duration'] = to_hm(y)
                print('{} (duration: {})'.format(x, d[i][x]))

                d[i][x]['lst_airlines'] = []
                for j in range(len(z.flights)):
                    a_n = airline_name(z.flights[j].airline)
                    d[i][x]['lst_airlines'].append(a_n) if a_n not in d[i][x]['lst_airlines'] else d[i][x][
                        'lst_airlines']

                print('airlines: ', d[i][x]['lst_airlines'])

                d[i][x]['from'] = z.flights[0].flyFrom
                print('from: ', d[i][x]['from'])

                d[i][x]['lst_stops'] = []
                for v in range(len(z.flights[:-1])):  # ignore first and last
                    d[i][x]['lst_stops'].append(
                        to_location_name(apikey,
                                         z.flights[v].flyTo
                                         )
                    )

                print('via {} stop(s): {}'.format(len(d[i][x]['lst_stops']), d[i][x]['lst_stops']))

                d[i][x]['to'] = z.flights[-1].flyTo
                print('to: ', d[i][x]['to'])

                d[i][x]['departure_time'] = \
                    dt.datetime.strftime(
                        dt.datetime.strptime(
                            z.flights[0].local_departure,  # first departure time
                            '%Y-%m-%dT%H:%M:%S.000Z'
                        ),
                        '%a %d-%b-%Y %H:%M')

                print('departure time: ', d[i][x]['departure_time'])

                d[i][x]['arrival_time'] = \
                    dt.datetime.strftime(
                        dt.datetime.strptime(
                            z.flights[-1].local_arrival,  # last arrival time
                            '%Y-%m-%dT%H:%M:%S.000Z'
                        ),
                        '%a %d-%b-%Y %H:%M')

                print('arrival time: ', d[i][x]['arrival_time'])

            print('\n')
            print('\n')

        else:
            pass

    return d


def to_iata_code(apikey, location_name):
    # inputs_location = {
    # 'term': 'rhodes',
    # 'locale': 'en-US',
    # 'limit': 10,
    # 'active_only': 'true'
    # }

    inputs_location = dict()
    inputs_location['term'] = location_name

    response_json = download_data(apikey, api="https://kiwicom-prod.apigee.net/locations/query?",
                                  parameters=inputs_location, cache_expire_after=3600 * 24 * 7)

    if not response_json['locations']:
        print("No results found for this location")
        iata_code = None
    else:
        iata_code = response_json['locations'][0]['code']  # the first result
    return iata_code


def to_location_name(apikey, iata_code):
    inputs_location = dict()
    inputs_location['term'] = iata_code

    response_json = download_data(apikey, api="https://kiwicom-prod.apigee.net/locations/query?",
                                  parameters=inputs_location, cache_expire_after=3600 * 24 * 7)

    if not response_json['locations']:
        print("No results found for this location")
        location_name = None
    else:
        location_name = response_json['locations'][0]['city']['name']  # the first result

    return location_name


def transform_parameters(apikey, parameters):
    for k in ['fly_from', 'fly_to']:
        if k in parameters:
            parameters[k] = to_iata_code(apikey, parameters[k])

    for k in ['date_from', 'date_to', 'return_from', 'return_to']:
        if k in parameters:
            # print(parameters[k], type(parameters[k]))
            if isinstance(parameters[k], dt.datetime):
                try:

                    # parameters[k] = dt.datetime.strptime(
                    #     parameters[k], '%Y-%m-%d %H:%M:%S'
                    # ).strftime('%d/%m/%Y')

                    parameters[k] = parameters[k].strftime('%d/%m/%Y')

                except ValueError:
                    pass

    return parameters


def search(flight_type, apikey, parameters, n):
    parameters = transform_parameters(apikey, parameters)

    response_json = download_data(apikey, api="https://kiwicom-prod.apigee.net/v2/search?",
                                  parameters=parameters, cache_expire_after=3600)
    if response_json is not None:
        options = ResponseData(response_json['data']).options
        # save_stdout = sys.stdout
        # sys.stdout = io.BytesIO()
        first_n_options = print_n_options(flight_type, options, n, apikey)
        # TODO suppress print
        # sys.stdout = save_stdout
        # print("captured_stdout", sys.stdout)
    else:
        print("There is no response")
        first_n_options = None

    return first_n_options

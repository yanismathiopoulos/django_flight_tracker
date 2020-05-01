import datetime as dt
from urllib.parse import urlencode
import requests
import pyshorteners
import requests_cache
import pandas as pd


def download_data(apikey, parameters):
    inputs_str = urlencode(parameters)

    url = "https://kiwicom-prod.apigee.net/v2/search?" + \
          'apikey=' + apikey + '&' + inputs_str

    # TODO: Cache
    print("Getting the data...")
    requests_cache.install_cache(cache_name='kiwi_cache',
                                 backend='sqlite', expire_after=3600)
    response = requests.get(url)

    if response.from_cache:
        print("Data loaded from cache")
    else:
        print("Data downloaded from kiwi ", response)
    print('\n')

    response_json = response.json()

    # print("Printing response headers: ", response.headers)

    # print("Printing response_json['data'][0] for debug: ", response_json['data'][0])

    return response_json


class Flight:
    """
    TODO: Documentation
    """

    def __init__(self, flight_d):
        for key in flight_d:
            setattr(self, key, flight_d[key])

        #         self.local_departure += 'lol'


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
        #         TODO: use the first way only for firts-level dictionary

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
    hours = int(s / 60 // 60)
    mins = int(s / 60 - hours * 60)
    return f'{hours}h{mins:02d}m'


def airline_name(airline_code):
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


def print_n_options(options, n):
    d = dict()
    for i in range(1, min(len(options), n+1)):
        d[i] = dict()
        d[i]['option'] = i
        print('--OPTION ', i)
        d[i]['link'] = pyshorteners.Shortener().tinyurl.short(options[i].deep_link)
        print('link: ', d[i]['link'])
        d[i]['price'] = options[i].price
        print('price: ', d[i]['price'])
        d[i]['duration_total'] = to_hm(options[i].duration_total)
        print('total duration: ', d[i]['duration_total'])

        for x, y, z in zip(['outbound', 'inbound'],
                           [options[i].duration_outbound, options[i].duration_inbound],
                           [options[i].outbound, options[i].inbound]
                           ):

            print('\n')
            d[i][x] = dict()
            d[i][x]['duration'] = to_hm(y)
            print('{} (duration: {})'.format(x, d[i][x]))

            d[i][x]['lst_airlines'] = []
            for j in range(len(z.flights)):
                a_n = airline_name(z.flights[j].airline)
                d[i][x]['lst_airlines'].append(a_n) if a_n not in d[i][x]['lst_airlines'] else d[i][x]['lst_airlines']

            print('airlines: ', d[i][x]['lst_airlines'])

            d[i][x]['from'] = z.flights[0].flyFrom
            print('from: ', d[i][x]['from'])

            d[i][x]['lst_stops'] = []
            for v in range(len(z.flights[:-1])):  # ignore first and last
                d[i][x]['lst_stops'].append(z.flights[v].flyTo)

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

    return d


def search(apikey, parameters, n):
    response_json = download_data(apikey, parameters)
    options = ResponseData(response_json['data']).options
    first_n_options = print_n_options(options, n)

    return first_n_options


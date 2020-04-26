import datetime as dt
from urllib.parse import urlencode
import requests
import pyshorteners
import requests_cache


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

    print("Printing response headers: ", response.headers)

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


def print_n_options(options, n):
    with open('out.txt', 'w') as f:
        for i in range(1, n + 1):
            print('--OPTION ', i, file=f)
            print('link: ', pyshorteners.Shortener().tinyurl.short(options[i].deep_link), file=f)
            print('price: ', options[i].price, file=f)
            print('total duration: ', to_hm(options[i].duration_total), file=f)

            for x, y, z in zip(['outbound', 'inbound'],
                               [options[i].duration_outbound, options[i].duration_inbound],
                               [options[i].outbound, options[i].inbound]
                               ):
                print('\n', file=f)
                print('{} (duration: {})'.format(x, to_hm(y)), file=f)

                print('from: ', z.flights[0].flyFrom, file=f)

                #     print('via {} stop(s): {}'.format(
                #         1,
                #         options[0].outbound.flights[1,2,3,4]['flyTo']), file=f)

                print('to: ', z.flights[-1].flyTo, file=f)

                print('departure time: ',
                      dt.datetime.strftime(
                          dt.datetime.strptime(
                              z.flights[0].local_departure,  # first departure time
                              '%Y-%m-%dT%H:%M:%S.000Z'
                          ),
                          '%a %d-%b-%Y %H:%M'), file=f
                      )

                print('arrival time: ',
                      dt.datetime.strftime(
                          dt.datetime.strptime(
                              z.flights[-1].local_arrival,  # last arrival time
                              '%Y-%m-%dT%H:%M:%S.000Z'
                          ),
                          '%a %d-%b-%Y %H:%M'), file=f
                      )

            print('\n', file=f)
            print('\n', file=f)

    # with open('out.txt', 'r') as file:
    #     output = file.read().replace('\n', '')


def options_to_dict(options, n):
    d = dict()
    for i in range(1, n + 1):
        d[i] = dict()
        d[i]['option'] = i
        d[i]['link'] = pyshorteners.Shortener().tinyurl.short(options[i].deep_link)
        d[i]['price'] = options[i].price
        d[i]['duration_total'] = to_hm(options[i].duration_total)

        d[i]['duration_outbound'] = to_hm(options[i].duration_outbound)
        d[i]['outbound_from'] = options[i].outbound.flights[0].flyFrom
        d[i]['outbound_to'] = options[i].outbound.flights[-1].flyTo

        d[i]['outbound_departure_time'] = \
            dt.datetime.strftime(
                dt.datetime.strptime(
                    options[i].outbound.flights[0].local_departure,  # first departure time
                    '%Y-%m-%dT%H:%M:%S.000Z'
                ),
                '%a %d-%b-%Y %H:%M')

        d[i]['outbound_arrival_time'] = \
            dt.datetime.strftime(
                dt.datetime.strptime(
                    options[i].outbound.flights[-1].local_arrival,  # last arrival time
                    '%Y-%m-%dT%H:%M:%S.000Z'
                ),
                '%a %d-%b-%Y %H:%M')

        d[i]['duration_inbound'] = to_hm(options[i].duration_inbound)
        d[i]['inbound_from'] = options[i].inbound.flights[0].flyFrom
        d[i]['inbound_to'] = options[i].inbound.flights[-1].flyTo

        d[i]['inbound_departure_time'] = \
            dt.datetime.strftime(
                dt.datetime.strptime(
                    options[i].inbound.flights[0].local_departure,  # first departure time
                    '%Y-%m-%dT%H:%M:%S.000Z'
                ),
                '%a %d-%b-%Y %H:%M')

        d[i]['inbound_arrival_time'] = \
            dt.datetime.strftime(
                dt.datetime.strptime(
                    options[i].inbound.flights[-1].local_arrival,  # last arrival time
                    '%Y-%m-%dT%H:%M:%S.000Z'
                ),
                '%a %d-%b-%Y %H:%M')

    return d


def search(apikey, parameters, n):
    response_json = download_data(apikey, parameters)
    options = ResponseData(response_json['data']).options
    print_n_options(options, n)
    first_n_options = options_to_dict(options, n)

    return first_n_options


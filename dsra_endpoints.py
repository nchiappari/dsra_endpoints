#!/usr/bin/python

import json, string, random, datetime, re, urllib2, os
from geoip import geolite2

####################################################################################
### Flask Specific Code ############################################################
####################################################################################

# from flask import Flask
# from flask import request, jsonify
#
# app = Flask(__name__)
# port = 8080
#
# @app.route('/get_ip/')
# def get_ip_wrapper():
#     return jsonify(get_ip())
#
# def get_ip():
#     return {'ip': request.remote_addr}

# # takes 'ip_address' GET parameter - takes your ip if none provided
# @app.route('/get_location/')
# def get_location_wrapper():
#     ip_address = request.args.get('ip_address')
#     if ip_address is None:
#         ip_address = get_ip()['ip']
#     try:
#         return jsonify(get_location(ip_address))
#     except ValueError as e:
#         return jsonify({'error':e.message})
#
# @app.route('/time_elapsed_calculator/<start_year>/<start_month>/<start_day>/<end_year>/<end_month>/<end_day>/')
# def time_elapsed_calculator(start_year, start_month, start_day, end_year, end_month, end_day):
#     days = time_elapsed_calculator(int(start_year), int(start_month), int(start_day), int(end_year), int(end_month), int(end_day)).days
#     return jsonify({'days_elapsed':days})
#
# @app.route('/weekday_calculator/<year>/<month>/<day>/')
# def weekday_calculator_wrapper(year, month, day):
#     return jsonify({'date':'{}-{}-{}'.format(year, month, day),'weekday':weekday_calculator(year, month, day)})
#
# @app.route('/is_valid_email_address/<input>/')
# def is_valid_email_address_wrapper(input):
#     return jsonify(is_valid_email_address(input))
#
# @app.route('/temperature_converter/<value_to_convert>/<from_unit>/<to_unit>/')
# def temperature_converter_wrapper(value_to_convert, from_unit, to_unit):
#     try:
#         return jsonify(temperature_converter(value_to_convert, from_unit, to_unit))
#     except ValueError as e:
#         return jsonify({'error':e.message})
#
# @app.route('/mass_converter/<value_to_convert>/<from_unit>/<to_unit>/')
# def mass_converter_wrapper(value_to_convert, from_unit, to_unit):
#     try:
#         return jsonify(mass_converter(value_to_convert, from_unit, to_unit))
#     except ValueError as e:
#         return jsonify({'error':e.message})
#
# @app.route('/length_converter/<value_to_convert>/<from_unit>/<to_unit>/')
# def length_converter_wrapper(value_to_convert, from_unit, to_unit):
#     return jsonify(length_converter(value_to_convert, from_unit, to_unit))
#
# @app.route('/currency_converter/<value_to_convert>/<from_currency>/<to_currency>/')
# def currency_converter_wrapper(value_to_convert, from_currency, to_currency):
#     try:
#         converted_value = round(currency_converter(float(value_to_convert), from_currency, to_currency), 2)
#         return jsonify({'value_to_convert':value_to_convert, 'from_currency': from_currency, 'to_currency': to_currency, 'result':converted_value})
#     except ValueError as e:
#         return jsonify({'error':e.message})
#
# @app.route('/')
# def about():
#     return '<table border="1">\
#                 <tr>\
#                     <th>Endpoints</th><th>Description</th><th>Sample Output</th>\
#                 </tr>\
#                 <tr>\
#                     <td>/get_ip/</td><td>Returns your IP address.</td><td>{ip: "221.192.199.49"}</td>\
#                 </tr>\
#                 <tr>\
#                     <td>/get_location/</td><td>Returns your location. Specify an IP with the `ip_address` GET parameter.</td><td>{continent: "AS",country: "CN",ip: "221.192.199.49",location: [39.8897,115.275],subdivisions: ["13"],timezone: "Asia/Shanghai"}</td>\
#                 </tr>\
#                 <tr>\
#                     <td>/time_elapsed_calculator/&lsaquo;start_year&rsaquo;/&lsaquo;start_month&rsaquo;/&lsaquo;start_day&rsaquo;/&lsaquo;end_year&rsaquo;/&lsaquo;end_month&rsaquo;/&lsaquo;end_day&rsaquo;/</td><td>Calculate the number of days between two dates.</td><td>{days_elapsed: 365}</td>\
#                 </tr>\
#                 <tr>\
#                     <td>/is_valid_email_address/&lsaquo;input&rsaquo;/</td><td>Checks if provided email address is valid.</td><td>{email_address: "sample@mail.com",is_valid: true}</td>\
#                 </tr>\
#                 <tr>\
#                     <td>/currency_converter/&lsaquo;value_to_convert&rsaquo;/&lsaquo;from_currency&rsaquo;/&lsaquo;to_currency&rsaquo;/</td><td>Convert from one currency to another. The following currencies are allowed: "USD","AUD","BGN","BRL","CAD","CHF","CNY","CZK","DKK","GBP","HKD",<br>"HRK","HUF","IDR","ILS","INR","JPY","KRW","MXN","MYR","NOK","NZD",<br>"PHP","PLN","RON","RUB","SEK","SGD","THB","TRY","ZAR","EUR"</td><td>{from_currency: "USD",result: 10.62,to_currency: "EUR",value_to_convert: "12.53"}</td>\
#                 </tr>\
#                 <tr>\
#                     <td>/temperature_converter/&lsaquo;value_to_convert&rsaquo;/&lsaquo;from_unit&rsaquo;/&lsaquo;to_unit&rsaquo;/</td><td>Convert from one temperature unit to another. The following units are allowed: "fahrenheit","celcius","kelvin"</td><td>{from_unit: "celcius",result: 93.2,to_unit: "fahrenheit",value_to_convert: "34"}</td>\
#                 </tr>\
#                 <tr>\
#                     <td>/mass_converter/&lsaquo;value_to_convert&rsaquo;/&lsaquo;from_unit&rsaquo;/&lsaquo;to_unit&rsaquo;/</td><td>Convert from one mass unit to another. The following units are allowed: "microgram", "milligram", "gram", "kilogram", "metric_ton", "us_ton", "imperial_ton", "stone", "pound", "ounce"</td><td>{from_unit: "kilogram",result: 374.7858457142919,to_unit: "us_ton",value_to_convert: "340000"}</td>\
#                 </tr>\
#             </table>'


####################################################################################
### Lambda Specific Code ###########################################################
####################################################################################

# turns python objects into HTTP responses
def respond(res, err=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

# AWS lambda entry point and routing method
# takes JSON object with 'endpoint' and 'data' attributes
def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        endpoint = body['endpoint']
        data = body['data']

        if endpoint == "get_location":
            ip_address = data['ip_address']
            return respond(get_location(ip_address))
        elif endpoint == "time_elapsed_calculator":
            start_year = data['start_year']
            start_month = data['start_month']
            start_day = data['start_day']
            end_year = data['end_year']
            end_month = data['end_month']
            end_day = data['end_day']
            days = time_elapsed_calculator(int(start_year), int(start_month), int(start_day), int(end_year), int(end_month), int(end_day)).days
            return respond({'days_elapsed':days})
        elif endpoint == "weekday_calculator":
            year = int(data['year'])
            month = int(data['month'])
            day = int(data['day'])
            return respond({'date':'{}-{}-{}'.format(year, month, day),'weekday':weekday_calculator(year, month, day)})
        elif endpoint == "is_valid_email_address":
            input = data['input']
            return respond(is_valid_email_address(input))
        elif endpoint == "temperature_converter":
            value_to_convert = data['value_to_convert']
            from_unit = data['from_unit']
            to_unit = data['to_unit']
            return respond(temperature_converter(value_to_convert, from_unit, to_unit))
        elif endpoint == "mass_converter":
            value_to_convert = data['value_to_convert']
            from_unit = data['from_unit']
            to_unit = data['to_unit']
            return respond(mass_converter(value_to_convert, from_unit, to_unit))
        elif endpoint == "length_converter":
            value_to_convert = data['value_to_convert']
            from_unit = data['from_unit']
            to_unit = data['to_unit']
            return respond(length_converter(value_to_convert, from_unit, to_unit))
        elif endpoint == "currency_converter":
            value_to_convert = data['value_to_convert']
            from_currency = data['from_currency'].upper()
            to_currency = data['to_currency'].upper()
            converted_value = round(currency_converter(float(value_to_convert), from_currency, to_currency), 2)
            return respond({'value_to_convert':value_to_convert, 'from_currency': from_currency, 'to_currency': to_currency, 'result':converted_value})
        elif endpoint == "random_generator":
            output_type = data['output_type'].lower()
            if 'length' in data:
                length = int(data['length'])
                return respond(random_generator(output_type, length))
            return respond(random_generator(output_type))
        else:
            raise ValueError("{} is not a valid endpoint.".format(endpoint))
    except ValueError as e:
        return respond(None, e)
    except KeyError as e:
        return respond(None, ValueError("Please provide more data: {}".format(e)))

##########################################################################
##########################################################################

# returns location info from ip_address
def get_location(ip_address):
    match = geolite2.lookup(ip_address)
    if match:
        location_data = match.to_dict()
        location_data['subdivisions'] = list(location_data['subdivisions'])
        return location_data
    raise ValueError("No results found for {}".format(ip_address))

# returns timedelta object calculated from 2 provided dates
def time_elapsed_calculator(start_year, start_month, start_day, end_year, end_month, end_day):
    start = datetime.datetime(start_year, start_month, start_day)
    end = datetime.datetime(end_year, end_month, end_day)
    return end - start


days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
# returns what day of the week the specified date is
def weekday_calculator(year, month, day):
    return days_of_the_week[datetime.datetime(year, month, day).weekday()]

# checks if input is formatted like a valid email address
def is_valid_email_address(input):
    return {'email_address':input,'is_valid':re.match("^.+@.+\..+$", input) is not None}


to_celcius_map = {'fahrenheit': lambda F: (F - 32.0) / (9.0/5.0), 'kelvin': lambda K: K - 273.15, 'celcius': lambda C: C}
from_celcius_map = {'fahrenheit': lambda C: ((C * 9.0) / 5.0) + 32.0, 'kelvin': lambda C: C + 273.15, 'celcius': lambda C: C}
# converts from one temperature unit to another
# allowed units: fahrenheit, celcius, kelvin
def temperature_converter(value_to_convert, from_unit, to_unit):
    return unit_conversion(value_to_convert, from_unit, to_unit, to_celcius_map, from_celcius_map)


to_gram_map = {'microgram': lambda mg: mg / 1000000, 'milligram': lambda mg: mg / 1000, 'gram': lambda g: g, 'kilogram': lambda kg: kg * 1000, 'metric_ton': lambda mt: mt * 1000000
    ,'us_ton': lambda t: t * 907184.74, 'imperial_ton': lambda t: t * 1016046.91, 'stone': lambda s: s / 0.00015747304441777, 'pound': lambda p: p * 453.59237, 'ounce': lambda o: o * 28.34952}
from_gram_map = {'microgram': lambda mg: mg * 1000000, 'milligram': lambda mg: mg * 1000, 'gram': lambda g: g, 'kilogram': lambda kg: kg / 1000, 'metric_ton': lambda mt: mt / 1000000
    ,'us_ton': lambda t: t / 907184.74, 'imperial_ton': lambda t: t / 1016046.91, 'stone': lambda s: s * 0.00015747304441777, 'pound': lambda p: p / 453.59237, 'ounce': lambda o: o / 28.34952}
# converts from one mass unit to another
# allowed units: microgram, milligram, gram, kilogram, metric_ton, us_ton, imperial_ton, stone, pound, ounce
def mass_converter(value_to_convert, from_unit, to_unit):
    return unit_conversion(value_to_convert, from_unit, to_unit, to_gram_map, from_gram_map)


valid_currencies = ["USD","AUD","BGN","BRL","CAD","CHF","CNY","CZK","DKK","GBP","HKD","HRK","HUF","IDR","ILS","INR","JPY","KRW","MXN","MYR","NOK","NZD","PHP","PLN","RON","RUB","SEK","SGD","THB","TRY","ZAR","EUR"]
# converts from one currency to another
# allowed currencies: "USD","AUD","BGN","BRL","CAD","CHF","CNY","CZK","DKK","GBP","HKD","HRK","HUF","IDR","ILS","INR","JPY","KRW","MXN","MYR","NOK","NZD","PHP","PLN","RON","RUB","SEK","SGD","THB","TRY","ZAR","EUR"
def currency_converter(value_to_convert, from_currency, to_currency):
    if from_currency not in valid_currencies or to_currency not in valid_currencies:
        raise ValueError("Please provide valid currencies.")
    url = "http://api.fixer.io/latest?base={}".format(from_currency)
    data = json.load(urllib2.urlopen(url))
    return value_to_convert * data['rates'][to_currency]


convert_to_meter = {'mm': lambda mm: mm / 1000, 'cm': lambda cm: cm / 100, 'm': lambda m: m, 'km': lambda km: km * 1000
    , 'inch': lambda inch: (inch / 12) * 0.3048, 'ft': lambda ft: ft * 0.3048, 'yd': lambda yd: (yd * 3) * 0.3048, 'mi': lambda mi: (mi * 5280) * 0.3048}
convert_from_meter = {'mm':lambda m: m * 1000, 'cm': lambda m: m * 100, 'm': lambda m: m, 'km': lambda m: m / 1000
    , 'inch': lambda inch: (inch / 0.3048) * 12, 'ft': lambda ft: ft / 0.3048, 'yd': lambda yd: (yd / 0.3048) / 3, 'mi': lambda mi: (mi / 0.3048) / 5280}
# converts from one length unit to another
# allowed units: mm, cm, m, km, inch, ft, yd, mi
def length_converter(value_to_convert, from_unit, to_unit):
    return unit_conversion(value_to_convert, from_unit, to_unit, convert_to_meter, convert_from_meter)


letters = string.ascii_letters
digits = string.digits
letters_and_digits = letters + digits
symbols = "~*!<&_-@;+.%$?" + letters_and_digits

# generates random content - default length = 10
# options: alphanumeric, symbol, text, number
def random_generator(output_type, length=10):
    if output_type == "alphanumeric":
        return generate_random_content(length, letters_and_digits)
    elif output_type == "symbol":
        return generate_random_content(length, symbols)
    elif output_type == "text":
        return generate_random_content(length, letters)
    elif output_type == "number":
        return generate_random_content(length, digits)
    else:
        raise ValueError("ERROR: \"{}\" is not a recognized type.".format(output_type))

# random_generator helper method
def generate_random_content(length, character_options):
    result = ""
    for i in range(0, length):
        result += random.choice(character_options)
    return result


##########################################################################
##########################################################################

# generic method for unit conversion
def unit_conversion(value_to_convert, from_unit, to_unit, to_base_unit_map, from_base_unit_map):
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    try:
        if from_unit == to_unit:
            return {'from_unit':from_unit,'to_unit':to_unit,'value_to_convert':value_to_convert,'result':float(value_to_convert)}
        value_in_base_unit = to_base_unit_map[from_unit](float(value_to_convert))
        result = from_base_unit_map[to_unit](float(value_in_base_unit))
        return {'from_unit':from_unit,'to_unit':to_unit,'value_to_convert':value_to_convert,'result':result}
    except KeyError as e:
        raise ValueError("ERROR: {} is not a valid unit.".format(e))

##########################################################################
##########################################################################

# START FLASK APP
# if __name__ == '__main__':
#     app.run(host='0.0.0.0',port=port,threaded=True)

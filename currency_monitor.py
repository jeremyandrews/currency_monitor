from ConfigParser import SafeConfigParser
import os
import urllib
import json
import sys

parser = SafeConfigParser()
# @todo: pretty error if no configuration file exists.
parser.read(['currency_monitor.cfg', os.path.expanduser('~/.currency_monitor.cfg')])
app_id = parser.get('openexchangerates', 'app_id')
if (parser.has_option('openexchangerates', 'currency_from')):
	currency_from = parser.get('openexchangerates', 'currency_from')
else:
	# Default currency provided by Open Exhange Rates is USD.
	currency_from = 'USD'

if (parser.has_option('openexchangerates', 'currency_to')):
	currency_to = parser.get('openexchangerates', 'currency_to')
else:
	# By default we'll convert to euros.
	currency_to= 'EUR'

currencyURL = "http://openexchangerates.org/api/currencies.json"
currency = urllib.urlopen(currencyURL)
currencies = currency.read()
currency.close()
fullNames = json.loads(currencies)

conversionURL = "https://openexchangerates.org/api/latest.json?app_id=" + app_id + "&base=" + currency_from
#print conversionURL
conversion = urllib.urlopen(conversionURL)
conversions = conversion.read()
conversion.close()
value = json.loads(conversions)

# @todo: improve error handling.
if (value['timestamp']):
	# SUCCESS
	# {u'timestamp': 1404878444, u'base': u'USD', u'rates': {u'DZD': 79.34277, u'NAD': 10.69646, u'GHS': 3.306963, u'EGP': 7.150547, u'BGN': 1.438379, u'PAB': 1, u'BOB': 6.901406, u'DKK': 5.477647, u'BWP': 8.841668, u'LBP': 1512.265, u'TZS': 1665.906667, u'VND': 21255.85, u'AOA': 97.492201, u'KHR': 4037.509967, u'MYR': 3.17505, u'KYD': 0.826218, u'LYD': 1.217933, u'UAH': 11.67394, u'JOD': 0.708706, u'AWG': 1.79, u'SAR': 3.750292, u'LTL': 2.536891, u'HKD': 7.749992, u'CHF': 0.893149, u'GIP': 0.58373, u'BYR': 10259.7, u'ALL': 102.9888, u'MRO': 291.45862, u'HRK': 5.58409, u'DJF': 178.659, u'SZL': 10.6999, u'THB': 32.35822, u'XAF': 482.251558, u'BND': 1.242448, u'ISK': 113.972, u'UYU': 22.98731, u'NIO': 25.9687, u'LAK': 8041.558333, u'SYP': 149.813332, u'MAD': 8.240034, u'MZN': 31.085, u'PHP': 43.38084, u'ZAR': 10.69324, u'NPR': 95.782259, u'ZWL': 322.355006, u'NGN': 162.4173, u'CRC': 539.422498, u'AED': 3.672803, u'EEK': 11.67285, u'MWK': 395.0696, u'LKR': 130.256899, u'PKR': 98.773649, u'HUF': 227.154899, u'BMD': 1, u'LSL': 10.69806, u'MNT': 1828.333333, u'AMD': 411.444998, u'UGX': 2642.448333, u'QAR': 3.640686, u'XDR': 0.647459, u'JMD': 112.109899, u'GEL': 1.76668, u'SHP': 0.58373, u'AFN': 58.008075, u'SBD': 7.2205, u'KPW': 900, u'TRY': 2.125263, u'BDT': 77.52332, u'YER': 214.9812, u'HTG': 44.5587, u'XOF': 482.651599, u'MGA': 2455.513333, u'ANG': 1.789, u'LRD': 90.4624, u'RWF': 677.67872, u'NOK': 6.184038, u'MOP': 7.975136, u'INR': 59.81701, u'MXN': 12.99247, u'CZK': 20.16312, u'TJS': 4.94725, u'BTC': 0.001610935, u'BTN': 59.81235, u'COP': 1853.723333, u'TMT': 2.8501, u'MUR': 30.30629, u'IDR': 11668.183333, u'HNL': 20.94614, u'XPF': 87.669449, u'FJD': 1.826409, u'ETB': 19.67856, u'PEN': 2.774609, u'BZD': 1.992562, u'ILS': 3.436953, u'DOP': 43.33512, u'GGP': 0.58373, u'MDL': 13.94616, u'BSD': 1, u'SEK': 6.832161, u'ZMK': 5252.024745, u'JEP': 0.58373, u'AUD': 1.064426, u'SRD': 3.308567, u'CUP': 0.998948, u'CLF': 0.023, u'BBD': 2, u'KMF': 361.483916, u'KRW': 1012.088325, u'GMD': 39.80439, u'VEF': 6.292751, u'IMP': 0.58373, u'CLP': 552.985, u'ZMW': 6.178178, u'EUR': 0.734568, u'CDF': 922.227, u'XCD': 2.70154, u'KZT': 183.3772, u'RUB': 34.25533, u'XAG': 0.04758306, u'TTD': 6.339383, u'OMR': 0.38497, u'BRL': 2.214332, u'MMK': 971.9999, u'PLN': 3.033139, u'PYG': 4255.278333, u'KES': 87.83927, u'SVC': 8.738283, u'MKD': 45.35261, u'GBP': 0.58373, u'AZN': 0.784033, u'TOP': 1.842632, u'MVR': 15.36253, u'VUV': 94.317501, u'GNF': 7035.305, u'WST': 2.293502, u'IQD': 1177.746733, u'ERN': 15.0624, u'BAM': 1.437724, u'SCR': 12.2972, u'CAD': 1.068138, u'CVE': 80.670861, u'KWD': 0.282018, u'BIF': 1548.325, u'PGK': 2.440521, u'SOS': 899.577025, u'TWD': 29.89019, u'SGD': 1.243351, u'UZS': 2312.619977, u'STD': 18020.65, u'IRR': 25737.333333, u'CNY': 6.192162, u'SLL': 4363, u'TND': 1.69133, u'GYD': 204.518749, u'MTL': 0.683602, u'NZD': 1.138138, u'FKP': 0.58373, u'LVL': 0.51587, u'USD': 1, u'KGS': 52.123875, u'ARS': 8.140804, u'RON': 3.223676, u'GTQ': 7.746895, u'RSD': 85.30666, u'BHD': 0.377002, u'JPY': 101.6395, u'SDG': 5.69271, u'XAU': 0.00075653}, u'license': u'Data sourced from various providers with public-facing APIs; copyright may apply; resale is prohibited; no warranties given of any kind. Bitcoin data provided by http://coindesk.com. All usage is subject to your acceptance of the License Agreement available at: https://openexchangerates.org/license/', u'disclaimer': u'Exchange rates are provided for informational purposes only, and do not constitute financial advice of any kind. Although every attempt is made to ensure quality, NO guarantees are given whatsoever of accuracy, validity, availability, or fitness for any purpose - please use at your own risk. All usage is subject to your acceptance of the Terms and Conditions of Service, available at: https://openexchangerates.org/terms/'}
	print "1 " + fullNames[currency_from] + " = " + str(value['rates'][currency_to]) + " " + fullNames[currency_to] + "s"
elif (value['error']):
	# ERROR
	# {u'status': 403, u'message': u'not_allowed', u'description': u'Changing `base` currency is only available for Enterprise and Unlimited clients - please upgrade, or contact support@openexchangerates.org with any questions. Thanks!', u'error': True}
	print value['description']
	sys.exit(-1)

#value = dict()
#value['disclaimer'] = "Exchange rates are provided for informational purposes only, and do not constitute financial advice of any kind. Although every attempt is made to ensure quality, NO guarantees are given whatsoever of accuracy, validity, availability, or fitness for any purpose - please use at your own risk. All usage is subject to your acceptance of the Terms and Conditions of Service, available at: https://openexchangerates.org/terms/"
#value['license'] = "Data sourced from various providers with public-facing APIs; copyright may apply; resale is prohibited; no warranties given of any kind. Bitcoin data provided by http://coindesk.com. All usage is subject to your acceptance of the License Agreement available at: https://openexchangerates.org/license/"
#value['timestamp'] = 1404349247
#value['base'] = currency_from
#value['rates'] = dict()
#value['rates']['BTC'] = .0015572593
#value['rates']['CAD'] = 1.066272
#value['rates']['EUR'] = 0.732336
# @todo: handle plurals when value['rates'][currency_to] != 1
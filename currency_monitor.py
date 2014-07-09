from ConfigParser import SafeConfigParser
import os
import urllib
import json

parser = SafeConfigParser()
# @todo: pretty error if no configuration file exists.
parser.read(['currency_monitor.cfg', os.path.expanduser('~/.currency_monitor.cfg')])
app_id = parser.get('openexchangerates', 'app_id')
currency_from = parser.get('openexchangerates', 'currency_from')
currency_to = parser.get('openexchangerates', 'currency_to')

currencyURL = "http://openexchangerates.org/api/currencies.json"
currency = urllib.urlopen(currencyURL)
currencies = currency.read()
currency.close()
fullNames = json.loads(currencies)
#print fullNames[currency_to]

conversionURL = "https://openexchangerates.org/api/latest.json?app_id=" + app_id
conversion = urllib.urlopen(conversionURL)
conversions = conversion.read()
conversion.close()
value = json.loads(conversions)

#value = dict()
#value['disclaimer'] = "Exchange rates are provided for informational purposes only, and do not constitute financial advice of any kind. Although every attempt is made to ensure quality, NO guarantees are given whatsoever of accuracy, validity, availability, or fitness for any purpose - please use at your own risk. All usage is subject to your acceptance of the Terms and Conditions of Service, available at: https://openexchangerates.org/terms/"
#value['license'] = "Data sourced from various providers with public-facing APIs; copyright may apply; resale is prohibited; no warranties given of any kind. Bitcoin data provided by http://coindesk.com. All usage is subject to your acceptance of the License Agreement available at: https://openexchangerates.org/license/"
#value['timestamp'] = 1404349247
#value['base'] = currency_from
#value['rates'] = dict()
#value['rates']['BTC'] = .0015572593
#value['rates']['CAD'] = 1.066272
#value['rates']['EUR'] = 0.732336
print value['rates'][currency_to]

#url = "http://currency-api.appspot.com/api/USD/EUR.json?key=abc"
#url = urllib.urlopen(url)
#result = url.read()
#url.close()
#result = json.loads(result)
#
#if result.success:
#    print "1 USD is worth %.2f EUR" % (result.rate)

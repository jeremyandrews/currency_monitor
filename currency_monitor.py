from ConfigParser import SafeConfigParser
import os
import urllib
import json
import sys
import sqlite3

def readConfiguration():
	config = dict()
	parser = SafeConfigParser()
	# @todo: pretty error if no configuration file exists.
	parser.read(['currency_monitor.cfg', os.path.expanduser('~/.currency_monitor.cfg')])
	config['app_id'] = parser.get('openexchangerates', 'app_id')
	if (parser.has_option('openexchangerates', 'currency_from')):
		config['currency_from'] = parser.get('openexchangerates', 'currency_from')
	else:
		# Default currency provided by Open Exhange Rates is USD.
		config['currency_from'] = 'USD'
	# @tado: track conversion to multiple currencies
	if (parser.has_option('openexchangerates', 'currency_to')):
		config['currency_to'] = parser.get('openexchangerates', 'currency_to')
	else:
		# By default we'll convert to euros.
		config['currency_to']= 'EUR'
	return config

def prepDatabase(config):
	db = dict()
	db['connection'] = sqlite3.connect('currency.db')
	db['connection'].execute("""CREATE TABLE IF NOT EXISTS history(
	  timestamp NUMERIC,
	  currency_from TEXT,
	  currency_to TEXT,
	  value REAL,
	  PRIMARY KEY(timestamp, currency_from, currency_to))""")
	db['cursor'] = db['connection'].cursor()
	return db

def closeDatabase(config, db):
	db['cursor'].close()
	db['connection'].close()

# Download current list of all currencies, used to convert abbreviation to full name.
def getCurrencyList(config):
	currencyURL = "http://openexchangerates.org/api/currencies.json"
	currency = urllib.urlopen(currencyURL)
	currencies = currency.read()
	currency.close()
	return json.loads(currencies)

# Download all current currency conversion values.
def getCurrencyValue(config):
	conversionURL = "https://openexchangerates.org/api/latest.json?app_id=" + config['app_id'] + "&base=" + config['currency_from']
	#print conversionURL
	#conversion = urllib.urlopen(conversionURL)
	#conversions = conversion.read()
	#conversion.close()
	#value = json.loads(conversions)

	### temporary data for testing
	value = dict()
	value['timestamp'] = 1405789261
	value['rates'] = dict()
	value['rates']['EUR'] = 0.739362
	return value

def getLastTimestamp(config, db):
	db['cursor'].execute("""SELECT MAX(timestamp) FROM history WHERE currency_from = :from and currency_to = :to""", {"from": config['currency_from'], "to": config['currency_to']})
	db['connection'].commit()
	row = db['cursor'].fetchone()
	return row[0]

# Parse the response from OpenExchangeRates.org.
# @todo: improve error handling.
def parseCurrencyValue(config, db, currencyValue):
	if (currencyValue['timestamp']):
		# SUCCESS: sample reply
		#          {u'timestamp': 1404878444, u'base': u'USD', u'rates': 
		#            {u'DZD': 79.34277, u'NAD': 10.69646, u'GHS': 3.306963, u'EGP': 7.150547,
		#             u'BGN': 1.438379, u'PAB': 1, u'BOB': 6.901406, u'DKK': 5.477647, u'BWP': 8.841668,
        #              ...
		#            u'JPY': 101.6395, u'SDG': 5.69271, u'XAU': 0.00075653},
		#           u'license': u'Data sourced from various providers with public-facing APIs; copyright may apply; resale is prohibited; no warranties given of any kind. Bitcoin data provided by http://coindesk.com. All usage is subject to your acceptance of the License Agreement available at: https://openexchangerates.org/license/', u'disclaimer': u'Exchange rates are provided for informational purposes only, and do not constitute financial advice of any kind. Although every attempt is made to ensure quality, NO guarantees are given whatsoever of accuracy, validity, availability, or fitness for any purpose - please use at your own risk. All usage is subject to your acceptance of the Terms and Conditions of Service, available at: https://openexchangerates.org/terms/'}
		#print "1 " + fullNames[currency_from] + " = " + str(value['rates'][currency_to]) + " " + fullNames[currency_to] + "s"
		db['cursor'].execute("""INSERT INTO history (timestamp, currency_from, currency_to, value) VALUES (?, ?, ?, ?);""", (currencyValue['timestamp'], config['currency_from'], config['currency_to'], currencyValue['rates'][config['currency_to']]))
		db['connection'].commit()
	elif (currencyValue['error']):
		# ERROR: sample reply
		#        {u'status': 403, u'message': u'not_allowed', u'description':
		#         u'Changing `base` currency is only available for Enterprise and Unlimited clients - please upgrade, or contact support@openexchangerates.org with any questions. Thanks!',
		#         u'error': True}
		print currencyValue['description']
		sys.exit(-1)

### MAIN

config = readConfiguration()
db = prepDatabase(config)
currencyList = getCurrencyList(config)
lastTimestamp = getLastTimestamp(config, db)
currencyValue = getCurrencyValue(config)
parseCurrencyValue(config, db, currencyValue)
closeDatabase(config, db)

print currencyValue

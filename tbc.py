#!/usr/bin/python3
from urllib import request
from bs4 import BeautifulSoup
import dateutil.parser
from datetime import datetime


request_params = {
	'base_url': 'http://data.bordeaux-metropole.fr/wps',
	'key': 'E91VUSAEIV',
	'service': 'WPS',
	'version': '1.0.0',
	'request': 'Execute',
	'identifier': 'saeiv_arret_passages',
	'data_input': 'GID=3382',
	'underscore': '1453728003441'
}

# Quai de Brienne en face: 1453467565258

url = "{}?key={}&service={}&version={}&request={}&Identifier={}&DataInputs={}&_={}".format(
	request_params['base_url'], 
	request_params['key'],
	request_params['service'],
	request_params['version'],
	request_params['request'],
	request_params['identifier'],
	request_params['data_input'],
	request_params['underscore']
	)


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class BusStop:
	def __init__(self, soup, line_number, location, color_provider):
		self.line_number = line_number
		self.location = location
		self.set_next_bus_stops(soup)
		self.color_provider = color_provider

	def set_next_bus_stops(self, soup):
		sv_arret_ps = soup.findAll('SV_ARRET_P')
		self.next_bus_stops = []

		for sv_arret_p in sv_arret_ps:
			libelle = sv_arret_p.find('LIBELLE').text
			for line_type in ['Lianes ','Ligne ']:
				if line_type in libelle:
					line_number = int(libelle.strip(line_type))
					if line_number == self.line_number:
						self.next_bus_stops.append({ 
							'stop_time_real': ((dateutil.parser.parse(sv_arret_p.find('HOR_REAL').text) - datetime.now()).seconds)//60,
							'stop_time_app': ((dateutil.parser.parse(sv_arret_p.find('HOR_APP').text) - datetime.now()).seconds)//60,
							'stop_time_theo': ((dateutil.parser.parse(sv_arret_p.find('HOR_THEO').text) - datetime.now()).seconds)//60,
							'terminus': sv_arret_p.find('TERMINUS').text
							})

	def print_next_stops(self):
		if self.next_bus_stops:
			for next_bus_stop in self.next_bus_stops:
				to_print = '[ '+self.color_provider.OKGREEN+self.color_provider.BOLD+'{}'.format(self.line_number)+self.color_provider.ENDC+' ]'+self.color_provider.ENDC
				to_print += self.color_provider.OKBLUE+' Prochain passage dans '+self.color_provider.ENDC
				to_print += self.color_provider.OKGREEN+self.color_provider.BOLD+'{}'.format(next_bus_stop['stop_time_real'])+self.color_provider.ENDC
				to_print += self.color_provider.OKBLUE+' min (théorique : '+self.color_provider.ENDC
				to_print += self.color_provider.OKGREEN+self.color_provider.BOLD+'{}'.format(next_bus_stop['stop_time_theo'])+self.color_provider.ENDC
				#to_print += self.color_provider.OKBLUE+' min, app : '+self.color_provider.ENDC
				#to_print += self.color_provider.OKGREEN+self.color_provider.BOLD+'{}'.format(next_bus_stop['stop_time_app'])+self.color_provider.ENDC
				#to_print += self.color_provider.OKBLUE+' min) à '+self.color_provider.ENDC
				#to_print += self.color_provider.OKGREEN+self.color_provider.BOLD+'{}'.format(self.location)+self.color_provider.ENDC
				#to_print += self.color_provider.OKBLUE+', terminus : '+self.color_provider.ENDC
				#to_print += self.color_provider.OKGREEN+self.color_provider.BOLD+'{}'.format(next_bus_stop['terminus'])+self.color_provider.ENDC
				print(to_print)
		else:
			to_print = 'No next bus stop time avalaible...'
			print(to_print)


response = request.urlopen(url)
soup = BeautifulSoup(response, 'xml')

bus_stop = BusStop(
	soup = soup,
	line_number = 11,
	location = 'Quai de Brienne',
	color_provider = BColors()
	)

bus_stop.print_next_stops()

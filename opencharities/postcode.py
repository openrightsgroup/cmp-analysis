
import re
import csv
import sys
import json
import time
import shelve
import logging
import requests

# A normal postcode regex.  Copes with:
# A1 1AA
# AA1 1AA
# A11 1AA
# AA11 1AA
# AA1A 1AA (London)
postcode = re.compile(r'[A-Z]{1,2}\d{1,2}[A-Z]? ?\d[A-Z]{2}')

PCDATA = shelve.open('pcdata')

logging.basicConfig(level=logging.DEBUG)

def getitem(data, key):
	return data.get('administrative', {}).get(key, {}).get('title','')

"""This script expects a single parameter - the name of the source list file.

The source list file is expected to have three columns - title, address and URL

The merged output is written in TSV format to stdout.
"""

# open input file and set up CSV parser
with open(sys.argv[1]) as fp:
	reader = csv.reader(fp, delimiter='\t')

	# create CSV output encoder
	writer = csv.writer(sys.stdout, delimiter='\t')

	# write column titles
	writer.writerow(['Title','Address','URL','County','Constituency','Council'])

	# for each source row
	for n,row in enumerate(reader):
		addr = row[1]
		logging.info("Checking: [%d] %s", n, row[0])
		# check address against postcode regex
		match = postcode.search(addr)
		if match:
			logging.debug("Found postcode: %s", match.group())
			# we use a normalized version of the postcode from now on. 
			# no spaces, uppercase
			pc = match.group().replace(' ','').upper()
			# cache based on the postcode sector (EC1A 2ZZ -> EC1A2)
			# the information we're getting is unlikely to vary inside a sector, and it sames API lookups
			if not pc[:-2] in PCDATA:
				logging.debug("Getting data: %s", pc)
				req = requests.get('http://uk-postcodes.com/postcode/' + pc.upper() + '.json')
				# there's no error handling for these lookups.  On this list we got away with it!
				data = req.json()
				PCDATA[ pc[:-2] ] = data
				# throttle API usage to 5 reqs a second.  Seems sufficiently polite
				time.sleep(0.2)
			else:
				logging.debug("Cache Hit")
				data = PCDATA[ pc[:-2] ]

			
			# write out the original row with the three additional lookup fields.
			writer.writerow( row + [ 
				getitem(data, 'county'), 
				getitem(data, 'constituency'),
				getitem(data, 'council')
				])
		else:
			# if we can't parse a postcode, log a warning
			logging.warn("No match: %s", addr)
			# output original row unchanged
			writer.writerow(row)


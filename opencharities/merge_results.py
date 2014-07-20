
# OK, this script is expensive! Also the coreutils join command is a pain when
# you're using tab separators

import subprocess
import csv
import sys

GEO = {}
TEST = {}

if len(sys.argv) < 3:
	print >>sys.stderr, """
	Requires two parameters: <test results TSV> <geo results TSV>
	"""
	sys.exit(1)

with open(sys.argv[1]) as fp:
	# test summary file
	reader = csv.reader(fp, delimiter='\t')
	TEST = {row[0]: row[1:] for row in reader }

with open(sys.argv[2]) as fp2:
	reader = csv.reader(fp2, delimiter='\t')
	GEO = {row[2]: row for row in reader if len(row) >= 3 }

# in-memory merge.

urls = set(TEST.keys() + GEO.keys())

writer = csv.writer(sys.stdout,delimiter='\t')
for url in sorted(urls):
	writer.writerow([url] + GEO.get(url, ['']*6) + TEST.get(url, [''] * 8) )
	
	
		



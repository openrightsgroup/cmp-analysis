# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 20:53:00 2014

@author: mrowe
"""

import csv
import tldextract
from Record import Record


# Create a list of filter records
recordList = []

# Get the export file and read it in as a map between URL and probe tests
print 'Reading in export from the file'
count = 0
with open('../data/export.csv', 'rb') as csvfile:
    # tokenise the line by comma delimiter
    csvReader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvReader:        
        # Create a data object and output it
        record = Record(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
        recordList.append(record)
#        print row[0]
#        print record
        
        # Output the count so far
        count += 1
        print count
 
        # Insert a temporary break to test for this       
        if(count > 10000):
            break
        
# Parse the domains and get the blocks per domain
domainsToBlocksDict = {}
for record in recordList:
    # check to see if the record is a block
    if(record.status == "blocked"):
        # get the domain of the record
        domain = tldextract.extract(record.url)
        domain = domain.domain
        
        # check to see if the dictionary contains the key
        if domain in domainsToBlocksDict:
            domainsToBlocksDict[domain] += 1
        else:
            domainsToBlocksDict[domain] = 1
            
# Write the dictionary to a local file for R to plot
file = open("../data/domainToBlockCount.tsv","w")
file.write("Domain\tBlock.Count\n")
for domain in domainsToBlocksDict:
    file.write(domain + "\t" + str(domainsToBlocksDict[domain]) + "\n")
file.close()

        
        


        
    



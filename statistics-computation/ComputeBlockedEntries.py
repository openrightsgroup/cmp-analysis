# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 20:53:00 2014
@author: mattroweshow
"""
import csv
import tldextract
from Record import Record

# Removes duplicate records from the export file
def cleanExport() :
    dumpExport = "../data/export.csv"
    cleanedExport = "../data/export_cleaned.csv"
    print 'Removing duplicate lines from the export'
    lines_seen = set() # holds lines already seen
    outfile = open(cleanedExport, "w")
    for line in open(dumpExport, "r"):
        if line not in lines_seen: # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()

    # This is to check that the analysis actually reveals a reduction
    print 'Counting file lengths'
    dumpLineCount = float(sum(1 for line in open(dumpExport)))
    print dumpLineCount
    cleanLineCount = float(sum(1 for line in open(cleanedExport)))
    print cleanLineCount

# Parse the export file to get: (i) the blocks per domain, store this within a dictionary (ii) the blocks per isp filter
def computeBlockedEntries() :
    cleanedExport = "../data/export_cleaned.csv"
    domainsToBlocksDict = {}
    filtersToDomainBlocksDict = {}

    # Get the export file and read it in as a map between URL and probe tests
    print 'Reading in export from the file'
    count = float(1)
    with open(cleanedExport, 'rb') as csvfile:

        # tokenise the line by comma delimiter
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvReader:
            # Create a data object and output it
            # url, submissionTimestamp, networkName, filterLevel, status, resultTimestamp, httpStatus, probeConfig
            record = Record(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            if(record.status == "blocked"):
    #            recordList.append(record)

                # get the filter of the block
                ispFilter = record.networkName

                # get the domain of the record
                domain = tldextract.extract(record.url)
                domain = domain.domain

                # check to see if the dictionary contains the key
                if domain in domainsToBlocksDict:
                    domainsToBlocksDict[domain] += 1
                else:
                    domainsToBlocksDict[domain] = 1

                # check to see if the dictionary contains a mapping between the ispFilter and the domains to block count dictionary
                if ispFilter in filtersToDomainBlocksDict:
                    innerDict = filtersToDomainBlocksDict[ispFilter]
                    # check to see if the per ispfilter block dictionary contains the domain key
                    if domain in innerDict:
                        innerDict[domain] += 1
                    else:
                        innerDict[domain] = 1

                    # map the innerDictinary back into the ispFilter to blocked domains dictionary
                    filtersToDomainBlocksDict[ispFilter] = innerDict

                    # otherwise generate a new inner dictionary
                else:
                    innerDict = {}
                    innerDict[domain] = 1
                    filtersToDomainBlocksDict[ispFilter] = innerDict

                print count

                # Output the count so far
                count += 1

    # Write the results to file
    writeBlockCounts(domainsToBlocksDict)
    writePerFilterBlockCounts(filtersToDomainBlocksDict)



# Writes the domain block frequency distribution to a file
def writeBlockCounts(domainsToBlocksDict) :
    # Write the dictionary to a local file for R to plot
    file = open("../data/domainToBlockCount.tsv","w")
    file.write("Domain\tBlock.Count\n")
    for domain in domainsToBlocksDict:
        try:
            file.write(domain + "\t" + str(domainsToBlocksDict[domain]) + "\n")
        except UnicodeEncodeError:
            print "UnicodeEncodeError"

    file.close()

# Writes the per-isp filter domain block frequency distribution to a per-ISP files
def writePerFilterBlockCounts(filtersToDomainBlocksDict) :
    # For each ispfilter, write out the dictionary mapping the domains to their counts
    for ispFilter in  filtersToDomainBlocksDict:
        file = open("../data/per-isp-filter/domains/" + ispFilter.replace(" ","_") + "_domainToBlockCount.tsv","w")
        file.write("Domain\tBlock.Count\n")
        innerBlockDict = filtersToDomainBlocksDict[ispFilter]
        for domain in innerBlockDict:
            try :
                file.write(domain + "\t" + str(innerBlockDict[domain]) + "\n")
            except UnicodeEncodeError:
                print "UnicodeEncodeError"
        file.close()



# Execution code:
#cleanExport()
computeBlockedEntries()
        
        


        
    



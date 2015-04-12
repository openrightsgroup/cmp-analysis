import csv
from Record import Record

class EntriesRetriever:
    # Utility method to get the list of blocked entries from the file
    def getBlockedEntries(self):
        cleanedExport = "../data/export_cleaned.csv"
        recordList = []

        # Get the export file and read it in as a map between URL and probe tests
        print 'Getting the blocked records from the cleaned export file'
        with open(cleanedExport, 'rb') as csvfile:

            # tokenise the line by comma delimiter
            csvReader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in csvReader:
                # Create a data object and output it
                # url, submissionTimestamp, networkName, filterLevel, status, resultTimestamp, httpStatus, probeConfig
                record = Record(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
                if record.status == "blocked":
                    recordList.append(record)

        # return the list of records
        return recordList


    def retrieveURLs(self):
        url_set = set()
        cleanedExport = "../data/export_cleaned.csv"

        # Get the export file and read it in as a map between URL and probe tests
        print 'Getting the examined URLs from the cleaned export file'
        with open(cleanedExport, 'rb') as csvfile:

            # tokenise the line by comma delimiter
            csvReader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in csvReader:
                # Create a data object and output it
                # url, submissionTimestamp, networkName, filterLevel, status, resultTimestamp, httpStatus, probeConfig
                record = Record(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
                url_set.add(record.url)
        return url_set

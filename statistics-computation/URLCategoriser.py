import EntriesIO
import json
from EntriesIO import EntriesRetriever
import urlparse

class URLCategoriser:

    def __init__(self):
        self.urlMap = {}

    def categorise(self,url):
        category = ""

        # First check that we don't have anything mapped for this URL
        if url not in self.urlMap :
            # ask dmoz for the category of the url
            category = "something"
            self.urlMap[url] = category
        else :
            category = self.urlMap[url]

        return category

    def __str__(self):
        return "Computed: " + self.urlMap.__len__()


# Main execution code
# Get the list of blocked entries from the cleaned export
#recordList = EntriesIO.getBlockedEntries()

# Initialise the categoriser
#categoriser = URLCategoriser()
#
#testURL = "www.google.com"
#category = categoriser.categorise(testURL)
#
#print category

jsonoutputfile = '../data/output.json'
linecount = float(sum(1 for line in open(jsonoutputfile)))

# Get the set of URLs that are to be analysed
retriever = EntriesRetriever()
#url_set = retriever.retrieveURLs()
blocked_records = retriever.getBlockedEntries()
url_set = set([record.url for record in blocked_records])
url_set_extended = set([url + "/" for url in url_set])
#print url_set

# map the url to its topics
urltopics = {}
f = open(jsonoutputfile, 'r')

count = float(1.0)
for line in f:
    # parse the line
    j = json.loads(line)
    url = j["url"]

    # strip the URL down to just its root domain
#    parsed_result = urlparse.urlparse(url)
#    stripped_url = parsed_result[0] + "://" + parsed_result[1]
#    print url + " => " + stripped_url

    if url in url_set or url in url_set_extended:
        topics = j["topic"]
        urltopics[url] = topics
        print "Added"

    # get the progress
    progress = (count / linecount) * 100
    print progress
    count += 1

#    if progress > 5:
#        break


    ## to here: need to modify this to handle the set of urls as input (this reduces the memory space issue)

print urltopics
print len(urltopics)

#for record in recordList :
#    category = categoriser.categorise(record.url)
#    print record.url + " | " + category


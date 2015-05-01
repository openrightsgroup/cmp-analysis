from Record import Record
from EntriesIO import EntriesRetriever

from DMOZUtils import DMOZUtils

from accuracy.BT import BTNormalFilter
from accuracy.Sky import Sky_Filter
from accuracy.TalkTalk import TalkTalkFilter
from accuracy.VirginMedia import VirginMediaFilter

from accuracy.Result import Result

###### Functions

def update_result(result, true_label, pred_label):
    # true positive (i.e. correctly blocked)
    if pred_label and true_label:
        result.true_pos += 1
    # true negative (i.e. correctly not blocked)
    elif not pred_label and not true_label:
        result.true_neg += 1
    # false positive (i.e. incorrectly blocked - overblocking)
    elif pred_label and not true_label:
        result.false_pos += 1
    # false negative (i.e. incorrectly not blocked - underblocked)
    elif not pred_label and true_label:
        result.false_neg += 1
    return result

###### Main Execution Code

# Get the set of records that are to be checked
print "Retrieving all entries records"
break_point = 100
retriever  = EntriesRetriever()
records = retriever.getAllEntries(break_point)

# Generate urls for category checking
print "Generating URL and extended URL List"
url_set = set([record.url for record in records])
url_set_extended = set([url + "/" for url in url_set])

# Load the relevant DMOZ Categories
print "Extracting DMOZ categories for the URLs"
urltopics = DMOZUtils.get_dmoz_categories(url_set, url_set_extended)

# Prime the result maps for each filter
results_map = {"BT": Result("BT"),
               "Sky": Result("Sky"),
               "TalkTalk": Result("TalkTalk"),
               "VirginMedia": Result("VirginMedia")}


# For each record assess each filter that is relevant
print "Checking the records and computing contingency table"
for record in records:

    # If the record's domain has a DMOZ category, then get that category
    if record.url in urltopics or record.url + "/" in urltopics:
        url_key = record.url
        if record.url+"/" in urltopics:
            url_key += "/"
        cat = urltopics[url_key]

        # Work out which ISP it belongs to
        if record.networkName == "BT":
            # Get the predicted label
            filter = BTNormalFilter()
            print "Filter = " + record.networkName
            print("Cat = " + str(cat))

            pred_label = filter.block_cat(cat)
            print str(pred_label)

            # Work out if the category should be blocked or not: true label
            true_label = False
            if record.status == "blocked":
                true_label = True

            # Update the filter's result
            results_map["BT"] = update_result(results_map["BT"], true_label, pred_label)



print results_map["BT"]


from EntriesIO import EntriesRetriever
from DMOZUtils import DMOZUtils

def writePerFilterBlockCounts(per_filter_blocked_categories, category_depth) :
    # For each ispfilter, write out the dictionary mapping the categories and their counts
    for isp_filter in  per_filter_blocked_categories:
        file = open("../data/per-isp-filter/categories/" + isp_filter.replace(" ","_") + "_categoriesToBlockCount" + str(category_depth) + ".tsv","w")
        file.write("Category\tBlock.Count\n")
        innerBlockDict = per_filter_blocked_categories[isp_filter]
        for category in innerBlockDict:
            try :
                file.write(category + "\t" + str(innerBlockDict[category]) + "\n")
            except UnicodeEncodeError:
                print "UnicodeEncodeError"
        file.close()

##### Main execution code

# Get the set of URLs that are to be analysed
retriever = EntriesRetriever()
blocked_records = retriever.getBlockedEntries()
url_set = set([record.url for record in blocked_records])
url_set_extended = set([url + "/" for url in url_set])

urltopics = DMOZUtils.get_dmoz_categories(url_set, url_set_extended)

#### Code to analyse the topic level distribution
topic_level_depths = [4, 5, 6]
for topic_level_depth in topic_level_depths:
    ##### Computer per filter block distribution
    print "Computing blocked categories distribution for depth " + str(topic_level_depth)
    per_filter_blocked_categories = {}
    for record in blocked_records:
        # Check that we have a mapping from the url to its topics
        url_key = ""
        matched_url = False
        if record.url in urltopics:
            url_key = record.url
            matched_url = True
        elif record.url + "/" in urltopics:
            url_key = record.url + "/"
            matched_url = True

        if matched_url:
            isp_filter = record.networkName
            topics_list = urltopics[url_key].split("/")

            # build the topic key to the topic_level_depth
            topic_key = ""
            if len(topics_list) <= topic_level_depth:
                topic_key = urltopics[url_key] + "/"
            else:
                i = 0
                while i < topic_level_depth - 1:
                    topic_key += topics_list[i] + "/"
                    i += 1

            # check that we have a mapping for the isp_filter already, if not create one
            if isp_filter not in per_filter_blocked_categories:
                blocked_cats = {topic_key: 1}
                per_filter_blocked_categories[isp_filter] = blocked_cats
            else:
                blocked_cats = per_filter_blocked_categories[isp_filter]
                # add the topic to the map, or increment the count
                if topic_key in blocked_cats:
                    blocked_cats[topic_key] += 1
                else:
                    blocked_cats[topic_key] = 1
                per_filter_blocked_categories[isp_filter] = blocked_cats

    # show the output from the mapping
    for isp_filter in per_filter_blocked_categories:
        print "\n" + isp_filter
        print per_filter_blocked_categories[isp_filter]

    # Write the distribution to a local file for plotting in R
    writePerFilterBlockCounts(per_filter_blocked_categories, topic_level_depth)



        




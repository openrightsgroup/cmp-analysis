import json

class DMOZUtils:
    @staticmethod
    def get_dmoz_categories(url_set, url_set_extended):
        # map the url to its topics
        print "Mapping URLs to topics"
        urltopics = {}

        # Do the non-adult content
        print "Extracting non-adult categories"
        dmoz_cats_files = '../data/output.json'
        linecount = float(sum(1 for line in open(dmoz_cats_files)))
        f = open(dmoz_cats_files, 'r')
        count = float(1.0)
        for line in f:
            # parse the line
            j = json.loads(line)
            url = j["url"]
            topics = j["topic"]
            if url in url_set or url in url_set_extended:
                # Strip out the first top element
                urltopics[url] = topics.replace("Top/","").replace("'","")
                #        print "Added"

            # get the progress
            progress = (count / linecount) * 100
            #        print progress
            count += 1

        #    if progress > 5:
        #        break

        # Do the adult content
        # Do the non-adult content
        print "Extracting adult categories"
        dmoz_adult_cats_files = '../data/ad-output.json'
        linecount = float(sum(1 for line in open(dmoz_adult_cats_files)))
        f = open(dmoz_adult_cats_files, 'r')
        count = float(1.0)
        for line in f:
            # parse the line
            j = json.loads(line)
            url = j["url"]
            topics = j["topic"]
            if url in url_set or url in url_set_extended:
                # Strip out the first top element
                urltopics[url] = topics.replace("Top/","").replace("'","")
#                print urltopics[url]

            # get the progress
            progress = (count / linecount) * 100
            #        print progress
            count += 1
        return urltopics


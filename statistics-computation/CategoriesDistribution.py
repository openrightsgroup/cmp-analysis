__author__ = 'rowem'

import logging
from pyspark import SparkContext, SparkConf
from result import ResultLog
import json


def match_cat_with_ofcom_cat(cats):
    # map of the category label to the DMOZ categories that it uses
    cat_labels_map = {}
    cat_labels_map['Pornography'] = ["Adult"]
    cat_labels_map['Hacking'] = ["Computers/Hacking"]
    cat_labels_map['Drugs'] = ["Recreation/Drugs"]
    cat_labels_map['Alcohol'] = ["Recreation/Food/Drink/Drinking",
                                 "Recreation/Food/Drink/Mead",
                                 "Recreation/Food/Drink/Wine",
                                 "Recreation/Food/Drink/Beer",
                                 "Recreation/Food/Drink/Alcopops",
                                 "Recreation/Food/Drink/Cider",
                                 "Recreation/Food/Drink/Cocktails",
                                 "Recreation/Food/Drink/Liquor",
                                 "Recreation/Food/Drink/Sake",
                                 "Health/Specific Substances/Alcoholic Beverages"]
    cat_labels_map['Smoking'] = ["Shopping/Tobacco",
                                 "Recreation/Tobacco"]
    cat_labels_map['Dating'] = ["Society/Relationships/Dating",
                                "Society/Relationships/Cyber_Relationships",
                                "Regional/Europe/United Kingdom/Society_and_Culture/Gay,_Lesbian,_and_Bisexual/Relationships"]
    cat_labels_map['Gaming'] = ["Games",
                                "Computers/Software/Internet/Clients/File_Sharing"]
    cat_labels_map['Gambling'] = ["Gambling"]
    cat_labels_map['Social-Networking'] = ["Computers/Internet/On_the_Web/Online_Communities/Social_Networking",
                                           "Kids_and_Teens/People_and_Society/Online Communities"]

    ofcom_cats = set()
    for cat in cats:
        # print("cat = " + str(cat))
        # match the cat with the ofcom key
        for ofcom_cat in cat_labels_map:
            mapped_cats = cat_labels_map[ofcom_cat]
            for mapped_cat in mapped_cats:
                # check that the mapped category is contained within the url's category from DMOZ
                if mapped_cat in cat:
                    ofcom_cats.add(ofcom_cat)
                    break
    return ofcom_cats


#### For getting the Ofcom category distribution
def flatMapLineToOfcomCategorySingletonTuple(line):
    ofcom_freq_tuples = []

    # get the topics from the broadcast
    topics = bTopics.value
    tokens = line.encode('utf-8').split(",")
    if len(tokens) is 10:
        url = tokens[0]
        # match the URL to the topic
        if url in topics or url + "/" in topics:
            url_key = url
            if url+"/" in topics:
                url_key += "/"
            cats = topics[url_key].split(";")
            logging.info(url + " - found cats = " + str(cats))

            # get the ofcom key from the cats
            ofcom_cats = match_cat_with_ofcom_cat(cats)
            for ofcom_cat in ofcom_cats:
                # url_set.append(url)
                # url_list = [url]
                ofcom_freq_tuples.append((ofcom_cat, url))
    return ofcom_freq_tuples

# def ofcomCategoriesReducer(tupleMap1, tupleMap2):
#     returnTupleMap = tupleMap1
#     for url in tupleMap2:
#         if url not in returnTupleMap:
#             returnTupleMap[url] = tupleMap2[url]
#     return returnTupleMap

def ofcomUrlCounter(tuple):
    url_set = set(tuple[1])
    return (tuple[0], len(url_set))

##### For loading DMOZ categories
def getURLMapper(line):
    j = json.loads(line)
    url = j["url"].encode('utf-8')
    topics = j["topic"].encode('utf-8')
    # Strip out the first top element
    return (url, topics.replace("Top/","").replace("'",""))

def reduceByURL(topics1, topics2):
    topics = topics1 + ";" + topics2
    return topics

if __name__ == "__main__":

    ##### Main Execution Code
    conf = SparkConf().setAppName("CMP Filters Processing - Categories Analyser")
    conf.set("spark.python.worker.memory","10g")
    conf.set("spark.driver.memory","10g")
    conf.set("spark.executor.memory","10g")
    conf.set("spark.default.parallelism", "12")
    conf.set("spark.mesos.coarse", "true")
    conf.set("spark.driver.maxResultSize", "10g")
    # Added the core limit to avoid resource allocation overruns
    conf.set("spark.cores.max", "5")
    conf.setMaster("mesos://zk://scc-culture-slave9.lancs.ac.uk:2181/mesos")
    conf.set("spark.executor.uri", "hdfs://scc-culture-mind.lancs.ac.uk/lib/spark-1.3.0-bin-hadoop2.4.tgz")
    conf.set("spark.broadcast.factory", "org.apache.spark.broadcast.TorrentBroadcastFactory")

    sc = SparkContext(conf=conf)
    sc.setCheckpointDir("hdfs://scc-culture-mind.lancs.ac.uk/data/checkpointing")

    # Load the DMOZ Topics map from HDFS using Spark
    # First get the non adult categories
    print("Loading General DMOZ Cats")
    nonAdultDmozFile = sc.textFile("hdfs://scc-culture-mind.lancs.ac.uk/data/output.json")
    nonAdultURLTopics = nonAdultDmozFile.map(getURLMapper).reduceByKey(reduceByURL)
    print("Loaded url topics = " + str(nonAdultURLTopics.count()))

    # Second get the adult categories
    print("Loading Adult DMOZ Cats")
    adultDmozFile = sc.textFile("hdfs://scc-culture-mind.lancs.ac.uk/data/ad-output.json")
    adultURLTopics = adultDmozFile.map(getURLMapper).reduceByKey(reduceByURL)
    print("Loaded adult url topics = " + str(adultURLTopics.count()))

    # join the results
    print("Joining URL Topics")
    urlTopics = nonAdultURLTopics.union(adultURLTopics)
    print("Joined url topics = " + str(urlTopics.count()))
    urlTopics.cache()

    # broadcast the topics
    #    someValue = 1
    # convert topics to map and broadcast
    print("Broadcasting key-value pairs from RDD")
    bTopics = sc.broadcast(urlTopics.collectAsMap())

    # go through and get the category of each URL
    print("Counting Ofcom Categories of URLs")
    distFile = sc.textFile("hdfs://scc-culture-mind.lancs.ac.uk/data/export-dec-2015.csv")
    category_counts = distFile\
        .flatMap(flatMapLineToOfcomCategorySingletonTuple)\
        .map(lambda x: x)\
        .collect()
        # .map(ofcomUrlCounter)\


    print("Performing single node reduction")
    ofcom_cat_map = {}
    for (ofcom_cat, url) in category_counts:
        if ofcom_cat in ofcom_cat_map:
            cat_urls = ofcom_cat_map[ofcom_cat]
            cat_urls.add(url)
            ofcom_cat_map[ofcom_cat] = cat_urls
        else:
            cat_urls = set()
            cat_urls.add(url)
            ofcom_cat_map[ofcom_cat] = cat_urls

    for ofcom_cat in ofcom_cat_map:
        print(ofcom_cat + " size = " + str(len(ofcom_cat_map[ofcom_cat])))


    print("Counting total URLs")
    total_url_set = set()
    for (ofcom_cat, url) in category_counts:
        total_url_set.add(url)
    print("Total URLs = " + str(len(total_url_set)))



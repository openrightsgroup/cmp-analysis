from __future__ import print_function

import sys
import os
from random import random
from operator import add
from pyspark import SparkContext, SparkConf
from result import ResultLog
import json
from functools import partial

if __name__ == "__main__":

    ##### Map-Reduce Functions
    ###### For processing export file
    def getNameMapper(line):
        # get the topics from the broadcast
        topics = bTopics.value
        tokens = line.split(",")
        if len(tokens) is 10:
            filter_name = tokens[2]
            request_result = tokens[4]
            url = tokens[0]
            result = ResultLog(filter_name)
            result.check_url(url, topics, request_result)
#            result.checkURL(str(topics.count()))
            return (filter_name, result)
        else:
            result = ResultLog("null")
            return ("null", result)

    def reduceByName(result1, result2):
        result = ResultLog(result1.filter_name)
        result.merge_results(result1, result2)
        return result

    ##### For loading DMOZ categories
    def getURLMapper(line):
        j = json.loads(line)
        url = j["url"]
        topics = j["topic"]
        # Strip out the first top element
        return (url, topics.replace("Top/","").replace("'",""))

    def reduceByURL(topics1, topics2):
        topics = topics1 + ";" + topics2
        return topics


    ##### Main Execution Code
    conf = SparkConf().setAppName("CMP Filters Processing - False Blocks Computation")
    conf.set("spark.python.worker.memory","10g")
    conf.set("spark.driver.memory","15g")
    conf.set("spark.executor.memory","10g")
    conf.set("spark.default.parallelism", "12")
    conf.set("spark.mesos.coarse", "true")
    conf.set("spark.driver.maxResultSize", "10g")
    conf.setMaster("mesos://zk://scc-culture-mind.lancs.ac.uk:2181/mesos")
    conf.set("spark.executor.uri", "hdfs://scc-culture-mind.lancs.ac.uk/lib/spark-1.3.0-bin-hadoop2.4.tgz")
    conf.set("spark.broadcast.factory", "org.apache.spark.broadcast.TorrentBroadcastFactory")
    #test

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
    print("Broadcasting key-value pairs from RDD")
    bTopics = sc.broadcast(urlTopics.collectAsMap())

#    # Read in export file from local disk as RDD
    distFile = sc.textFile("hdfs://scc-culture-mind.lancs.ac.uk/data/export_cleaned.csv")
    counts = distFile.map(lambda line: getNameMapper(line)).reduceByKey(reduceByName)

    output = counts.collect()
    print("Writing false positives and false negatives to disk...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for (filter_name, result_log) in output:
        print(filter_name)
        # Write to the local file system
        # false positives first
        file_fp_write = open(current_dir + "/../data/output/" + filter_name + "_fps.csv", "w")
        file_fp_write.write(result_log.fp_str())
        file_fp_write.close()

        # false negatives next
        file_fn_write = open(current_dir + "/../data/output/" + filter_name + "_fns.csv", "w")
        file_fn_write.write(result_log.fn_str())
        file_fn_write.close()
    sc.stop()


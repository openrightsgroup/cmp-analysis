from __future__ import print_function

import sys
import os
from random import random
from operator import add
from pyspark import SparkContext, SparkConf
from result import ResultLog
import json
from functools import partial
from datetime import datetime, timedelta

if __name__ == "__main__":

    ##### Map-Reduce Functions
    ###### For processing export file
    def getNameMapper(line):
        # Set the analysis start point - use this to convert the date into a week from number to use in the maps
        dateFormatter = "%Y-%m-%d %H:%M:%S"
        startDate = datetime.strptime("2013-01-01 00:00:00", dateFormatter)

        # get the topics from the broadcast
        topics = bTopics.value
        tokens = line.split(",")
        if len(tokens) is 10:
            filter_name = tokens[2]
            request_result = tokens[4]
            url = tokens[0]

            # Get the date and the weeks from the date
            dateString = tokens[5]
            if "Result" not in dateString:
                date = datetime.strptime(dateString.replace("\"",""), dateFormatter)
                startMonday = (startDate - timedelta(days=startDate.weekday()))
                dateMonday = (date - timedelta(days=date.weekday()))
                weekDiffKey = (dateMonday - startMonday).days / 7

                # Get the result from checking the URL
                result = ResultLog(filter_name)
                result.check_url(url, topics, request_result)

                # Map the date to when the url was computed
                return (filter_name, {weekDiffKey: result})
            else:
                result = ResultLog("null")
                return ("null", {0: result})
        else:
            result = ResultLog("null")
            return ("null", {0: result})

    def reduceByName(resultMap1, resultMap2):
        # Combines the result maps together
        resultMapNew = resultMap1
        for weekKey in resultMap2.keys():
            weekResult = resultMap2[weekKey]

            # merge the results if they exist for this week already
            if weekKey in resultMapNew:
                currentWeekResult = resultMapNew[weekKey]
                newResult = ResultLog(currentWeekResult.filter_name)
                newResult.merge_results(currentWeekResult, weekResult)
                resultMapNew[weekKey] = newResult
            # otherwise generate map the week to the current result
            else:
                resultMapNew[weekKey] = weekResult
        return resultMapNew

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
    conf = SparkConf().setAppName("CMP Filters Processing - Time-Series Accuracy Computation")
    conf.set("spark.python.worker.memory","10g")
    conf.set("spark.driver.memory","15g")
    conf.set("spark.executor.memory","10g")
    conf.set("spark.default.parallelism", "12")
    conf.set("spark.mesos.coarse", "true")
    conf.set("spark.driver.maxResultSize", "10g")
    # Added the core limit to avoid resource allocation overruns
    conf.set("spark.cores.max", "5")
    conf.setMaster("mesos://zk://scc-culture-mind.lancs.ac.uk:2181/mesos")
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

#    bTopics = sc.broadcast({"a": 1, "b": 2, "c": 3})
    # Separate spark context for broadcasting?


#    # Read in export file from local disk as RDD
    distFile = sc.textFile("hdfs://scc-culture-mind.lancs.ac.uk/data/export_cleaned.csv")
    counts = distFile.map(lambda line: getNameMapper(line)).reduceByKey(reduceByName)
    output = counts.collect()

    print("Filter Accuracy...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for (filter_name, week_map) in output:
        print(filter_name)
        # Write to the local file system
        file = open(current_dir + "/../data/output/" + filter_name + "_ts_accuracy.csv","w")
        for week_key in sorted(week_map):
            file.write(str(week_key) + "," + str(week_map[week_key].csv_str()) + "\n")
        file.close()
    sc.stop()


from __future__ import print_function

import sys
from random import random
from operator import add
from pyspark import SparkContext, SparkConf
from result import Result
import json
from functools import partial
from datetime import datetime, timedelta

if __name__ == "__main__":

    ##### Map-Reduce Functions
    ###### For processing export file
    def ispNameMapper(line):
        # Split the line into tokens
        tokens = line.split(",")
        dateFormatter = "%Y-%m-%d %H:%M:%S"
        if len(tokens) is 10:
            filter_name = tokens[2]
            request_result = tokens[4]
            url = tokens[0]
            dateString = tokens[5]
            date = datetime.strptime(dateString.replace("\"", ""), dateFormatter)

            date_to_status = {date: request_result}
            url_to_results = {url: date_to_status}

#            result.checkURL(str(topics.count()))
            return (filter_name, url_to_results)
        else:
            url_to_results = {}
            return ("null", url_to_results)

    def reduceByISPName(url_to_results_1, url_to_results_2):
        url_to_results = url_to_results_1
        for url in url_to_results_2:
            if url in url_to_results:
                url_to_results[url].update(url_to_results_2[url])
            else:
                url_to_results[url] = url_to_results_2[url]
        return url_to_results

    ######## For reducing the isp to domain dates map once more
    def ispDomainMapper((key, value)):
        pass

#test
    ##### Main Execution Code
    conf = SparkConf().setAppName("CMP Filters - Unblock Delta Function Computation")
    conf.set("spark.python.worker.memory","10g")
    conf.set("spark.driver.memory","15g")
    conf.set("spark.executor.memory", "10g")
    conf.set("spark.default.parallelism", "12")
    conf.set("spark.mesos.coarse", "true")
    conf.set("spark.driver.maxResultSize", "10g")
    conf.setMaster("mesos://zk://scc-culture-mind.lancs.ac.uk:2181/mesos")
    conf.set("spark.executor.uri", "hdfs://scc-culture-mind.lancs.ac.uk/lib/spark-1.3.0-bin-hadoop2.4.tgz")
    conf.set("spark.broadcast.factory", "org.apache.spark.broadcast.TorrentBroadcastFactory")

    sc = SparkContext(conf=conf)
    sc.setCheckpointDir("hdfs://scc-culture-mind.lancs.ac.uk/data/checkpointing")


    distFile = sc.textFile("hdfs://scc-culture-mind.lancs.ac.uk/data/export_cleaned.csv")
    # Run first map reduce job to generate <isp, <url, <date, status>>> nested map
    print("Running first map reduce job to generate nested isp-to-url-status-dates map")
    ispDomainsMap = distFile.map(lambda line: ispNameMapper(line)).reduceByKey(reduceByISPName)
    output = ispDomainsMap.collect()
    print("ISP - Status results")
    for (isp, url_to_results) in output:
        print(isp + "...")
        for url in url_to_results:
            print(url + "......")
            date_to_status = url_to_results[url]
            for date in date_to_status:
                print(date + " with " + date_to_status[date])

    print("Running second map reduce job to generate isp-to-unblock-time-count map ")



#    #print("Writing output to HDFS")
#    #counts.saveAsTextFile("hdfs://scc-culture-mind.lancs.ac.uk/data/test-export")

	
    sc.stop()


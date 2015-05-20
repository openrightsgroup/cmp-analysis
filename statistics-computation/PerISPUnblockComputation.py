from __future__ import print_function

import sys
from random import random
from operator import add
from pyspark import SparkContext, SparkConf
from result import Result
import json
from functools import partial
from datetime import datetime, timedelta, date
import os

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
            if "Result" not in dateString:
                date = datetime.strptime(dateString.replace("\"", ""), dateFormatter)
                date_to_status = {date: request_result}
                url_to_results = {url: date_to_status}
                return (filter_name, url_to_results)
            else:
                url_to_results = {}
                return ("null", url_to_results)

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
    # Added the core limit to avoid resource allocation overruns
    conf.set("spark.cores.max", "5")
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
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for (isp, url_to_results) in output:
        print(isp + "...")
        # for each ISP log the delta distribution (in hours) between the blocked and ok dates
        delta_dist = []
        for url in url_to_results:
            # print(url + "......")
            date_to_status = url_to_results[url]
            prior_blocked = False
            blocked_date = date.today()
            for date in sorted(date_to_status.keys()):
                status = str(date_to_status[date])

                # check if the URL has been blocked
                if "blocked" in status:
                    prior_blocked = True
                    blocked_date = date

                # check if the next URL is OK
                if prior_blocked:
                    if "ok" in status:
                        prior_blocked = False
                        unblock_date = date
                        # work out the difference in hours
                        hoursDiff = unblock_date - blocked_date
                        delta_dist.append(str(hoursDiff.total_seconds() / 60))
        print(delta_dist)
        # Write the delta distribution to a CSV file for processing
        file = open(current_dir + "/../data/output/" + isp + "_unblock_dist.csv", "w")
        for delta in delta_dist:
            file.write(str(delta) + "\n")
        file.close()


#    #print("Writing output to HDFS")
#    #counts.saveAsTextFile("hdfs://scc-culture-mind.lancs.ac.uk/data/test-export")

	
    sc.stop()


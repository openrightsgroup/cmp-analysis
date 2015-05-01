from __future__ import print_function

import sys
from random import random
from operator import add

from pyspark import SparkContext


if __name__ == "__main__":
    """
        Usage: pi [partitions]
    """
    sc = SparkContext(appName="SparkFileReadTest")

    # Read in export file from local disk as RDD
    distFile = sc.textFile("/home/rowem/data/export_cleaned.csv")
    counts = distFile.flatMap(lambda line: line.split("\t")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
    counts.saveAsTextFile("/home/rowem/data/counts.csv")

    sc.stop()

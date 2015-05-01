# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 16:12:02 2014

@author: mrowe
"""

class Record:
    def __init__(self, url, submissionTimestamp, networkName, filterLevel, status, resultTimestamp, httpStatus, probeConfig):
        self.url = url
        self.submissionTimestamp = submissionTimestamp
        self.networkName = networkName
        self.filterLevel = filterLevel
        self.status = status
        self.resultTimestamp = resultTimestamp
        self.httpStatus = httpStatus
        self.probeConfig = probeConfig
        
    def __str__(self):
        return "URL: " + self.url + " | Submitted: " + self.submissionTimestamp + " | NetworkName: " + self.networkName + " | Status: " + self.status
        
    def tsvString(self):
        return self.url + "\t" + self.submissionTimestamp + "\t" + self.networkName + "\t" + self.filterLevel + "\t" + self.status + "\t" \
               + self.resultTimestamp + "\t" + self.httpStatus + "\t" + self.probeConfig
        
    def compareRecords(recordA, recordB):
        same = False
        if recordA.url is recordB.url and recordA.networkName is recordB.networkName:
            same = True
        return same
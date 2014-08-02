# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 16:12:02 2014

@author: mrowe
"""

class Record:
    def __init__(self, url, submissionTimestamp, networkName, filterLevel, status, resulTimestamp, httpStatus, probeConfig):
        self.url = url
        self.submissionTimestamp = submissionTimestamp
        self.networkName = networkName
        self.filterLevel = filterLevel
        self.status = status
        self.resulTimestamp = resulTimestamp
        self.httpStatus = httpStatus
        self.probeConfig = probeConfig
        
    def __str__(self):
        return "URL: " + self.url + " | Submitted: " + self.submissionTimestamp + " | NetworkName: " + self.networkName + " | Status: " + self.status
        
    def tsvString(self):
        return self.url + "\t" + self.submissionTimestamp + "\t" + self.networkName + "\t" + self.filterLevel + "\t" + self.status + "\t" + self.resulTimestamp + "\t" + self.httpStatus + "\t" + self.probeConfig
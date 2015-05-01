class Result(object):
    def __init__(self, filter_name):
        self.filter_name = filter_name
        self.true_pos = 0
        self.true_neg = 0
        self.false_pos = 0
        self.false_neg = 0

    def checkURL(self, url):
        # Check the URL using the appropriate filter
        self.true_pos = 1

    def mergeResults(self, result1, result2):
        self.true_pos = result1.true_pos + result2.true_pos

    def __str__(self):
        return "tp = " + str(self.true_pos) + " | tn = " + str(self.true_neg)\
               + " | fp = " + str(self.false_pos) + " | fn = " + str(self.false_neg)

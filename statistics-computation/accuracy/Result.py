class Result:
    def __init__(self, filter_name):
        self.filter_name = filter_name

        self.true_pos = 0
        self.true_neg = 0
        self.false_pos = 0
        self.false_neg = 0

    def __str__(self):
        return self.filter_name + " | tp = " + str(self.true_pos) + " | tn = " + str(self.true_neg) \
               + " | fp = " + str(self.false_pos) + " | fn = " + str(self.false_neg)

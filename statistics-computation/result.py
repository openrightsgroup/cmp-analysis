from ISPFilters import *
from MobileFilters import *
from FilterClassifier import *
import math


class Result(object):
    def __init__(self, filter_name):
        self.filter_name = filter_name.strip()
        self.true_pos = 0
        self.true_neg = 0
        self.false_pos = 0
        self.false_neg = 0

        # Load the appropriate filter given the filter name
        if "BT" in self.filter_name:
            self.filter = BTNormalFilter()
        elif "Sky" in self.filter_name:
            self.filter = SkyFilter()
        elif "TalkTalk" in self.filter_name:
            self.filter = TalkTalkFilter()
        elif "VirginMedia" in self.filter_name:
            self.filter = VirginMediaFilter()
        elif "EE" in self.filter_name:
            self.filter = EEFilter()
        elif "O2" in self.filter_name:
            self.filter = O2Filter()
        elif "Three" in self.filter_name:
            self.filter = ThreeFilter()
        elif "VirginMobile" in self.filter_name:
            self.filter = VirginMobileFilter()
        elif "Vodafone" in self.filter_name:
            self.filter = VodafoneFilter()
        else:
            self.filter = NullFilter()

    def check_url(self, url, topics, request_result):
        # check that the url has categories mapped to it
        if url in topics or url + "/" in topics:
            url_key = url
            if url+"/" in topics:
                url_key += "/"
            cats = topics[url_key].split(";")
            # cat = topics[url_key]

            # check each category
            true_label = False
            for cat in cats:
                true_label = self.filter.block_cat(cat)
                if true_label is True:
                    break

            # Work out if the category should be blocked or not: true label
            pred_label = False
            if request_result == "blocked":
                pred_label = True

            # true positive (i.e. correctly blocked)
            if pred_label and true_label:
                self.true_pos += 1
            # true negative (i.e. correctly not blocked)
            elif not pred_label and not true_label:
                self.true_neg += 1
            # false positive (i.e. incorrectly blocked - overblocking)
            elif pred_label and not true_label:
                self.false_pos += 1
            # false negative (i.e. incorrectly not blocked - underblocked)
            elif not pred_label and true_label:
                self.false_neg += 1

    def merge_results(self, result1, result2):
        self.true_pos = result1.true_pos + result2.true_pos
        self.true_neg = result1.true_neg + result2.true_neg
        self.false_pos = result1.false_pos + result2.false_pos
        self.false_neg = result1.false_neg + result2.false_neg

    def __str__(self):
        # compute precision, recall, fpr, and f-measure if we have non zero numbers
        prec = 0
        rec = 0
        fpr = 0
        mcc = 0
        f1 = 0
        if self.true_pos > 0 and self.false_pos > 0 and self.false_neg > 0:
            prec = float(self.true_pos) / (float(self.true_pos) + float(self.false_pos))
            rec = float(self.true_pos) / (float(self.true_pos) + float(self.false_neg))
            fpr = float(self.false_pos) / (float(self.false_pos) + float(self.true_neg))
            mcc_numerator = (float(self.true_pos) * float(self.true_neg)) - (float(self.false_pos) * float(self.false_neg))
            mcc_denominator = (self.true_pos + self.false_pos) * (self.true_pos + self.false_neg) * (self.true_neg + self.false_pos) * (self.true_neg + self.false_neg)
            mcc_denominator = math.sqrt(mcc_denominator)
            if mcc_denominator > 0:
                mcc = mcc_numerator / mcc_denominator
            f1 = 2 * ((prec * rec) / (prec + rec))

        return "tp = " + str(self.true_pos) + " | tn = " + str(self.true_neg)\
               + " | fp = " + str(self.false_pos) + " | fn = " + str(self.false_neg)\
               + " | prec = " + str("%.3f" % prec) + " | rec = " + str("%.3f" % rec) + " | FPR = " + str("%.3f" % fpr) \
               + " | mcc = " + str("%.3f" % mcc) + " | F1 = " + str("%.3f" % f1)

    def csv_str(self):
        # compute precision, recall, fpr, and f-measure if we have non zero numbers
        prec = 0
        rec = 0
        fpr = 0
        mcc = 0
        f1 = 0
        if self.true_pos > 0 and self.false_pos > 0 and self.false_neg > 0:
            prec = float(self.true_pos) / (float(self.true_pos) + float(self.false_pos))
            rec = float(self.true_pos) / (float(self.true_pos) + float(self.false_neg))
            fpr = float(self.false_pos) / (float(self.false_pos) + float(self.true_neg))
            mcc_numerator = (float(self.true_pos) * float(self.true_neg)) - (float(self.false_pos) * float(self.false_neg))
            mcc_denominator = (self.true_pos + self.false_pos) * (self.true_pos + self.false_neg) * (self.true_neg + self.false_pos) * (self.true_neg + self.false_neg)
            mcc_denominator = math.sqrt(mcc_denominator)
            if mcc_denominator > 0:
                mcc = mcc_numerator / mcc_denominator
            f1 = 2 * ((prec * rec) / (prec + rec))

        return str(self.true_pos) + "," + str(self.true_neg)\
               + "," + str(self.false_pos) + "," + str(self.false_neg)\
               + "," + str("%.3f" % prec) + "," + str("%.3f" % rec) + "," + str("%.3f" % fpr)\
               + "," + str("%.3f" % mcc) + "," + str("%.3f" % f1)


class ResultLog(object):
    def __init__(self, filter_name):
        self.filter_name = filter_name.strip()
        self.true_pos = set()
        self.true_neg = set()
        self.false_pos = set()
        self.false_neg = set()

        # Load the appropriate filter given the filter name
        if "BT" in self.filter_name:
            self.filter = BTNormalFilter()
        elif "Sky" in self.filter_name:
            self.filter = SkyFilter()
        elif "TalkTalk" in self.filter_name:
            self.filter = TalkTalkFilter()
        elif "VirginMedia" in self.filter_name:
            self.filter = VirginMediaFilter()
        elif "EE" in self.filter_name:
            self.filter = EEFilter()
        elif "O2" in self.filter_name:
            self.filter = O2Filter()
        elif "Three" in self.filter_name:
            self.filter = ThreeFilter()
        elif "VirginMobile" in self.filter_name:
            self.filter = VirginMobileFilter()
        elif "Vodafone" in self.filter_name:
            self.filter = VodafoneFilter()
        else:
            self.filter = NullFilter()

    def check_url(self, url, topics, request_result):
        # check that the url has categories mapped to it
        if url in topics or url + "/" in topics:
            url_key = url
            if url+"/" in topics:
                url_key += "/"
            cats = topics[url_key].split(";")
            # cat = topics[url_key]

            # check each category
            true_label = False
            for cat in cats:
                true_label = self.filter.block_cat(cat)
                if true_label is True:
                    break

            # Work out if the category should be blocked or not: true label
            pred_label = False
            if request_result == "blocked":
                pred_label = True

            # true positive (i.e. correctly blocked)
            if pred_label and true_label:
                self.true_pos.add(url_key)
            # true negative (i.e. correctly not blocked)
            elif not pred_label and not true_label:
                self.true_neg.add(url_key)
            # false positive (i.e. incorrectly blocked - overblocking)
            elif pred_label and not true_label:
                self.false_pos.add(url_key)
            # false negative (i.e. incorrectly not blocked - underblocked)
            elif not pred_label and true_label:
                self.false_neg.add(url_key)

    def merge_results(self, result1, result2):
        self.true_pos = result1.true_pos.union(result2.true_pos)
        self.true_neg = result1.true_neg.union(result2.true_neg)
        self.false_pos = result1.false_pos.union(result2.false_pos)
        self.false_neg = result1.false_neg.union(result2.false_neg)

    def __str__(self):
        # compute precision, recall, fpr, and f-measure if we have non zero numbers
        prec = 0
        rec = 0
        fpr = 0
        mcc = 0
        f1 = 0
        if self.true_pos > 0 and self.false_pos > 0 and self.false_neg > 0:
            prec = float(len(self.true_pos)) / (float(len(self.true_pos)) + float(len(self.false_pos)))
            rec = float(len(self.true_pos)) / (float(len(self.true_pos)) + float(len(self.false_neg)))
            fpr = float(len(self.false_pos)) / (float(len(self.false_pos)) + float(len(self.true_neg)))
            mcc_numerator = (float(len(self.true_pos)) * float(len(self.true_neg))) - (float(len(self.false_pos)) * float(len(self.false_neg)))
            mcc_denominator = len(self.true_pos.union(self.false_pos)) * \
                              len(self.true_pos.union(self.false_neg)) * \
                              len(self.true_neg.union(self.false_pos)) * \
                              len(self.true_neg.union(self.false_neg))
            mcc_denominator = math.sqrt(mcc_denominator)
            if mcc_denominator > 0:
                mcc = mcc_numerator / mcc_denominator
            f1 = 2 * ((prec * rec) / (prec + rec))

        return "tp = " + str(self.true_pos) + " | tn = " + str(self.true_neg)\
               + " | fp = " + str(self.false_pos) + " | fn = " + str(self.false_neg)\
               + " | prec = " + str("%.3f" % prec) + " | rec = " + str("%.3f" % rec) + " | FPR = " + str("%.3f" % fpr) \
               + " | mcc = " + str("%.3f" % mcc) + " | F1 = " + str("%.3f" % f1)

    def csv_str(self):
       # compute precision, recall, fpr, and f-measure if we have non zero numbers
        prec = 0
        rec = 0
        fpr = 0
        mcc = 0
        f1 = 0
        if self.true_pos > 0 and self.false_pos > 0 and self.false_neg > 0:
            prec = float(len(self.true_pos)) / (float(len(self.true_pos)) + float(len(self.false_pos)))
            rec = float(len(self.true_pos)) / (float(len(self.true_pos)) + float(len(self.false_neg)))
            fpr = float(len(self.false_pos)) / (float(len(self.false_pos)) + float(len(self.true_neg)))
            mcc_numerator = (float(len(self.true_pos)) * float(len(self.true_neg))) - (float(len(self.false_pos)) * float(len(self.false_neg)))
            mcc_denominator = len(self.true_pos.union(self.false_pos)) * \
                              len(self.true_pos.union(self.false_neg)) * \
                              len(self.true_neg.union(self.false_pos)) * \
                              len(self.true_neg.union(self.false_neg))
            mcc_denominator = math.sqrt(mcc_denominator)
            if mcc_denominator > 0:
                mcc = mcc_numerator / mcc_denominator
            f1 = 2 * ((prec * rec) / (prec + rec))

        return str(self.true_pos) + "," + str(self.true_neg)\
               + "," + str(self.false_pos) + "," + str(self.false_neg)\
               + "," + str("%.3f" % prec) + "," + str("%.3f" % rec) + "," + str("%.3f" % fpr)\
               + "," + str("%.3f" % mcc) + "," + str("%.3f" % f1)

    def fp_str(self):
        output = ""
        for fp in self.false_pos:
            output += str(fp) + "\n"
        return output

    def fn_str(self):
        output = ""
        for fn in self.false_neg:
            output += str(fn) + "\n"
        return output
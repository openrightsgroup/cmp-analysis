from abc import ABCMeta, abstractmethod


class Filter:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_blocked_cats(self):
        pass

    @abstractmethod
    def str(self):
        pass

    @abstractmethod
    def block_cat(self, url_cat):
        pass


class NullFilter(Filter):
    # Checks if the category of the URL should be blocked, or not
    def block_cat(self, url_cat):
        block = False
        return block

    # Returns the blocked categories
    def get_blocked_cats(self):
        return self.cats

    def str(self):
        return "Null Filter: " + str(self.cats)

    def __init__(self):
        self.cats = []
        pass
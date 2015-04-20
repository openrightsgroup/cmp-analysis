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






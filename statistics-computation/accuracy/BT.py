from FilterClassifier import Filter


class BTNormalFilter(Filter):

    def __init__(self):
        # Add the DMOZ categories that should be blocked
        self.cats = []
        self.cats.append("Adult")
        self.cats.append("Computers/Hacking")

        self.cats.append("Recreation/Drugs")
        self.cats.append("Recreation/Food/Drink/Drinking")
        self.cats.append("Health/Specific Substances/Alcoholic Beverages")
        self.cats.append("Shopping/Tobacco")
        self.cats.append("Recreation/Tobacco")
        self.cats.append("Society/Relationships/Dating")
        self.cats.append("Society/Relationships/Cyber_Relationships")
        self.cats.append("Games/Online")


    # Checks if the category of the URL should be blocked, or not
    def block_cat(self, url_cat):
        block = False
        for cat in self.cats:
            if cat in url_cat:
                block = True
                break
        return block


    # Returns the blocked categories
    def get_blocked_cats(self):
        return self.cats


    def str(self):
        return "BT Normal with: " + str(self.cats)

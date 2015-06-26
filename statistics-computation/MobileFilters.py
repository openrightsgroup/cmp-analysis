from FilterClassifier import Filter


class EEFilter(Filter):
    def __init__(self):
        # Add the DMOZ categories that should be blocked
        self.cats = []
        self.cats.append("Adult")
        self.cats.append("Computers/Hacking")

        self.cats.append("Recreation/Drugs")

        self.cats.append("Recreation/Food/Drink/Drinking")
        self.cats.append("Recreation/Food/Drink/Mead")
        self.cats.append("Recreation/Food/Drink/Wine")
        self.cats.append("Recreation/Food/Drink/Beer")
        self.cats.append("Recreation/Food/Drink/Alcopops")
        self.cats.append("Recreation/Food/Drink/Cider")
        self.cats.append("Recreation/Food/Drink/Cocktails")
        self.cats.append("Recreation/Food/Drink/Liquor")
        self.cats.append("Recreation/Food/Drink/Sake")
        self.cats.append("Health/Specific Substances/Alcoholic Beverages")

        self.cats.append("Shopping/Tobacco")
        self.cats.append("Recreation/Tobacco")
        # self.cats.append("Society/Relationships/Dating")
        # self.cats.append("Society/Relationships/Cyber_Relationships")
        # self.cats.append("Regional/Europe/United Kingdom/Society_and_Culture/Gay,_Lesbian,_and_Bisexual/Relationships")

        # self.cats.append("Games")
        self.cats.append("Computers/Software/Internet/Clients/File_Sharing")
        # self.cats.append("Gambling")
        # self.cats.append("Computers/Internet/On_the_Web/Online_Communities/Social_Networking")
        # self.cats.append("Kids_and_Teens/People_and_Society/Online Communities")

        # add banned category keywords
        self.keywords = []
        self.keywords.append("Wine")
        self.keywords.append("Beer")
        self.keywords.append("Brewery")
        self.keywords.append("Breweries")

        # self.keywords.append("Relationships")

    # Checks if the category of the URL should be blocked, or not
    def block_cat(self, url_cat):
        block = False
        for cat in self.cats:
            # Altered string comparison method to check for substring contains at the start
            if url_cat.find(cat) is 0:
                block = True
                break

        for keyword in self.keywords:
            if keyword in url_cat:
                block = True
                break
        return block

    # Returns the blocked categories
    def get_blocked_cats(self):
        return self.cats

    def str(self):
        return "EE with: " + str(self.cats)


class O2Filter(Filter):
    def __init__(self):
        # Add the DMOZ categories that should be blocked
        self.cats = []
        self.cats.append("Adult")
        # self.cats.append("Computers/Hacking")

        # self.cats.append("Recreation/Drugs")
        # self.cats.append("Recreation/Food/Drink/Drinking")
        # self.cats.append("Health/Specific Substances/Alcoholic Beverages")
        # self.cats.append("Shopping/Tobacco")
        # self.cats.append("Recreation/Tobacco")
        # self.cats.append("Society/Relationships/Dating")
        # self.cats.append("Society/Relationships/Cyber_Relationships")
        # self.cats.append("Games")
        # self.cats.append("Computers/Software/Internet/Clients/File_Sharing")
        # self.cats.append("Gambling")
        # self.cats.append("Computers/Internet/On_the_Web/Online_Communities/Social_Networking")
        # self.cats.append("Kids_and_Teens/People_and_Society/Online Communities")

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
        return "O2 with: " + str(self.cats)


class ThreeFilter(Filter):
    def __init__(self):
        # Add the DMOZ categories that should be blocked
        self.cats = []
        self.cats.append("Adult")
        # self.cats.append("Computers/Hacking")

        # self.cats.append("Recreation/Drugs")
        # self.cats.append("Recreation/Food/Drink/Drinking")
        # self.cats.append("Health/Specific Substances/Alcoholic Beverages")
        # self.cats.append("Shopping/Tobacco")
        # self.cats.append("Recreation/Tobacco")
        # self.cats.append("Society/Relationships/Dating")
        # self.cats.append("Society/Relationships/Cyber_Relationships")
        # self.cats.append("Games")
        # self.cats.append("Computers/Software/Internet/Clients/File_Sharing")
        # self.cats.append("Gambling")
        # self.cats.append("Computers/Internet/On_the_Web/Online_Communities/Social_Networking")
        # self.cats.append("Kids_and_Teens/People_and_Society/Online Communities")

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
        return "Three with: " + str(self.cats)


class VirginMobileFilter(Filter):
    def __init__(self):
        # Add the DMOZ categories that should be blocked
        self.cats = []
        self.cats.append("Adult")
        # self.cats.append("Computers/Hacking")

        # self.cats.append("Recreation/Drugs")
        # self.cats.append("Recreation/Food/Drink/Drinking")
        # self.cats.append("Health/Specific Substances/Alcoholic Beverages")
        # self.cats.append("Shopping/Tobacco")
        # self.cats.append("Recreation/Tobacco")
        # self.cats.append("Society/Relationships/Dating")
        # self.cats.append("Society/Relationships/Cyber_Relationships")
        # self.cats.append("Games")
        # self.cats.append("Computers/Software/Internet/Clients/File_Sharing")
        # self.cats.append("Gambling")
        # self.cats.append("Computers/Internet/On_the_Web/Online_Communities/Social_Networking")
        # self.cats.append("Kids_and_Teens/People_and_Society/Online Communities")

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
        return "VirginMobile with: " + str(self.cats)

class VodafoneFilter(Filter):
    def __init__(self):
        # Add the DMOZ categories that should be blocked
        self.cats = []
        self.cats.append("Adult")
        # self.cats.append("Computers/Hacking")

        # self.cats.append("Recreation/Drugs")
        # self.cats.append("Recreation/Food/Drink/Drinking")
        # self.cats.append("Health/Specific Substances/Alcoholic Beverages")
        # self.cats.append("Shopping/Tobacco")
        # self.cats.append("Recreation/Tobacco")
        self.cats.append("Society/Relationships/Dating")
        self.cats.append("Society/Relationships/Cyber_Relationships")
        # self.cats.append("Games")
        # self.cats.append("Computers/Software/Internet/Clients/File_Sharing")
        self.cats.append("Gambling")
        # self.cats.append("Computers/Internet/On_the_Web/Online_Communities/Social_Networking")
        # self.cats.append("Kids_and_Teens/People_and_Society/Online Communities")

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
        return "VirginMobile with: " + str(self.cats)


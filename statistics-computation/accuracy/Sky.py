from FilterClassifier import Filter


class Sky_Filter(Filter):
    def __init__(self):
        # Add the DMOZ categories that should be blocked
        self.cats = []
        self.cats.append("Adult")
        self.cats.append("Computers/Hacking")

        self.cats.append("Computers/Security/Malicious_Software/Spyware_and_Adware")
        self.cats.append("Recreation/Drugs")
        self.cats.append("Society/Relationships/Dating")
        self.cats.append("Society/Relationships/Cyber_Relationships")
        self.cats.append("Computers/Internet/On_the_Web/Online_Communities/Social_Networking")
        self.cats.append("Kids_and_Teens/People_and_Society/Online Communities")
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



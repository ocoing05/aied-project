import requests

class WikiHelper:
    def __init__(self):
        # Session object allows one to persist certain parameters across requests.
        self.S = requests.Session()
        self.URL = "https://en.wikipedia.org/w/api.php"

    # Returns list of titles of all links from the given page
    def getLinkedPages(self, title):
        params = {
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "links",
            "pllimit": 500
        }

        linkedPages = []
        morePages = True
        while morePages: 
            res = self.S.get(url=self.URL, params=params)
            resJSON = res.json()

            pages = resJSON["query"]["pages"]

            for i, j in pages.items(): 
            # i = number representing the original page (key), j = the actual content containing everything (value)
                for k in j["links"]: # "links" is an attribute inside of j and contains the actual list of pages
                    if k["ns"] == 0: # ns = 0 are actual pages
                        linkedPages.append(k["title"])

            # if there are still more pages to load, we will call again from where we left off
            if (not "continue" in resJSON):
                morePages = False
            else:
                cont = resJSON["continue"]["plcontinue"] # used to get more pages
                params["plcontinue"] = cont

        return linkedPages

# example call
wh = WikiHelper()
pages = wh.getLinkedPages("Aristotle")
print(pages)

# NOTES : 
# i feel like there is a way to be neater about the code above ? but for now it works
# there are a LOT of links for each page and still not entirely sure if they're all right... they all seem related but can't find them all on actual pages
# maybe we need to filter down somehow from there..?
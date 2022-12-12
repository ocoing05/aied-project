import networkx as nx
import spacy
import re
import sense2vec

from FoxQueue import PriorityQueue
from wikinode import WikiNode 
from mediawiki import MediaWiki

# load nlp and add sense2vec multiword phrase vector pipe

class GraphTracker():

    def __init__(self, nlp) -> None:

        self.nlp = nlp # natural language processor 
        self.graph = nx.Graph() # graph of already read articles and edges between them represent from what link they were discovered
        self.fringe = PriorityQueue() # unopened WikiNodes adjacent to progressGraph, sorted by potential interest

    def updateGraph(self, node):
        '''Called by the student model update() method after a student reads a new article. 
        Adds node to graph.'''
        self.graph.add_node(node.title)
        if node.prevNode:
            self.graph.add_edge(node.title, node.prevNode)

    def alreadyExplored(self, title):
        if title in list(self.graph.nodes):
            return True
        else:
            return False

    def getFringe(self, numNodes) -> list:

        fringeList = []
        tempFringeQueue = copy.deepcopy(self.fringe) # needs to be copy not ref
        for x in range(numNodes):
            node = tempFringeQueue.delete()
            if node is not None:
                fringeList.append(node)

        return fringeList

    def shortenFringe(self, num) -> None:
        '''Deletes num nodes from the end of the queue.'''
        fringeItems = self.getFringe(self.fringe.size)
        keep = self.fringe.size - num # number of nodes to keep
        for i in range(self.fringe.size):
            if i > keep:
                self.fringe.removeValue(fringeItems[i])


class ExplorationTracker(GraphTracker):

    def __init__(self, nlp, initialInterests) -> None:

        super().__init__(nlp)
        
        for i in initialInterests:
            try:
                self.fringe.insert(WikiNode(i), 0.0) 
            except: # don't add this interest if MediaWiki can't identify the correct article to use
                continue

    def updateFringe(self, node, studentInterests):
        '''Called by the student model update() method after a student reads a new article.
        Updates fringe with linked articles from node they just read. Ranked based on student interests.'''
        if self.fringe.size > 30:
            self.shortenFringe(self.fringe.size / 2) # cut fringe size in half
        linkedPageTitles = node.getLinkedPageTitles()
        kwTokens = self.nlp(node.getKeyWords())._.s2v_phrases
        sortedLinks = {} # linkedPageTitles (keys) sorted by their average s2v similarity to all node keywords

        for link in linkedPageTitles:
            linkDoc = self.nlp(link)
            if len(linkDoc) == 1: 
                for kwToken in kwTokens:
                    sim = 0

        # for pg in set(lp) & set(kw): # words that exist as both linked pages and key words of the node
        # TODO: instead of using the set of both ^ like above, maybe use keywords to rank linked pages but don't disregard completely?
        # maybe something like that ^ but use similarity between kw and lp? prioritize the ones where similarity is greatest
        for pg in linkedPageTitles:
            # print(pg)
            if self.alreadyExplored(pg): # that article was already read
                continue
            pg = re.sub(r'\W+', ' ', pg) # replaces all non-alphanumeric/underscore characters w space

            # Shouldn't need to split page title with sense2vec loaded
            # if len(pg.strip().split(" ")) > 1 or not pg.isalpha(): # more than 1-gram phrases and non-letters will mess up spacy's analysis
            #    # TODO: logic for n-gram pages?
            #    # print("n-gram")
            #    continue

            priority = self.getPriority(pg, studentInterests)
            if priority == -1: 
                continue # ignore if does not exist in spacy nlp model
            # print(priority)
            try: 
                node = WikiNode(pg, node.title)
            except: # ignore if MediaWiki can't identify which article should be used for this title
                continue
            print(node.title, priority)
            self.fringe.insert(node, priority)

    def getPriority(self, nodeTitle, studentInterests):

        totalSim = 0
        nodeDoc = self.nlp(nodeTitle)

        for interest in list(studentInterests.keys()):
            timesUpdated, interestVal = studentInterests[interest]
            intDoc = self.nlp(interest)
            if len(intDoc) != 1 or len(nodeDoc) != 1:
                totalSim += (nodeDoc._.s2vphrases[0].s2v_similarity(intDoc._.s2v_phrases[0]) + 1) * 0.5 * interestVal
            else:
                totalSim += (nodeDoc.similarity(intDoc) + 1) * 0.5 * interestVal
        
        priority = totalSim/len(studentInterests)
        return 1 - priority

        # words = nodeTitle
        # for interest in list(studentInterests.keys()):
        #     words = words + ' ' + interest
        # # print(words)
        # tokens = nlp(words)
        # priority = 0
        # interestTokens = tokens[1:]
        # # print(tokens[0])
        # if tokens[0].has_vector: 
        #     for i in interestTokens:
        #         #if i.has_vector: # TODO: should always be true ... delete later
        #         x = studentInterests[i.text]
        #         interestVal = x[1]
        #         # print(i)
        #         # print("similarity", tokens[0].similarity(i))
        #         # print("interest", interestVal)
        #         priority += (tokens[0].similarity(i)+1)*0.5 * interestVal # similarity() => -1 to 1
        # else:
        #     return -1 # nodeTitle does not exist in nlp model, can not be analyzed
        # return (1 - priority / len(interestTokens))

class DomainTracker(GraphTracker):

    def __init__(self, nlp, wiki, initialInterests) -> None:

        super().__init__(nlp)

        self.wikipedia = wiki
        self.initGraph(initialInterests)
        

    def initGraph(self, initialInterests):

        for i in initialInterests:
            node = WikiNode(i, self.nlp, self.wikipedia, domainNode=True)
            self.updateGraph(node)
            catTree = self.wikipedia.categorytree(node.getTitle, 2)
            catDict = catTree['category']
            subCatsDict = catDict['sub-categories']
            for subCat in subCatsDict:
                subCatNode = WikiNode(subCat, self.nlp, self.wikipedia, prevNode=node, domainNode=True)
                self.updateGraph(subCatNode)
                # subCatDict = catTree['category']['sub-categories'][subCat]
                # node.getKeyWords()
            parentCatsList = catDict['parent-categories']
            for parentCat in parentCatsList:
                parentNode = WikiNode(parentCat, self.nlp, self.wikipedia, domainNode=True)
                parentDoc = self.nlp(parentCat)
                for kw in node.getKeyWords():
                    pass


if __name__ == "__main__":

    test = ExplorationTracker()
    print(test.getPriority(WikiNode('Dogs'), {'cats': (1,1), 'dinosaurs': (1,1)})) # highest priority
    print(test.getPriority(WikiNode('Dogs'), {'cats': (1,0.5), 'dinosaurs': (1,1)})) # smaller priority
    print(test.getPriority(WikiNode('dogs'), {'fashion': (1,1), 'winter': (1,1)})) # low priority
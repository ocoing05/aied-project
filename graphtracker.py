"""
COMP 484 - Introduction to Artificial Intelligence, Fall 2022
Term Project - AI in Education: FreeLearner, presented 12/16/2022
Ingrid O'Connor and Quentin Harrington

This file: graphtracker.py
    This file contains a class GraphTracker, a parent (base) class for two separate trackers:

        1. ExplorationTracker --> created by Student Model, holds two main objects:
            a. graph --> networkx.Graph()
                --> non-hierarchical graph of explored nodes, and edges representing students path
            b. fringe --> PriorityQueue() --> from FoxQueue.py by Susan Fox    
                --> Priority queue of links to nodes in the explored graph, sorted by expected interest 
                based on a similarity analysis to studentInterests

        2. DomainTracker --> created by Domain Model, holds one object:
            a. graph --> networkx.Graph()
                --> heirarchical category graph encompassing all parent, sibling, and children nodes of
                explored nodes
                
"""

import networkx as nx
import spacy
import re
from sense2vec import Sense2Vec
import copy

from FoxQueue import PriorityQueue
from wikinode import WikiNode 
from mediawiki import MediaWiki

class GraphTracker():

    def __init__(self, nlp, wiki) -> None:

        self.graph = nx.Graph() # graph of already read articles and edges between them represent from what link they were discovered
        self.nlp = nlp # natural language processor 
        self.wiki = wiki # MediaWiki() wikipedia api object

        # Check if sense2vec is in pipeline
        self.hasS2V = True
        try:
            nlp("test")._.in_s2v
        except AttributeError:
            self.hasS2V = False

    def alreadyExplored(self, title):
        if title in list(self.graph.nodes):
            return True
        else:
            return False

    def updateGraph(self, node):
        '''Called by the student model update() method after a student reads a new article. 
        Adds node to graph.'''
        self.graph.add_node(node.title)
        if node.prevNode:
            self.graph.add_edge(node.title, node.prevNode)

class ExplorationTracker(GraphTracker):

    def __init__(self, nlp, wiki, initialInterests) -> None:

        super().__init__(nlp, wiki)
        self.fringe = PriorityQueue() # unopened WikiNodes adjacent to progressGraph, sorted by potential interest

        for i in initialInterests:
            try:
                self.fringe.insert(WikiNode(i, nlp, wiki), 0.0) 
            except: # don't add this interest if MediaWiki can't identify the correct article to use
                continue

    def updateFringe(self, node, studentInterests, mvp):
        '''Called by the student model update() method after a student reads a new article.
        Updates fringe with linked articles from node they just read. Ranked based on student interests.'''
        # if self.fringe.size > 30: # to reimplement, would need to use new deleteFromFringe() function
        #     self.shortenFringe(self.fringe.size / 2) # cut fringe size in half
        linkedPageTitles = node.getLinkedPageTitles() # links are sorted by similarity to node keywords
        self.deleteFromFringe(node.title)
        # if self.fringe.contains(node):
        #     print("removing node")
        #     # self.fringe.removeValue(node)
        #     print("done")
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
            if (mvp):
                if len(pg.strip().split(" ")) > 1 or not pg.isalpha(): # more than 1-gram phrases and non-letters will mess up spacy's analysis
                    continue
                priority = self.getPriorityMVP(pg,studentInterests)
            else:
                priority = self.getPriority(pg, studentInterests)
            if priority == -1: 
                continue # ignore if does not exist in spacy nlp model
            # print(priority)
            # print(pg, priority)
            self.fringe.insert(WikiNode(pg, self.nlp, self.wiki, prevNode = node), priority)

    def getFringe(self, numNodes=None) -> list:
        """Returns list of fringe nodes, numNodes long, or all if numNodes is not provided."""
        if not numNodes:
            numNodes = self.fringe.getSize()
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

    def getPriority(self, nodeTitle, studentInterests) -> float:
        """Param:
                nodeTitle (string)
                studentInterests (dict{string, (int, float)})
            Returns:
                priority (float): Avg Similarity (0-high, 1-low) of node to studentInterests."""
        totalSim = 0
        nodeDoc = self.nlp(nodeTitle)

        for interest in list(studentInterests.keys()):
            timesUpdated, interestVal = studentInterests[interest]
            intDoc = self.nlp(interest)
            if not intDoc.has_vector:
                continue
            if self.hasS2V and len(intDoc) == 1 and len(nodeDoc) == 1:
                totalSim += (nodeDoc._.s2v_phrases[0].s2v_similarity(intDoc._.s2v_phrases[0]) + 1) * 0.5 * interestVal
            else:
                totalSim += (nodeDoc.similarity(intDoc) + 1) * 0.5 * interestVal
        
        return 1 - totalSim/len(studentInterests)

    def getPriorityMVP(self, nodeTitle, studentInterests):
        words = nodeTitle
        for interest in list(studentInterests.keys()):
            words = words + ' ' + interest
        tokens = self.nlp(words)
        priority = 0
        interestTokens = tokens[1:]
        if tokens[0].has_vector: 
            for i in interestTokens:
                x = studentInterests[i.text]
                interestVal = x[1]
                priority += (tokens[0].similarity(i)+1)*0.5 * interestVal # similarity() => -1 to 1
        else:
            return -1 # nodeTitle does not exist in nlp model, can not be analyzed
        return (1 - priority / len(interestTokens))   

    def updatePriorities(self, studentInterests):
        '''Updates priority values of existing fringe nodes based on updated student interests.'''
        # TODO: still need to test this once logic is working (mainly to make sure each is what i think it is)
        # should be called in updateFringe() after shortenFringe()
        tempFringe = self.fringe
        for node in tempFringe:
            #print(each) # TODO: delete after testing
            
            newPriority = self.getPriority(node.getTitle(), studentInterests)
            self.fringe.update(node, newPriority)

    def deleteFromFringe(self, title):
        success = False
        for [v,p] in self.fringe.qData:
            if v.title == title:
                self.fringe.removeValue(v)
                success = True
        return success

class DomainTracker(GraphTracker):

    def __init__(self, nlp, wiki, initialInterests) -> None:

        super().__init__(nlp, wiki)
        self.initGraph(initialInterests)
        
    def initGraph(self, initialInterests):
        for i in initialInterests:
            node = WikiNode(i, self.nlp, self.wiki, domainNode=True)
            self.updateGraph(node)
            catTree = self.wiki.categorytree(node.getTitle, 1)
            catDict = catTree['category']
            subCatsDict = catDict['sub-categories']
            for subCat in subCatsDict:
                subCatNode = WikiNode(subCat, self.nlp, self.wiki, prevNode=node, domainNode=True)
                self.updateGraph(subCatNode)
                # subCatDict = catTree['category']['sub-categories'][subCat]
                # node.getKeyWords()
            parentCatsList = catDict['parent-categories']
            sortedParentCats = {}
            for parentCat in parentCatsList:
                parentNode = WikiNode(parentCat, self.nlp, self.wiki, domainNode=True)
                parentDoc = self.nlp(parentCat)
                totalSim = 0
                for kw in node.getKeyWords():
                    kwDoc = self.nlp(kw)
                    if self.hasS2V and len(parentDoc) == 1 and len(kwDoc) == 1:
                        totalSim += parentDoc._.s2v_phrases[0]._.s2v_similarity(kwDoc._.s2v_phrases[0])
                    else:
                        totalSim += parentDoc.similarity(kwDoc)
                sortedParentCats[parentNode] = ( totalSim / len(node.getKeyWords()))
            parentNode = dict(sorted(sortedParentCats.items(), key=lambda item:item[0], reverse=True)).items()[0][0]
            node.setPrevNode(parentNode)

    def updateGraph(self, node):
        self.graph.add_node(node.title)
        if node.prevNode:
            self.graph.add_edge(node.title, node.prevNode)

if __name__ == "__main__":

    test = ExplorationTracker()
    print(test.getPriority(WikiNode('Dogs'), {'cats': (1,1), 'dinosaurs': (1,1)})) # highest priority
    print(test.getPriority(WikiNode('Dogs'), {'cats': (1,0.5), 'dinosaurs': (1,1)})) # smaller priority
    print(test.getPriority(WikiNode('dogs'), {'fashion': (1,1), 'winter': (1,1)})) # low priority
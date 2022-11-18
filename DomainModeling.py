"""
Represents a node in the graph of Wikipedia articles.
Includes title, url, summary, categories, linked pages, and content of page.
Uses NLP on content to determine key words, which are used by recommender system.
"""

import wikipedia
import yake
import networkx as nx
from FoxQueue import PriorityQueue
import WikiNode
from mediawiki import MediaWiki

# from owlready2 import *



if __name__ == "__main__":

    wikipedia = MediaWiki() 

    # onto = get_ontology("file:///Users/quentinharrington/Desktop/COMP484/aied-project/wiki_cats_full_non_cyclic_v1.owl")
    # onto.load()
    # ontoList = list(onto.classes())
    # print(ontoList)


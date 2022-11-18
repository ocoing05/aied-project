

import yake
import networkx as nx
from FoxQueue import PriorityQueue
from wikinode import WikiNode
from mediawiki import MediaWiki
from owlready2 import *

class DomainModel:
    
    def __init__(self) -> None:
        pass

if __name__ == "__main__":

    wikipedia = MediaWiki() 

    onto = get_ontology("file:///Users/quentinharrington/Desktop/COMP484/aied-project/wiki_cats_full_non_cyclic_v1.owl")
    onto.load()
    ontoList = list(onto.classes())
    print(ontoList)


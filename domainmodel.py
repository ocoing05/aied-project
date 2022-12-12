

import yake
from explorationtracker import DomainTracker
from FoxQueue import PriorityQueue 
from wikinode import WikiNode  
from mediawiki import MediaWiki
from owlready2 import *

class DomainModel:
    
    def __init__(self, nlp, wiki, initialInterests) -> None:

        self.wikipedia = wiki
        self.domainTracker = DomainTracker(nlp, wiki, initialInterests)

    

if __name__ == "__main__":

    # 1 Function Iterate(A) :
        # 2 Find page id pd, title t, page namespace pn of page A;
        # 3 if pn == 0 then
            # 4 Declare title t as an entity e;
            # 5 Find categories (c ∈ C) of entity e;
            # 6 foreach c ∈ C do
                # 7 Declare category c as a rdf:type (class);
                # 8 Create facts: e rdf:type c;
                # 9 Find the pages (p ∈ P) which are entity of category c;
                # 10 foreach p ∈ P do
                    # 11 Iterate(p) ;
                # 12 end
            # 13 end
        # 14 end
        # 15 else if pn == 14 then
            # 16 Declare title t a category (class) c;
            # 17 Find all sub-categories (sc v c) of category c;
            # 18 foreach sc ∈ C do
                # 19 Create relation: sc subClassOf c;
                # 20 Iterate(sc);
            # 21 end
        # 22 end
    # 23 end  

    wikipedia = MediaWiki() 

    onto = get_ontology("file:///Users/quentinharrington/Desktop/COMP484/aied-project/wiki_cats_full_non_cyclic_v1.owl")
    onto.load()
    ontoList = list(onto.classes())
    print(ontoList)


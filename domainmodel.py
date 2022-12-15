"""
COMP 484 - Introduction to Artificial Intelligence, Fall 2022
Term Project - AI in Education: FreeLearner, presented 12/16/2022
Ingrid O'Connor and Quentin Harrington

This file: domainmodel.py
    This file builds the student-specific domain graph, tracking
    student explored nodes within wikipedia category hierarchy.
    Guides article recommendations towards unexplored categories 
    to bridge and expand student interests.
"""

from graphtracker import DomainTracker 

class DomainModel:
    
    def __init__(self, nlp, wiki, initialInterests) -> None:

        self.wiki = wiki
        self.nlp = nlp
        self.domainTracker = DomainTracker(nlp, wiki, initialInterests)

        print("domain initiated.")

    def updateModel(self, node):
        self.domainTracker.updateGraph(node)

if __name__ == "__main__":
    pass

    # Pseudocode for building wikipedia noncyclic domain knowledge graph
    # ------------------------------------------------------------------
    # 1 Function Iterate(A) :
        # 2 Find page id pd, title t, page namespace pn of page A;
        # 3 if pn == 0 thencscs
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


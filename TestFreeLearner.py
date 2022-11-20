from studentmodel import StudentModel
from wikinode import WikiNode
from progressgraph import ProgressGraph

# *** MOCK DATA ***

# create students
student1 = StudentModel("Ingrid", "ingrid", "12345", "ioconnor@macalester.edu", ["Disney", "Dinosaurs", "Volcanoes"])

# create articles
article1 = WikiNode("Disney")
article2 = WikiNode("Penguins")
article3 = WikiNode("Volcanoes")
article4 = WikiNode("Egyptian pyramids")
article5 = WikiNode("Wolfgang Amadeus Mozart")
# when creating new nodes, if the node was added from the fringe by being linked from a previous article it would be created like this:
article6 = WikiNode("Mickey Mouse", "Disney")

# *** TEST DEFINITIONS ***

# *** WikiNode ***
def testWikiNodes():
    testSections()
    testSummary()
    testPrevNode()
    testKeyWords()

def testSections():
    assert 'History' in article1.getSectionTitles()
    assert 'Legacy' in article1.getSectionTitles()
    assert article1.getSection('History') == 'Empty section'
    assert "Bob Iger introduced D23 in 2009" in article1.getSection("2005–2020: Bob Iger's leadership, expansion, and Disney+")

def testSummary():
    # print(article4.getSummary(4))
    assert "After becoming a major success by the early 1940s" in article1.getSummary(4)

def testPrevNode():
    assert article1.prevNode == None
    assert article6.prevNode == "Disney"

def testKeyWords():
    kw = article1.getKeyWords()
    assert 'film' in kw
    assert 'Mickey Mouse' in kw
    # print("DISNEY KEY WORDS: ", kw)

# *** StudentModel ***
def testStudentModel():
    pass
    # TODO: student creation, fringe updates, student interest updates, session stats

# *** ExplorationTracker ***
def testExplorationTracker():
    testGraph()
    testFringe()

def testGraph():
    student1.updateModel(article1)
    assert len(list(student1.progressGraph.graph.nodes)) == 1
    # TODO : test that fringe was updated with linked nodes in prioritized order ?
    # and test that the student interests were updated correctly
    # student1 reads article6
    student1.updateModel(article6)
    assert len(list(student1.progressGraph.graph.nodes)) == 2
    assert len(student1.progressGraph.graph.edges) == 1

def testFringe():
    testPriorityRankings()
    testUpdateFringe()

def testPriorityRankings():
    et = ProgressGraph()
    priority1 = et.getPriority(WikiNode('Science'), {'math': (1,1), 'physics': (1,1)})
    priority2 = et.getPriority(WikiNode('Science'), {'dogs': (1,1), 'Disney': (1,1)})
    priority3 = et.getPriority(WikiNode('Science'), {'math': (1,0.5), 'physics': (1,0.5)})
    priority4 = et.getPriority(WikiNode('Science'), {'math': (1,0.5), 'physics': (1,0.8)})
    assert priority1 > priority2
    assert priority1 > priority3
    assert priority4 > priority3
    
def testUpdateFringe():
    pass

# *** Recommender ***
def testRecommender():
    pass

# *** UI ***
def testUI():
    pass

# *** RUN TESTS ***

if __name__ == "__main__":
    # testWikiNodes()
    # testStudentModel()
    testExplorationTracker()
    # testRecommender()
    # testUI()
    print("All tests pass.")
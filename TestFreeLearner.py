from studentmodel import StudentModel  
from wikinode import WikiNode 
from explorationtracker import ExplorationTracker
from mediawiki import MediaWiki
import spacy
from sense2vec import Sense2Vec, Sense2VecComponent
import yake

# *** MOCK DATA ***

# Domain and NLP objects
    # create Spacy natural language processor, 
    # add sense2vec pipe for multiword phrase similarity accuracy
nlp = spacy.load('en_core_web_lg')
s2v = nlp.add_pipe("sense2vec")
s2v.from_disk("/Users/quentinharrington/Desktop/COMP484/aied-project/s2v_reddit_2019_lg")
    # create MediaWiki() object and setting user_agent following mediawiki etiquette
wiki = MediaWiki()
wiki.user_agent = 'macalester_comp484_quentin_ingrid_AI_capstone_qharring@macalester.edu' # MediaWiki etiquette

# create students
student1 = StudentModel("Ingrid", 
                        ["Disney", "Dinosaurs", "Volcanoes"],
                        nlp,
                        username="ingrid", 
                        password="12345", 
                        email="ioconnor@macalester.edu")
studentQ = StudentModel("Quentin Harrington", 
                        ["Computers", "Sustainability", "Ecology", "Soccer", "Urbanism", "Architecture", "Plants", "Psychology"],
                        nlp)
student3 = StudentModel("student3", 
                        ["Rainbows", "Dragons", "Hippopotamus", "Japan", "Fruit", "Baking", "Photography", "Hiking", "Kayaking"],  
                        nlp)


# create articles
article1 = WikiNode("Disney", nlp, wiki)
article2 = WikiNode("Penguins", nlp, wiki)
article3 = WikiNode("Volcanoes", nlp, wiki)
article4 = WikiNode("Egyptian pyramids", nlp, wiki)
article5 = WikiNode("Wolfgang Amadeus Mozart", nlp, wiki)
# when creating new nodes, if the node was added from the fringe by being linked from a previous article it would be created like this:
article6 = WikiNode("Mickey Mouse", nlp, wiki, prevNode=article1)

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
    testStudentCreation()
    # TODO: student creation, fringe updates, student interest updates, session stats

def testStudentCreation():
    student2 = StudentModel("test", ["Dogs", "Dinosaurs", "Volcanoes", "Disney"], nlp)
    assert student2.getStudentName() == 'test'
    assert 'Dogs' in student2.getInterestKeywords()
    assert 'Volcanoes' in student2.getInterestKeywords()
    # TODO : test fringe creation

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
    et = ExplorationTracker([])
    priority1 = et.getPriority('Science', {'math': (1,1), 'physics': (1,1)})
    priority2 = et.getPriority('Science', {'dogs': (1,1), 'Disney': (1,1)})
    priority3 = et.getPriority('Science', {'math': (1,0.5), 'physics': (1,0.5)})
    priority4 = et.getPriority('Science', {'math': (1,0.5), 'physics': (1,0.8)})
    assert priority1 < priority2
    assert priority1 < priority3
    assert priority4 < priority3
    priority5 = et.getPriority('ndlsajncjxdsfjvdk', {'math':(1,1)})
    assert priority5 == -1
    
def testUpdateFringe():
    pass

def testShortenFringe():
    pass

def testUpdatePriorities():
    student1.explorationTracker.updatePriorities(student1.getInterestKeywords())

# *** Recommender ***
def testRecommender():
    pass

# *** UI ***
def testUI():
    pass

# *** Spacy and sense2vec ***
def testSpacy():

    # doc = s2vNLP("A sentence about natural language processing.")
    # assert doc[3:6].text == "natural language processing"
    # freq = doc[3:6]._.s2v_freq
    # vector = doc[3:6]._.s2v_vec
    # most_similar = doc[3:6]._.s2v_most_similar(3)
    # print(freq)
    # print(most_similar)

    # doc = s2vNLP("A sentence about Facebook and Google.")
    # for ent in doc.ents:
    #     assert ent._.in_s2v
    #     most_similar = ent._.s2v_most_similar(3)
    # print(most_similar
    pass

def tests2v():
    pass

def testMediaWiki():
    """Testing:
        1. For each articleTitle:
            a. Initialize wikiNode
            b. Initialize spacy doc for articleTitle
            c. Initialize spacy doc for page summary
            d. Build dictionary of links and their similarity to summary, normalized to title <-> summary similarity
                1. 
    """
    # debug variable, prints debugging statements if True
    debug = True

    # Function for debugging
    def _debugFunc(debugPrintDict, key):
        print(debugPrintDict.get(key)) if debug else debugPrintDict
        return debugPrintDict

    # Dictionary of ordered debugging statements
    debugDict = {1:("loading MediaWiki object..."),
                      2:("loaded as wikipedia."),
                      3:("loading spacy NLP..."),
                      4:("attaching sense2vec pipe..."),
                      5:("loaded s2vNLP. Beginning article analysis loop."),
                      6:("building WikiNode object..."),
                      7:("WikiNode built. creating s2vNLP doc objects for WikiNode title, summary, and links...")}

    debugDict = _debugFunc(debugDict, 1) # if debug variable at top of file is True, print debugging string

    # wikipedia = MediaWiki()

    debugDict = _debugFunc(debugDict, 2) # 2

    filePath = input("\nCopy in the full path to your vector data folder. \
                      \ni.e. '/Users/quentinharrington/Desktop/COMP484/aied-project/s2v_reddit_2019_lg' \
                      \n    --> ")
    # create natural language processing elements
    # controlNLP = spacy.load("en_core_web_lg")

    debugDict = _debugFunc(debugDict, 3) # 3

    s2vNLP = spacy.load("en_core_web_lg")

    debugDict = _debugFunc(debugDict, 4) # 4

    s2v = s2vNLP.add_pipe("sense2vec")
    s2v.from_disk(filePath)

    debugDict = _debugFunc(debugDict, 5) # 5

    randomArticles = {} # Dictionary of random article titles (keys) and their links sorted by (values)
    for articleTitle in ["FIFA World Cup", "internet", "United States Department of Defense", "urban planning"]:
        print("======================")
        print("Title: " + articleTitle)

        debugDict = _debugFunc(debugDict, 6) # 6

        wikiNode = WikiNode(articleTitle)

        debugDict = _debugFunc(debugDict, 7) # 7

        titleDoc = s2vNLP(articleTitle)
        summaryDoc = s2vNLP(wikiNode.getSummary())
        
        print("title <-> summary similarity: ", titleDoc.similarity(summaryDoc))
        
        # for link in wikiNode.getLinkedPageTitles:
        #     linkDoc = s2vNLP(link)
        #     if len(linkDoc) == 1: # This means the full linked page title has a vector in the sense2vec pipe, usable for similarity
        #         linkToken = linkDoc._.s2v_phrases
        #         linkSimDict[linkToken] = linkToken.
        # linksDoc = 
        # linkSimDict = {} 
        # for link in linksDoc:
            
        # for link in links:
        #     if
        #     linkDoc = s2vNLP(link)
        # UAWords = []
        # for token in doc:
        #     if token.is_alpha and not token.is_oov and not token.is_stop and token.text not in UAWords:
        #         UAWords.append(token.text)
        # print(UAWords)
        # print("======================")

        # links = wikiNode.getLinkedPageTitles
        # links.sort(key=_sortFunc)
        # randomArticles[wikiNode] = links

        # titleToken = s2vNLP(articleTitle)._.s2v_phrases
        # if len(titleToken) != 1:
        #     break
        # print(titleToken)

        # summaryTokens_withDup = s2vNLP(summary)._.s2v_phrases
        # summaryTokens = []
        # for token in summaryTokens_withDup:
        #     if token in summaryTokens:
        #         continue
        #     else:
        #         summaryTokens.append(token)
        

        # print(summaryTokens)

# *** RUN TESTS ***

if __name__ == "__main__":

    testWikiNodes()
    testStudentModel()
    testExplorationTracker()
    testRecommender()
    testUI()
    testUpdatePriorities()
    print("All tests pass.")
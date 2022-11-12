import networkx as nx

from WikiNode import WikiNode

def updateGraph(studentGraph, node):
    if not studentGraph:
        studentGraph = nx.Graph()
    # update explored graph
    studentGraph.add_node(node.title)
    if node.prevNode:
        studentGraph.add_edge(node.title, node.prevNode)
    # update fringe queue
    # something like the lines below, but ranked based on interests / NLP / key words ?
    # for pg in node.linkedPages:
        # studentFringe.add(WikiNode(pg, node.title))
    # update student interests ?

# NOTES
# add in time/other stats somehow
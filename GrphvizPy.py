import graphviz

from graphviz import Digraph

dot = Digraph()
dot.node('A', 'Apple')
dot.node('B', 'Banana')
dot.edge('A', 'B')
dot.render('test-output/graph.pdf', view=True)
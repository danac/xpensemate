import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab

G1 = nx.DiGraph()
G2 = nx.DiGraph()

for G in [G1, G2]: 
    G.add_node('A', pos=(0.55,0.5))
    G.add_node('B', pos=(0.95,0.6))
    G.add_node('C', pos=(0,0.7))
    G.add_node('D', pos=(0.9,1.2))
    G.add_node('E', pos=(0.35,1.1))

G1.add_edges_from([('A', 'B')], weight=1)
G1.add_edges_from([('A', 'C')], weight=2)
G1.add_edges_from([('D', 'B')], weight=1.5)
G1.add_edges_from([('D', 'C')], weight=5)
G1.add_edges_from([('A', 'D')], weight=1)
G1.add_edges_from([('C', 'B')], weight=1.5)
G1.add_edges_from([('E', 'C')], weight=1)

G2.add_edges_from([('A', 'B')], weight=4)
G2.add_edges_from([('E', 'C')], weight=1)
G2.add_edges_from([('D', 'C')], weight=5.5)

names = ["full", "simple"]
i=0
for G in [G1, G2]:
    f=plt.figure() 
    edge_labels=dict([((u,v,),d['weight'])
                     for u,v,d in G.edges(data=True)])
                     
    #red_edges = [('C','D'),('D','A')]
    edge_colors = ['black' for edge in G.edges()] #['black' if not edge in red_edges else 'red' for edge in G.edges()]

    pos=nx.spring_layout(G)
    pos=nx.get_node_attributes(G,'pos')
    # Draw nodes
    nx.draw_networkx_nodes(G,pos,node_size=700, node_color='orange')
     
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels, font_size=16)
    nx.draw_networkx_edges(G,pos,edgelist=G.edges(data=True), edge_color='k')
    nx.draw_networkx_labels(G,pos,font_size=16,font_family='sans-serif')
    #nx.draw(G,pos, node_color = 'orange', node_size=1500,edge_color=edge_colors,edge_cmap=plt.cm.Reds)
    plt.axis('off')
    plt.savefig("../static/debt_graph_"+names[i]+".png", format='png', transparent=True)
    i+=1
pylab.show()

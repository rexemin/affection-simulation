"""
This module uses graph algorithms to assess community structure
and other things.

Author: Ivan A. Moreno Soto
Last updated: 27/March/2018
"""

#-----------------------------------------------------------#

import igraph

#-----------------------------------------------------------#

def getCommunities(graph, algorithm = 'between'):
    """
    Gets the community structure of a given network.

    @param graph: igraph Graph object to be analyzed.
    @param algorithm: Algorithm to be used. Options are:
                      * 'between': Edge betweenness
                      * 'map': Map of random walks
                      * 'label': Labels propagation
    """
    if algorithm == 'between':
        dendrogram = graph.community_edge_betweenness(directed = False)
        clusters = dendrogram.as_clustering()
    elif algorithm == 'label':
        clusters = graph.community_label_propagation()
    elif algorithm == 'map':
        clusters = graph.community_infomap()
    else:
        raise ValueError("Invalid option!")

    return clusters.subgraphs()

#-----------------------------------------------------------#

###### EOF: analysis.py #####################################

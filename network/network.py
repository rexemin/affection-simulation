"""
This module simulates an affection social network.

Author: Ivan A. Moreno Soto
Last updated: 17/March/2018

TODO List:
- Plot network.
- Compute relationships that stay and that get broken up.
- Recompute formation of relationships.
- Plot network.
"""

############################################################

from random import uniform
from numpy import tanh
from math import sqrt

import igraph

import people

############################################################

class Network:
    """
    This class defines a container for all the data needed in
    order to simulate a social network.
    """

    def __init__(self, society):
        """
        Creates all the data needed to compute the simulation.

        @param society: List of People.
        """
        self.people = society

        self.singles = [ident for ident in range(len(society))]
        self.in_relation = [] # People in relationships.

        self.network = igraph.Graph()
        self.network.add_vertices(len(self.people))
        for (person, i) in zip(self.people, range(len(self.people))):
            self.network.vs[i]['info'] = person

    def __str__(self):
        """
        Returns a string representation of the data contained
        in this Network.
        """
        return ''.join('Network with ' + str(len(self.people)) + ' people.\n'
                      + str(len(self.singles)) + ' are single.\n'
                      + str(len(self.in_relation)) + ' are in relationships.\n'
                      + str(self.network))

############################################################

def normalize(v):
    """
    Returns the normalized vector of v.

    @param v: An iterable object of numbers.
    """
    norm = sqrt( sum( [x**2 for x in v] ) )
    return [x/norm for x in v]

############################################################

def dist(a, b):
    """
    Computes the distance between two Persons. Automatically
    normalizes the vector of each Person.

    @param a: A Person object.
    @param b: A Person object.
    """
    vec_a = normalize(people.attrib2vec(a))
    vec_b = normalize(people.attrib2vec(b))

    distance = sqrt( sum( [(at_a - at_b)**2 for at_a, at_b in zip(vec_a, vec_b)] ) )
    return distance

############################################################

def computeRomanticRelationships(network):
    """
    Computes what relationships are made from the pool of
    single people of the network.

    @param network: Network where the relationships will be computed.
    """
    for person in network.singles:
        for pos_partner in network.singles[network.singles.index(person)+1:]:
            if person not in network.in_relation and pos_partner not in network.in_relation and dist(network.people[person], network.people[pos_partner]) <= uniform(0, 0.3):
                network.in_relation.append(person)
                network.in_relation.append(pos_partner)
                network.network.add_edges([(person, pos_partner)])
                break

    # Before returning, we update the singles' list.
    for person in network.in_relation:
        if person in network.singles:
            del network.singles[network.singles.index(person)]

############################################################

def computeBreakups():
    """
    """
    pass

############################################################

if __name__ == "__main__":
    """
    Tests the things defines in this module.
    """
    society = people.createPopulation('./names.txt', 100)
    network = Network(society)
    print(network)

    computeRomanticRelationships(network)
    print(network)

    #for p in network.people:
    #    print(p)

###### EOF: network.py #####################################

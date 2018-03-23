"""
This module simulates an affection social network.

Author: Ivan A. Moreno Soto
Last updated: 21/March/2018

TODO List:
- Plot network.
- Compute relationships that stay and that get broken up.
- Recompute formation of relationships.
- Plot network.
"""

############################################################

import numpy as np

import igraph
import plotly.plotly as py
from plotly.graph_objs import *

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
                      + str(2*len(self.in_relation)) + ' are in relationships.\n'
                      + str(self.network))

############################################################

def computeVecMagnitude(v):
    """
    Returns the magnitude of a vector v.

    @param v: Iterable object.
    """
    return np.sqrt( sum( np.power(v, [2 for x in v]) ) )

############################################################

def computeDotProduct(v, u):
    """
    Returns the dot product of two vectors v and u.

    @param v: Iterable object.
    @param u: Iterable object.
    """
    return sum( [x * y for (x, y) in zip(v, u)] )

############################################################

def computeAngleBtwnPeople(a, b):
    """
    Returns the angle between two people's attributes vector.

    @param a: Person object.
    @param b: Person object.
    """
    va = people.attrib2vec(a)
    vb = people.attrib2vec(b)

    return np.arccos( computeDotProduct(va, vb) /
                      (computeVecMagnitude(va) * computeVecMagnitude(vb)) )

############################################################

def alreadyInRelation(pos_partner, in_relation):
    """
    Returns wheter or not the possible partner is already in
    a relationship.

    @param pos_partner: Index of a possible partner.
    @param in_relation: Set of current couples in a network.
    """
    for couple in in_relation:
        if pos_partner in couple:
            return True

    return False

############################################################

def computeRomanticRelationships(network):
    """
    Computes what relationships are made from the pool of
    single people of the network.

    @param network: Network where the relationships will be computed.
    """
    n = network
    for person in network.singles:
        # First, we skip this person if its already in a relationship.
        if alreadyInRelation(person, n.in_relation):
            continue

        for pos_partner in n.singles[n.singles.index(person)+1:]:
            # We skip this person if its already in a relationship.
            if alreadyInRelation(pos_partner, n.in_relation):
                continue

            # We skip if we they have incompatible orientations.
            if n.people[person].attributes['orientation'] + n.people[pos_partner].attributes['orientation'] == 0:
                continue

            # We skip if we have a heterosexual men or a woman with another
            # person of the same sex, and viceversa.
            if n.people[person].attributes['orientation'] == -1:
                if n.people[person].attributes['sex'] == n.people[pos_partner].attributes['sex']:
                    continue
            elif n.people[person].attributes['orientation'] == 1:
                if n.people[person].attributes['sex'] != n.people[pos_partner].attributes['sex']:
                    continue

            if n.people[pos_partner].attributes['orientation'] == -1:
                if n.people[person].attributes['sex'] == n.people[pos_partner].attributes['sex']:
                    continue
            elif n.people[pos_partner].attributes['orientation'] == 1:
                if n.people[person].attributes['sex'] != n.people[pos_partner].attributes['sex']:
                    continue

            prob = 1 # At the start, it's a given that they'll date.

            # We adjust the probability if they're friends, exes, or if they
            # complete a cycle of length 4.
            if n.people[pos_partner] in n.people[person].friends:
                prob -= 0.5
            if n.people[pos_partner] in n.people[person].exes:
                prob -= 0.5
            for ex in n.people[person].exes:
                if ex.current_partner is not None and n.people[pos_partner] in ex.current_partner.exes:
                    prob -= 0.7

            angle_btwn = computeAngleBtwnPeople(n.people[person], n.people[pos_partner])

            if angle_btwn > 0 and angle_btwn <= np.pi/4:
                prob -= 0.3
            elif angle_btwn > np.pi/4 and angle_btwn <= np.pi/2:
                prob -= 0.5
            elif angle_btwn > np.pi/2 and angle_btwn <= 3*np.pi/4:
                prob -= 0.7
            elif angle_btwn > 3*np.pi/4:
                prob -= 0.9

            if np.random.random() <= prob:
                network.in_relation.append((person, pos_partner))
                n.people[person].current_partner = n.people[pos_partner]
                n.people[pos_partner].current_partner = n.people[person]
                network.network.add_edges([(person, pos_partner)])
                # Add attribute to the edge!
                break

    # Before returning, we update the singles' list.
    for (person1, person2) in network.in_relation:
        if person1 in network.singles:
            del network.singles[network.singles.index(person1)]
        if person2 in network.singles:
            del network.singles[network.singles.index(person2)]

############################################################

def computeBreakups(network):
    """
    Computes the relationships that get broken up.

    @network: Network where the people are.
    """
    for couple in network.in_relation:
        prob = 0.95

        p, q = network.people[couple[0]], network.people[couple[1]]
        angle_btwn = computeAngleBtwnPeople(p, q)

        if angle_btwn > 0 and angle_btwn <= np.pi/4:
            prob -= 0.3
        elif angle_btwn > np.pi/4 and angle_btwn <= np.pi/2:
            prob -= 0.5
        elif angle_btwn > np.pi/2 and angle_btwn <= 3*np.pi/4:
            prob -= 0.7
        elif angle_btwn > 3*np.pi/4:
            prob -= 0.9

        if np.random.random() <= prob:
            del network.in_relation[network.in_relation.index(couple)]

            p.current_partner = None
            q.current_partner = None

            network.singles.append(couple[0])
            network.singles.append(couple[1])

            p.exes.add(q)
            q.exes.add(p)
            # Change attribute of the edge!

############################################################

def computeFriendships():
    """
    """
    pass

############################################################

def computeEndingFriend():
    """
    """
    pass

############################################################

if __name__ == "__main__":
    """
    Tests the things defined in this module.
    """
    society = people.createPopulation('./names.txt', 100)
    network = Network(society)

    print("Network without relations.")
    print(network)

    print("First generation of relations.")
    computeRomanticRelationships(network)
    print(network)

    #for p in network.people:
    #    print(p)

    computeBreakups(network)
    print("First generation of breakups.")
    print(network)
###### EOF: network.py #####################################

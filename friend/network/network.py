#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module simulates an affection social network.

Author: Ivan A. Moreno Soto
Last updated: 27/March/2018

TODO:
- Make computeFriendships take into account friends of friends.
"""

#-----------------------------------------------------------#

from random import sample

import numpy as np
import igraph

import network.people as people

#-----------------------------------------------------------#

class Network:
    """
    This class defines a container for all the data needed in
    order to simulate a social network of lovers.
    """

    def __init__(self, society):
        """
        Creates all the data needed to compute the simulation.

        @param society: List of People.
        """
        self.people = society

        # In the beggining, everybody is single.
        self.singles = [ident for ident in range(len(society))]
        self.in_relation = [] # People in relationships.

        self.graph = igraph.Graph()
        # We add our society to the graph.
        self.graph.add_vertices(len(self.people))
        # We add references to the Person objects.
        for (person, i) in zip(self.people, range(len(self.people))):
            self.graph.vs[i]['info'] = person

    def __str__(self):
        """
        Returns a string representation of the data contained
        in this Network.
        """
        return ''.join('Network with ' + str(len(self.people)) + ' people.\n'
                      + str(len(self.singles)) + ' are single.\n'
                      + str(2*len(self.in_relation)) + ' are in relationships.\n'
                      + str(self.graph.summary()))

#-----------------------------------------------------------#

def computeVecMagnitude(v):
    """
    Returns the magnitude of a vector v.

    @param v: Iterable object.
    """
    return np.sqrt( sum( np.power(v, [2 for x in v]) ) )

#-----------------------------------------------------------#

def computeDotProduct(v, u):
    """
    Returns the dot product of two vectors v and u.

    @param v: Iterable object.
    @param u: Iterable object.
    """
    return sum( [x * y for (x, y) in zip(v, u)] )

#-----------------------------------------------------------#

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

#-----------------------------------------------------------#

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

#-----------------------------------------------------------#

def areIncompatible(p, q):
    """
    Returns whether or not p and q have incompatible sexual
    orientations.

    @param p: Person object.
    @param q: Person object.
    """
    # If they have incompatible orientations.
    if p.attributes['orientation'] + q.attributes['orientation'] == 0:
        return True
    
    # If we have a heterosexual men or a woman with another
    # person of the same sex, and viceversa.
    if p.attributes['orientation'] == -1:
        if p.attributes['sex'] == q.attributes['sex']:
            return True
    elif p.attributes['orientation'] == 1:
        if p.attributes['sex'] != q.attributes['sex']:
            return True
            
    if q.attributes['orientation'] == -1:
        if p.attributes['sex'] == q.attributes['sex']:
            return True
    elif q.attributes['orientation'] == 1:
        if p.attributes['sex'] != q.attributes['sex']:
            return True

    return False

#-----------------------------------------------------------#

def createRelationship(network, p, q):
    """
    Adds a new relationship between p and q of a social network.

    @param network: Network object where p and q must be part of.
    @param p: Person object.
    @param q: Person object.
    """
    p_position = network.people.index(p)
    q_position = network.people.index(q)

    network.in_relation.append((p_position, q_position))
    p.current_partner = q
    q.current_partner = p
    network.graph.add_edges([(p_position, q_position)])

    # We get the id of the edge we just added and specify that it's
    # a current relationship.
    edge_id = network.graph.get_eid(p_position, q_position)
    network.graph.es[edge_id]['romantic'] = True

#-----------------------------------------------------------#

def reduceSinglesPool(network):
    """
    Deletes the indices of everybody in a relationship from
    the singles list of network.

    @param network: Network object whose singles list will be reduced.
    """
    for (person1, person2) in network.in_relation:
        if person1 in network.singles:
            del network.singles[network.singles.index(person1)]
        if person2 in network.singles:
            del network.singles[network.singles.index(person2)]

#-----------------------------------------------------------#

def computeRomanticRelationships(network, sample_pool = 20, pos_pool = 10):
    """
    Computes what relationships are made from the pool of
    single people of the network.

    @param network: Network where the relationships will be computed.
    @param sample_pool: Size of the sample from the singles pool.
    @param pos_pool: Size of the sample of 'dates' a person will have.
    """
    # To avoid making too many couples we just take a random sample from
    # the pool of single people.
    # We reduce the pool sizes in case they're too big.
    if len(network.singles) < sample_pool:
        sample_pool = len(network.singles)
    if len(network.singles) < pos_pool:
        pos_pool = len(network.singles)

    for person in sample(network.singles, sample_pool):
        # First, we skip this person if its already in a relationship.
        if alreadyInRelation(person, network.in_relation): continue

        p = network.people[person]
        
        # Now, we suppose that a single will know only a tiny part of the community.
        for pos_partner in sample(network.singles, pos_pool):
            # We skip if it's the same person.
            if person == pos_partner: continue
            
            # We skip this person if its already in a relationship.
            if alreadyInRelation(pos_partner, network.in_relation): continue

            q = network.people[pos_partner]

            # We check if they can even date.
            if areIncompatible(p, q): continue

            prob = 1 # At the start, it's a given that they'll date.

            # We adjust the probability if they're friends, exes, or if they
            # complete a cycle of length 4.
            if q in p.friends:
                prob -= 0.5
            if q in p.exes:
                prob -= 0.7
            for ex in p.exes:
                if ex.current_partner is not None and q in ex.current_partner.exes:
                    prob -= 0.6

            angle_btwn = computeAngleBtwnPeople(p, q)

            if angle_btwn > 0 and angle_btwn <= np.pi/4:
                prob -= 0.3
            elif angle_btwn > np.pi/4 and angle_btwn <= np.pi/2:
                prob -= 0.4
            elif angle_btwn > np.pi/2 and angle_btwn <= 3*np.pi/4:
                prob -= 0.5
            elif angle_btwn > 3*np.pi/4:
                prob -= 0.6

            if np.random.random() <= prob:
                createRelationship(network, p, q)
                break

    # Before returning, we update the singles' list.
    reduceSinglesPool(network)

#-----------------------------------------------------------#

def deleteRelationship(network, couple):
    """
    Changes current_partner and exes of p and q. Changes the
    relationships list of network.

    @param network: Network object where p and q must be.
    @param couple: Tuple of indices of Person objects.
    """
    p, q = network.people[couple[0]], network.people[couple[1]]

    del network.in_relation[network.in_relation.index(couple)]
    
    p.current_partner = None
    q.current_partner = None
    
    # We return the couple to the pool on singles.
    network.singles.append(couple[0])
    network.singles.append(couple[1])

    p.exes.add(q)
    q.exes.add(p)

    edge_id = network.graph.get_eid(couple[0], couple[1], directed = False)
    network.graph.delete_edges(edge_id)

#-----------------------------------------------------------#

def computeBreakups(network):
    """
    Computes the relationships that get broken up.

    @network: Network where the people are.
    """
    for couple in network.in_relation:
        break_prob = 0.95

        p, q = network.people[couple[0]], network.people[couple[1]]
        angle_btwn = computeAngleBtwnPeople(p, q)

        # Adjusting probability of a breakup.
        if angle_btwn >= 0 and angle_btwn <= np.pi/4:
            break_prob -= 0.9
        elif angle_btwn > np.pi/4 and angle_btwn <= np.pi/2:
            break_prob -= 0.7
        elif angle_btwn > np.pi/2 and angle_btwn <= 3*np.pi/4:
            break_prob -= 0.5
        elif angle_btwn > 3*np.pi/4:
            break_prob -= 0.3

        if np.random.random() <= break_prob:
            deleteRelationship(network, couple)

            if p in q.friends and np.random.random() <= 0.9:
                p.friends.remove(q)
                q.friends.remove(p)
                
#-----------------------------------------------------------#

def computeFriendships(network, sample_size = 70, pos_size = 8):
    """
    Decides what friendships get made and adds the respective edges
    to the network.

    @param network: Network object.
    @param sample_size: Number of people that'll get selected to make friends.
    @param pos_size: Number of possible friends for a person.
    """
    if len(network.people) < sample_size:
        sample_size = len(network.people)
    if len(network.people) < pos_size:
        pos_size = len(network.people)

    for person in sample(network.people, sample_size):
        for pos_friend in sample(network.people, pos_size):
            if person == pos_friend: continue
            if person in pos_friend.friends: continue
            if person.current_partner == pos_friend: continue
            
            prob = 1 # At the start, it's a given that they'll be friends.

            # We adjust the probability if they're friends, exes, or if they
            # complete a cycle of length 4.
            if pos_friend in person.exes:
                prob -= 0.9

            angle_btwn = computeAngleBtwnPeople(person, pos_friend)

            if angle_btwn > 0 and angle_btwn <= np.pi/4:
                prob -= 0.3
            elif angle_btwn > np.pi/4 and angle_btwn <= np.pi/2:
                prob -= 0.6
            elif angle_btwn > np.pi/2 and angle_btwn <= 3*np.pi/4:
                prob -= 0.8
            elif angle_btwn > 3*np.pi/4:
                prob -= 0.9

            if np.random.random() <= prob:
                person.friends.add(pos_friend)
                pos_friend.friends.add(person)

                p_position = network.people.index(person)
                q_position = network.people.index(pos_friend)

                network.graph.add_edges([(p_position, q_position)])
                
                # We get the id of the edge we just added and specify that it's
                # a friendly relationship.
                edge_id = network.graph.get_eid(p_position, q_position)
                network.graph.es[edge_id]['romantic'] = False

#-----------------------------------------------------------#

###### EOF: network.py ######################################

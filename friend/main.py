#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module controls the simulation and
visualization of a social network.

Author: Ivan A. Moreno Soto
Last updated: 27/March/18
"""

#-----------------------------------------------------------#

import network.people as people
import network.network as nw
import draw.draw as draw

#-----------------------------------------------------------#

print("Simulation of social networks of lovers.")
names_file = input("Path of a database of names and sexes: ")
society_size = int(input("Number of names to pull out of " + names_file + ": "))

society = people.createPopulation(names_file, society_size)
network = nw.Network(society)

generations = int(input("Number of generations for the simulation: "))
step = int(input("After how many generations do you want to see the plots of the network? "))

print("Network without relations.")
print(network)

nw.computeFriendships(network, sample_size = 20)
print("Network with only friendships.")
print(network)
draw.plotNetwork(network, "Network with only friendships")

for generation in range(1, generations+1):
    nw.computeRomanticRelationships(network)

    if generation % step == 0 and generation != generations:
        print("\nNetwork after " + str(generation) +  " generations.")
        print(network)
        draw.plotNetwork(network, "Network after " + str(generation) + " generations of relationships",
                         width = 1200, height = 1200)
        continue_sim = input("Continue the simulation? ")
        
    nw.computeBreakups(network)
    nw.computeFriendships(network, sample_size = 20)
    
print("\nFinal network after " + str(generations) +  " generations.")
print(network)
print(len(network.in_relation))
draw.plotNetwork(network, "Final network after " + str(generations) + " generations of relationships")

#-----------------------------------------------------------#

###### EOF: main.py #########################################

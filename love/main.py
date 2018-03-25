#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module controls the simulation, analysis, and
visualization of a social network.

Author: Ivan A. Moreno Soto
Last updated: 25/March/18

TODO:
- Create a simple menu to control the parameters.
"""

#-----------------------------------------------------------#

import network.people as people
import network.network as nw
import draw.draw as draw

#-----------------------------------------------------------#

society = people.createPopulation(".\\network\\names.txt", 210)
network = nw.Network(society)

print("Network without relations.")
print(network)

for generation in range(15):
    nw.computeRomanticRelationships(network)
    nw.computeBreakups(network)
    
print("Network after 15 generations")
print(network)
draw.plotNetwork(network, 'Network after 15 generations of relationships')

#-----------------------------------------------------------#

###### EOF: main.py #########################################

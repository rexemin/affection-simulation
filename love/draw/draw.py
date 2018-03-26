#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module implements everything needed for plotting
of a social network.

Author: Ivan A. Moreno Soto
Last updated: 25/March/2018
"""

#-----------------------------------------------------------#

import igraph

import plotly.offline as py
from plotly.graph_objs import *

from network.people import active_attr

#-----------------------------------------------------------#

def makeLabels(network):
    """
    Makes the labels that describes nodes of a network. Returns
    a tuple containing labels for males and labels for females.

    @param network: Network with which the labels will be made.
    """
    males = [person.name + ', ' +
              str(person.attributes['age']) + ', ' +
              active_attr['orientation'][person.attributes['orientation']]
              for person in network.people if person.attributes['sex'] == 0]

    females = [person.name + ', ' +
               str(person.attributes['age']) + ', ' +
               active_attr['orientation'][person.attributes['orientation']]
               for person in network.people if person.attributes['sex'] == 1]

    return (males, females)

#-----------------------------------------------------------#

def plotNetwork(network, plot_title, width = 800, height = 800):
    """
    Plots a 2D graph of the contents of network using plotly.

    @param network: An igraph graph.
    @param plot_title: Title of the plot (so, a string, obviously.)
    @param width: Width in pixels of the plot.
    @param height: Height in pixels of the plot.
    """
    # We get a description of the nodes (persons) of the network.
    labels = makeLabels(network)

    # We get an aesthetically pleasant layout for our graph.
    layout = network.graph.layout('kk') # Kamada-Kawai layout.

    # We get the nodes and edges in a way plotly can work the coordinates of them.
    coord_male = [[], []]
    coord_fem = [[], []]

    for v in network.people:
        k = network.people.index(v)
        
        if v.attributes['sex'] == 0:
            coord_male[0].append(layout[k][0])
            coord_male[1].append(layout[k][1])
        else:
            coord_fem[0].append(layout[k][0])
            coord_fem[1].append(layout[k][1])

    coord_current = [[], []]
    coord_past = [[], []]

    # We get the starting and ending points of every edge.
    for e in network.graph.es:
        e_v = e.tuple

        if e['current'] == True:
            coord_current[0] += [layout[e_v[0]][0], layout[e_v[1]][0], None]
            coord_current[1] += [layout[e_v[0]][1], layout[e_v[1]][1], None]
        else:
            coord_past[0] += [layout[e_v[0]][0], layout[e_v[1]][0], None]
            coord_past[1] += [layout[e_v[0]][1], layout[e_v[1]][1], None]

    # We make all the data we need to plot the edges and nodes.
    current_edges_trace = Scatter(x = coord_current[0], y = coord_current[1],
                               mode = 'lines',
                               line = Line(color='rgb(30, 144, 255)', width = 1),
                               hoverinfo = 'none')

    # We paint past relationships black.
    past_edges_trace = Scatter(x = coord_past[0], y = coord_past[1],
                               mode = 'lines',
                               line = Line(color='rgb(0, 0, 0)', width = 1),
                               hoverinfo = 'none')

    # Male nodes are purple.
    male_nodes_trace = Scatter(x = coord_male[0], y = coord_male[1],
                               mode = 'markers',
                               name = 'ntw',
                               marker = Marker(symbol = 'dot', size = 5, color = '#9400D3',
                                               line = Line(color = 'rgb(75, 0, 130)', width = 0.5)),
                               text = labels[0],
                               hoverinfo = 'text')

    # Female nodes are orange.
    fem_nodes_trace = Scatter(x = coord_fem[0], y = coord_fem[1],
                               mode = 'markers',
                               name = 'ntw',
                               marker = Marker(symbol = 'dot', size = 5, color = '#FFA500',
                                               line = Line(color = 'rgb(255, 140, 0)', width = 0.5)),
                               text = labels[1],
                               hoverinfo = 'text')

    # Options for the background of the plot.
    axis = dict(showline = False,
                zeroline = False,
                showgrid = False,
                showticklabels = False,
                title = '')

    # Characteristics of the plot.
    plot_layout = Layout(title = plot_title,
                    font = Font(size = 14),
                    showlegend = False,
                    autosize = False,
                    width = width, height = height,
                    xaxis = XAxis(axis), yaxis = YAxis(axis),
                    margin = Margin(l = 40, r = 40, b = 85, t = 100),
                    hovermode = 'closest')

    data = Data([current_edges_trace, past_edges_trace,
                 male_nodes_trace, fem_nodes_trace])
    figure = Figure(data = data, layout = plot_layout)
    py.plot(figure)

#-----------------------------------------------------------#

###### EOF: draw.py #########################################

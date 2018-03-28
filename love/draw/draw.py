#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module implements everything needed for plotting
of a social network.

Author: Ivan A. Moreno Soto
Last updated: 28/March/2018
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

def getNodesCoordinates(network, layout):
    """
    Returns the coordinates (IN 3D) for male and female nodes of a social
    network.

    @param network: Social network.
    @param layout: A graph layout from igraph.
    """
    coord_male = [[], [], []]
    coord_fem = [[], [], []]

    for v in network.people:
        k = network.people.index(v)
        
        if v.attributes['sex'] == 0:
            coord_male[0].append(layout[k][0])
            coord_male[1].append(layout[k][1])
            coord_male[2].append(layout[k][2])
        else:
            coord_fem[0].append(layout[k][0])
            coord_fem[1].append(layout[k][1])
            coord_fem[2].append(layout[k][2])

    return coord_male, coord_fem

#-----------------------------------------------------------#

def getEdgesCoordinates(network, layout):
    """
    Returns the coordinates for current and past relationships
    edges of a social network.

    @param network: Social network.
    @param layout: A graph layout from igraph.
    """
    coord_current = [[], [], []]
    coord_past = [[], [], []]

    # We get the starting and ending points of every edge.
    for e in network.graph.es:
        e_v = e.tuple

        if e['current'] == True:
            coord_current[0] += [layout[e_v[0]][0], layout[e_v[1]][0], None]
            coord_current[1] += [layout[e_v[0]][1], layout[e_v[1]][1], None]
            coord_current[2] += [layout[e_v[0]][2], layout[e_v[1]][2], None]
        else:
            coord_past[0] += [layout[e_v[0]][0], layout[e_v[1]][0], None]
            coord_past[1] += [layout[e_v[0]][1], layout[e_v[1]][1], None]
            coord_past[2] += [layout[e_v[0]][2], layout[e_v[1]][2], None]

    return coord_current, coord_past

#-----------------------------------------------------------#

def plotNetwork(network, plot_title, width = 1000, height = 1000):
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
    layout = network.graph.layout('kk_3d') # Kamada-Kawai layout.

    # We get the nodes and edges in a way plotly can work the coordinates of them.
    coord_male, coord_fem = getNodesCoordinates(network, layout)
    coord_current, coord_past = getEdgesCoordinates(network, layout)


    # We make all the data we need to plot the edges and nodes.
    current_edges_trace = Scatter3d(x = coord_current[0], y = coord_current[1], z = coord_current[2],
                                    mode = 'lines',
                                    name = 'Current',
                                    line = Line(color='rgb(30, 144, 255)', width = 5),
                                    hoverinfo = 'none')

    # We paint past relationships black.
    past_edges_trace = Scatter3d(x = coord_past[0], y = coord_past[1], z = coord_past[2],
                                 mode = 'lines',
                                 name = 'Past',
                                 line = Line(color='rgb(0, 0, 0)', width = 5),
                                 hoverinfo = 'none')

    # Male nodes are purple.
    male_nodes_trace = Scatter3d(x = coord_male[0], y = coord_male[1], z = coord_male[2],
                                 mode = 'markers',
                                 name = 'Male',
                                 marker = Marker(symbol = 'dot', size = 5, color = '#9400D3',
                                                 line = Line(color = 'rgb(75, 0, 130)', width = 0.5)),
                                 text = labels[0],
                                 hoverinfo = 'text')

    # Female nodes are orange.
    fem_nodes_trace = Scatter3d(x = coord_fem[0], y = coord_fem[1], z = coord_fem[2],
                                mode = 'markers',
                                name = 'Female',
                                marker = Marker(symbol = 'dot', size = 5, color = '#FFA500',
                                                line = Line(color = 'rgb(255, 140, 0)', width = 0.5)),
                                text = labels[1],
                                hoverinfo = 'text')

    # Options for the background of the plot.
    axis = dict(showbackground = False,
                showline = False,
                zeroline = False,
                showgrid = False,
                showticklabels = False,
                title = '')

    # Characteristics of the plot.
    plot_layout = Layout(title = plot_title,
                         font = Font(size = 14),
                         showlegend = True,
                         width = width, height = height,
                         scene = Scene(xaxis = XAxis(axis), yaxis = YAxis(axis), zaxis = ZAxis(axis)),
                         margin = Margin(t = 100),
                         hovermode = 'closest')

    data = Data([current_edges_trace, past_edges_trace,
                 male_nodes_trace, fem_nodes_trace])
    figure = Figure(data = data, layout = plot_layout)
    py.plot(figure, filename = plot_title.replace(' ', '') + '.html')

#-----------------------------------------------------------#

###### EOF: draw.py #########################################

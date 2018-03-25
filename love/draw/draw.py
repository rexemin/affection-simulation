#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module implements everything needed for plotting
of a social network.

Author: Ivan A. Moreno Soto
Last updated: 25/March/2018

TODO:
- Better document the plotting.
- Adjust colors.
- Add more description to the nodes.
"""

#-----------------------------------------------------------#

import igraph

import plotly.offline as py
from plotly.graph_objs import *

#-----------------------------------------------------------#

def plotNetwork(network, plot_title):
    """
    Plots a 2D graph of the contents of network using plotly.

    @param network: An igraph graph.
    @param plot_title: Title of the plot (so, a string, obviously.)
    """
    labels = [person.name for person in network.network.vs['info']]
    num_labels = len(labels)
    edges = [e.tuple for e in network.network.es]
    layout = network.network.layout('kk') # Kamada-Kawai layout.

    # We get the nodes and edges in a way plotly can work the coordinates of them.
    Xn = [layout[k][0] for k in range(num_labels)]
    Yn = [layout[k][1] for k in range(num_labels)]
    Xe = []
    Ye = []

    for e in edges:
        Xe += [layout[e[0]][0], layout[e[1]][0], None]
        Ye += [layout[e[0]][1], layout[e[1]][1], None]

    trace1 = Scatter(x = Xe, y = Ye,
                     mode = 'lines',
                     line = Line(color='rgb(210, 210, 210)', width = 1),
                     hoverinfo = 'none')

    trace2 = Scatter(x = Xn, y = Yn,
                     mode = 'markers',
                     name = 'ntw',
                     marker = Marker(symbol = 'dot', size = 5, color = '#6959CD',
                                     line = Line(color = 'rgb(50, 50, 50)', width = 0.5)),
                     text = labels,
                     hoverinfo = 'text')

    axis = dict(showline = False,
                zeroline = False,
                showgrid = False,
                showticklabels = False,
                title = '')

    width = 800
    height = 800

    plot_layout = Layout(title = plot_title,
                    font = Font(size = 14),
                    showlegend = False,
                    autosize = False,
                    width = width,
                    height = height,
                    xaxis = XAxis(axis),
                    yaxis = YAxis(axis),
                    margin = Margin(l = 40, r = 40, b = 85, t = 100),
                    hovermode = 'closest')

    data = Data([trace1, trace2])
    figure = Figure(data = data, layout = plot_layout)
    py.plot(figure)

#-----------------------------------------------------------#

###### EOF: draw.py #########################################

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module generates a set of people to be used
in the module network.py.

Author: Ivan A. Moreno Soto
Last updated: 26/March/2018
"""

#-----------------------------------------------------------#

from random import sample
from random import randint as ri

#-----------------------------------------------------------#

"""
Global dictionaries for indicating parameters used to create people.
"""
active_attr = {'sex':{0:'M', 1:'F'},
              'orientation':{-1:'straight', 0:'bi', 1:'gay'},
              'age':{i:i for i in range(16, 30)},
              'religion':{-2:'atheist', -1:'agnostic', 0:'catholic', 1:'christian', 2:'muslim'},
              'socio':{-1:'low', 0:'mid', 1:'high'},
              'race':{-2:'white', -1:'asian', 0:'light-brown', 1:'dark-brown', 2:'afro'},
              'music':{i:i for i in range(-5, 6)},
              'hobby':{i:i for i in range(-10, 11)},
              'personality':{i:i for i in range(-2, 3)}}

#-----------------------------------------------------------#

class Person:
    """
    This class defines a container for the name and
    attributes of a person. Defines a method to easily
    obtain a vector of its attributes and to print it.
    """

    def __init__(self, name, attrib):
        """
        Creates a new person with a given name and attributes.

        @param name: Name of this person.
        @param attrib: Dictionary of attributes for this person.
        """
        if type(attrib) is not dict:
            raise TypeError("attrib is not a dictionary!")

        self.name = str(name)
        self.attributes = attrib
        self.exes = set()
        self.friends = set()
        self.current_partner = None

    def __str__(self):
        """
        Returns a string that allows all the information of this
        person to be printed to some output flow.
        """
        attr = ''.join(str(key) + ": " + str(self.attributes[key]) + '\n'
                       for key in sorted(self.attributes.keys()))

        attr += 'Exes:\n'
        attr += ''.join(name + '\n' for name in self.exes)

        return "Name: " + self.name + "\n" + attr

#-----------------------------------------------------------#

def attrib2vec(person):
    """
    Returns the attributes dictionary of a person as
    a sorted vector with only the values of each attribute.

    @param person: Person object.
    """
    if type(person) is not Person:
        raise TypeError("person is not a Person object!")

    return [person.attributes[key] for key in sorted(person.attributes.keys())]

#-----------------------------------------------------------#

def readSample(file_path, size):
    """
    Reads a file containing rows of names and sexes
    and samples a set of a given size. Returns a None object
    if the file fails to be read, otherwise returns a list of
    tuples.

    @param file_path: Path to the file containing names and sexes.
    @param size: Size of the sample.
    """
    names = None

    with open(file_path, 'r') as database:
        database_sample = sample(database.readlines(), size)
        names = [tuple(row.split()) for row in database_sample]
    return names

#-----------------------------------------------------------#

def makeAttributes(names):
    """
    Creates a Person object for every name in names with the
    following attributes:
    - Sex
    - Sexual orientation
    - Age
    - Religion
    - Socioeconomic status
    - Race
    - Favorite music genre
    - Favorite hobby
    - Personality
    Returns a list of Person objects.

    @param names: List of tuples from readSample.
    """
    if type(names) is not list:
        raise TypeError("names is not a list!")
    if len(names) == 0:
        raise ValueError("names is an empty list!")
    if type(names[0]) is not tuple:
        raise TypeError("names is not a list of tuples. Values may be missing!")

    return [Person(name, {'sex':int(sex),
                          'orientation':ri(-1, 1),
                          'age':ri(16, 29),
                          'religion':ri(-2, 2),
                          'socio':ri(-1, 1),
                          'race':ri(-2, 2),
                          'music':ri(-5, 5),
                          'hobby':ri(-10, 10),
                          'personality':ri(-2, 2)}) for (name, sex) in names]

#-----------------------------------------------------------#

def createPopulation(file_path, size):
    """
    Creates a population of a given size for an artificial social
    network with names from file_path. Returns a list of Person objects.

    @param file_path: Path of the file with rows of names and sexes.
    @param size: Size of the population.
    """
    names = readSample(file_path, size)
    population = makeAttributes(names)
    return population

#-----------------------------------------------------------#

###### EOF: people.py #######################################

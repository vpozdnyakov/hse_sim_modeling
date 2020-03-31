"""
Python model "SI.py"
Translated using PySD version 0.10.0
"""
from __future__ import division
import numpy as np
from pysd import utils
import xarray as xr

from pysd.py_backend.functions import cache
from pysd.py_backend import functions

_subscript_dict = {}

_namespace = {
    'TIME': 'time',
    'Time': 'time',
    'New Reported Cases': 'new_reported_cases',
    'Infected': 'infected',
    'Susceptible': 'susceptible',
    'Contact Frequency': 'contact_frequency',
    'Contacts Between Infected and Uninfected Persons':
    'contacts_between_infected_and_uninfected_persons',
    'Cumulative Reported Cases': 'cumulative_reported_cases',
    'Infection Rate': 'infection_rate',
    'Infectivity': 'infectivity',
    'Probability of Contact with Infected Person': 'probability_of_contact_with_infected_person',
    'Susceptible Contacts': 'susceptible_contacts',
    'Total Population': 'total_population',
    'FINAL TIME': 'final_time',
    'INITIAL TIME': 'initial_time',
    'SAVEPER': 'saveper',
    'TIME STEP': 'time_step'
}

__pysd_version__ = "0.10.0"

__data = {'scope': None, 'time': lambda: 0}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


def time():
    return __data['time']()


@cache('step')
def new_reported_cases():
    """
    Real Name: b'New Reported Cases'
    Original Eqn: b'Infection Rate'
    Units: b'Persons/Week'
    Limits: (None, None)
    Type: component

    b''
    """
    return infection_rate()


@cache('step')
def infected():
    """
    Real Name: b'Infected'
    Original Eqn: b'INTEG ( Infection Rate, 1)'
    Units: b'Persons'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_infected()


@cache('step')
def susceptible():
    """
    Real Name: b'Susceptible'
    Original Eqn: b'INTEG ( -Infection Rate, Total Population)'
    Units: b'Persons'
    Limits: (None, None)
    Type: component

    b'The Population Susceptible to Ebola is the equal to the population \\n    \\t\\tsusceptible prior to the onset of the disease less all of those that have \\n    \\t\\tcontracted it. It is initialized to the Total Effective Population.'
    """
    return _integ_susceptible()


@cache('run')
def contact_frequency():
    """
    Real Name: b'Contact Frequency'
    Original Eqn: b'7'
    Units: b'Persons/Person/Week'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 7


@cache('step')
def contacts_between_infected_and_uninfected_persons():
    """
    Real Name: b'Contacts Between Infected and Uninfected Persons'
    Original Eqn: b'Probability of Contact with Infected Person * Susceptible Contacts'
    Units: b'Persons/Week'
    Limits: (None, None)
    Type: component

    b''
    """
    return probability_of_contact_with_infected_person() * susceptible_contacts()


@cache('step')
def cumulative_reported_cases():
    """
    Real Name: b'Cumulative Reported Cases'
    Original Eqn: b'INTEG ( New Reported Cases, 0)'
    Units: b'Persons'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_cumulative_reported_cases()


@cache('step')
def infection_rate():
    """
    Real Name: b'Infection Rate'
    Original Eqn: b'Contacts Between Infected and Uninfected Persons * Infectivity'
    Units: b'Persons/Week'
    Limits: (None, None)
    Type: component

    b'The infection rate is determined by the total number of contacts between \\n    \\t\\tinfected and uninfected people each week (Contacts Between Infected and \\n    \\t\\tUninfected Persons), and the probability that each such contact results in \\n    \\t\\ttransmission from the infected to uninfected person (Infectivity).'
    """
    return contacts_between_infected_and_uninfected_persons() * infectivity()


@cache('run')
def infectivity():
    """
    Real Name: b'Infectivity'
    Original Eqn: b'0.05'
    Units: b'Dmnl'
    Limits: (-1.0, 1.0, 0.001)
    Type: constant

    b''
    """
    return 0.05


@cache('step')
def probability_of_contact_with_infected_person():
    """
    Real Name: b'Probability of Contact with Infected Person'
    Original Eqn: b'Infected / Total Population'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return infected() / total_population()


@cache('step')
def susceptible_contacts():
    """
    Real Name: b'Susceptible Contacts'
    Original Eqn: b'Contact Frequency * Susceptible'
    Units: b'Persons/Week'
    Limits: (None, None)
    Type: component

    b''
    """
    return contact_frequency() * susceptible()


@cache('run')
def total_population():
    """
    Real Name: b'Total Population'
    Original Eqn: b'10000'
    Units: b'Persons'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 10000


@cache('run')
def final_time():
    """
    Real Name: b'FINAL TIME'
    Original Eqn: b'35'
    Units: b'Week'
    Limits: (None, None)
    Type: constant

    b'The final time for the simulation.'
    """
    return 35


@cache('run')
def initial_time():
    """
    Real Name: b'INITIAL TIME'
    Original Eqn: b'0'
    Units: b'Week'
    Limits: (None, None)
    Type: constant

    b'The initial time for the simulation.'
    """
    return 0


@cache('step')
def saveper():
    """
    Real Name: b'SAVEPER'
    Original Eqn: b'TIME STEP'
    Units: b'Week'
    Limits: (0.0, None)
    Type: component

    b'The frequency with which output is stored.'
    """
    return time_step()


@cache('run')
def time_step():
    """
    Real Name: b'TIME STEP'
    Original Eqn: b'0.125'
    Units: b'Week'
    Limits: (0.0, None)
    Type: constant

    b'The time step for the simulation.'
    """
    return 0.125


_integ_infected = functions.Integ(lambda: infection_rate(), lambda: 1)

_integ_susceptible = functions.Integ(lambda: -infection_rate(), lambda: total_population())

_integ_cumulative_reported_cases = functions.Integ(lambda: new_reported_cases(), lambda: 0)

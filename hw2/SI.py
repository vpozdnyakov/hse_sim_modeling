from __future__ import division
import numpy as np
from pysd import utils
import xarray as xr

from pysd.py_backend.functions import cache
from pysd.py_backend import functions

_subscript_dict = {}

_namespace = {
    'TIME': 'time',
    'TIME STEP': 'time_step',
    'SAVEPER': 'saveper',
    'FINAL TIME': 'final_time',
    'INITIAL TIME': 'initial_time',
    #
    'Infected': 'infected',
    'Susceptible': 'susceptible',
    'Contact Frequency': 'contact_frequency',
    'Contacts Between Infected and Uninfected Persons':
    'contacts_between_infected_and_uninfected_persons',
    'Infection Rate': 'infection_rate',
    'Infectivity': 'infectivity',
    'Probability of Contact with Infected Person': 'probability_of_contact_with_infected_person',
    'Susceptible Contacts': 'susceptible_contacts',
    'Total Population': 'total_population'    
}

__pysd_version__ = "0.10.0"

__data = {'scope': None, 'time': lambda: 0}

def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]

def time():
    return __data['time']()

@cache('step')
def infected():
    return _integ_infected()

@cache('step')
def susceptible():
    return _integ_susceptible()

@cache('run')
def contact_frequency():
    return 7

@cache('step')
def contacts_between_infected_and_uninfected_persons():
    return probability_of_contact_with_infected_person() * susceptible_contacts()

@cache('step')
def infection_rate():
    return contacts_between_infected_and_uninfected_persons() * infectivity()

@cache('run')
def infectivity():
    return 0.05

@cache('step')
def probability_of_contact_with_infected_person():
    return infected() / total_population()

@cache('step')
def susceptible_contacts():
    return contact_frequency() * susceptible()

@cache('run')
def total_population():
    return 10000

@cache('run')
def final_time():
    return 35

@cache('run')
def initial_time():
    return 0

@cache('step')
def saveper():
    return time_step()

@cache('run')
def time_step():
    return 0.125

_integ_infected = functions.Integ(lambda: infection_rate(), lambda: 1)

_integ_susceptible = functions.Integ(lambda: -infection_rate(), lambda: total_population())

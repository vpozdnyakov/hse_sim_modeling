from __future__ import division
import numpy as np
from pysd import utils
import xarray as xr

from pysd.py_backend.functions import cache
from pysd.py_backend import functions

_subscript_dict = {}

_namespace = {
    # Environment
    'TIME': 'time',
    'TIME STEP': 'time_step',
    'SAVEPER': 'saveper',
    'FINAL TIME': 'final_time',
    'INITIAL TIME': 'initial_time',
    # Stocks
    'Potential customers': 'potential_customers',
    'Customers': 'customers',
    'Competitor\'s customers': 'comp_customers',
    # Flows
    'Adopting rate': 'adopting_rate',
    'Frustration rate': 'frustration_rate',
    'Competitor\'s adopting rate': 'comp_adopting_rate',
    'Competitor\'s frustration rate': 'comp_frustration_rate',
    'Poaching rate': 'poaching_rate',
    'Competitor\'s poaching rate': 'comp_poaching_rate',
    # Dynamic variables
    'Adopting from advertising': 'adopting_from_ad',
    'Adopting from word of mouth': 'adopting_from_wom',
    'Competitor\'s adopting from advertising': 'comp_adopting_from_ad',
    'Competitor\'s adopting from word of mouth': 'comp_adopting_from_wom',
    # Parameters
    'Contact rate': 'contact_rate',
    'Adopting fraction': 'adopting_fraction',
    'Total population': 'total_population',
    'Advertising effectiviness': 'ad_effectiviness',
    'Competitor\'s advertising effectiviness': 'comp_ad_effectiviness',
    'Tolerance': 'tolerance',
    'Aggressiveness': 'aggressiveness',
    'Satisfying fraction': 'satis_fraction',
    'Competiror\'s satisfying fraction': 'comp_satis_fraction',
    'Neutral fraction': 'neutral_fraction',
    'Competiror\'s neutral fraction': 'comp_neutral_fraction'
    }

__pysd_version__ = "0.10.0"

__data = {'scope': None, 'time': lambda: 0}

def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]

def time():
    return __data['time']()

# Environment
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

# Stocks
@cache('step')
def potential_customers():
    return _integ_potential_customers()

@cache('step')
def customers():
    return _integ_customers()

@cache('step')
def comp_customers():
    return _integ_comp_customers()

# Flows
@cache('step')
def adopting_rate():
    return adopting_from_ad() + adopting_from_wom()

@cache('step')
def frustration_rate():
    return (
        customers() * 
        (1 - satis_fraction() - neutral_fraction()) * 
        (1 - tolerance()/adopting_rate())
    )

@cache('step')
def comp_adopting_rate():
    return comp_adopting_from_ad() + comp_adopting_from_wom()

@cache('step')
def comp_frustration_rate():
    return (
        comp_customers() * 
        (1 - comp_satis_fraction() - comp_neutral_fraction()) * 
        (1 - tolerance()/adopting_rate())
    )

@cache('step')
def poaching_rate():
    return (
        customers() * satis_fraction() * aggressiveness() * comp_customers() * 
        (
            comp_neutral_fraction() + 
            (1 - comp_satis_fraction() - comp_neutral_fraction()) * 
            tolerance() / 
            adopting_fraction()
        ) * tolerance()
    )

@cache('step')
def comp_poaching_rate():
    return (
        comp_customers() * comp_satis_fraction() * aggressiveness() * customers() * 
        (
            neutral_fraction() + 
            (1 - satis_fraction() - neutral_fraction()) * 
            tolerance() / 
            adopting_rate()
        ) * tolerance()
    )

# Dynamic variables
@cache('step')
def adopting_from_ad():
    return ad_effectiviness() * potential_customers()

@cache('step')
def adopting_from_wom():
    return (
        contact_rate() * 
        adopting_fraction() * 
        potential_customers() * 
        customers() / 
        total_population()
        )

@cache('step')
def comp_adopting_from_ad():
    return comp_ad_effectiviness() * potential_customers()

@cache('step')
def comp_adopting_from_wom():
    return (
        contact_rate() * 
        adopting_fraction() * 
        potential_customers() * 
        comp_customers() / 
        total_population()
        )

# Parameters
@cache('run')
def total_population():
    return 100000

@cache('run')
def contact_rate():
    return 100

@cache('run')
def adopting_fraction():
    return 0.015

@cache('run')
def ad_effectiviness():
    return 0.011

@cache('run')
def comp_ad_effectiviness():
    return 0.011

@cache('run')
def tolerance():
    return 0.01

@cache('run')
def aggressiveness():
    return 0.1

@cache('run')
def satis_fraction():
    return 0.2

@cache('run')
def neutral_fraction():
    return 0.7

@cache('run')
def comp_satis_fraction():
    return 0.4

@cache('run')
def comp_neutral_fraction():
    return 0.5

_integ_potential_customers = functions.Integ(
    lambda: frustration_rate() + comp_frustration_rate() - comp_adopting_rate() - adopting_rate(), 
    lambda: total_population())
_integ_customers = functions.Integ(
    lambda: adopting_rate() + poaching_rate() - frustration_rate() - comp_poaching_rate(),
    lambda: 0)
_integ_comp_customers = functions.Integ(
    lambda: comp_adopting_rate() + comp_poaching_rate() - comp_frustration_rate() - poaching_rate(),
    lambda: 0)
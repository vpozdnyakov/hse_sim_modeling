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
    'Potential customers': 'potential_customers',
    'Customers': 'customers',
    'Adopting rate': 'adopting_rate',
    'Adopting from advertising': 'adopting_from_ad',
    'Advertising effectiviness': 'ad_effectiviness',
    'Adopting from word of mouth': 'adopting_from_wom',
    'Contact rate': 'contact_rate',
    'Adopting fraction': 'adopting_fraction',
    'Total population': 'total_population'}

__pysd_version__ = "0.10.0"

__data = {'scope': None, 'time': lambda: 0}

def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]

def time():
    return __data['time']()

# basis
@cache('step')
def potential_customers():
    return _integ_potential_customers()

@cache('step')
def customers():
    return _integ_customers()

@cache('step')
def adopting_rate():
    return adopting_from_ad() + adopting_from_wom()

# constants
@cache('run')
def total_population():
    return 10000

@cache('run')
def contact_rate():
    return 100

@cache('run')
def ad_effectiviness():
    return 0.011

@cache('run')
def adopting_fraction():
    return 0.015

# parameters
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

# time constants
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

_integ_potential_customers = functions.Integ(lambda: -adopting_rate(), lambda: total_population())
_integ_customers = functions.Integ(lambda: adopting_rate(), lambda: 0)
import os
import environ
import requests
import beeline

# patch requests
from beeline.patch.requests import *

env = environ.Env(
    HONEYCOMB_API_KEY=(str,None),
    HONEYCOMB_DATASET=(str,'simpleweather-nonprod'),
    HONEYCOMB_DEBUG=(bool,False),
)
HONEYCOMB_API_KEY = env('HONEYCOMB_API_KEY')
HONEYCOMB_DATASET = env('HONEYCOMB_DATASET')
HONEYCOMB_DEBUG = env('HONEYCOMB_DEBUG')

def beeline_init():
    print(f'beeline initialization in process pid {os.getpid()}. Dataset is `{HONEYCOMB_DATASET}`, debug is {HONEYCOMB_DEBUG}')
    beeline.init(writekey=HONEYCOMB_API_KEY, dataset=HONEYCOMB_DATASET, debug=HONEYCOMB_DEBUG)

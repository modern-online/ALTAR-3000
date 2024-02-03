#!/usr/bin/python3

import pandas as pd
import pickle
import ssl
import os
from random import randint
import requests

# Required for SSL requests
ssl._create_default_https_context = ssl._create_unverified_context

# File to log Predictit bets
markets_archive_file = 'markets.txt'

api_url = 'https://www.predictit.org/api/marketdata/all/'

header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

# ===========================================================================
# RETRIEVE MARKET DATA
# ===========================================================================

# Clears archive Pickle
def clear_archive():
    empty = []
    with open(markets_archive_file, 'wb') as fp:
        pickle.dump(empty, fp)

# Retrieves and stores names of all current markets
def all_market_names():
    #clear_archive()
    bets = []
    print("Retrieving market data...")
    r = requests.get(api_url, headers=header).json()
    #print(j)
    df = pd.DataFrame.from_dict(r)
    print("Retrieved.")
    print("Storing.")
    for item in df.values:
        bets.append(item[0]['name'])
    with open(markets_archive_file, "wb") as fp:
        pickle.dump(bets, fp)

# Chooses random bet headline
def pick_random_bet():
    if os.stat(markets_archive_file).st_size != 0:
        with open(markets_archive_file, "rb") as fp:
            markets_archive = pickle.load(fp)
            random_bet = markets_archive[randint(0, len(markets_archive))]
            return random_bet

# ===========================================================================
import re
import numpy as np
import pandas as pd
import pickle
from bs4 import BeautifulSoup
import urllib
import time

DATA_PATH='data/'
RAW_PATH = f'{DATA_PATH}raw/'
MAX_TRIES = 10

def get_soup(url,nth_try=0):
    i = nth_try + 1
    if i > MAX_TRIES: return(None)
    try:
        #read html
        f = urllib.request.urlopen(url)
        page_bytes = f.read()
        page = page_bytes.decode("utf8")
        f.close()
        #parse
        soup = BeautifulSoup(page,'html.parser')
        return(soup)
    except:
        print(f'Trying for {i}th time')
        return(get_soup(url,i))
    
url_df = pd.read_csv(f'{DATA_PATH}url_df.csv')
recipe_urls = list(url_df['recipe_url'])

soups = []
soup_nutris = []

from datetime import datetime
start_time = datetime.now()
for i in range(len(recipe_urls)):
    soup = get_soup(recipe_urls[i])
    soups.append(soup)
    
    nutri_url = f'{recipe_urls[i]}fullrecipenutrition'
    soup_nutri = get_soup(nutri_url)
    soup_nutris.append(soup_nutri)
    
    if i % 100 == 0:
        print(datetime.now()-start_time)
        np.save(f'{RAW_PATH}soups.npy',[str(s) for s in soups])
        np.save(f'{RAW_PATH}soup_nutris.npy',[str(s) for s in soup_nutris])

np.save(f'{RAW_PATH}soups.npy',[str(s) for s in soups])
np.save(f'{RAW_PATH}soup_nutris.npy',[str(s) for s in soup_nutris])
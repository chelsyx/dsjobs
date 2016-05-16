import requests
import json
from collections import OrderedDict
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from sqlalchemy import create_engine


myUserAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/601.5.17 (KHTML, like Gecko) Version/9.1 Safari/601.5.17"
basepath_id = 'http://api.indeed.com/ads/apisearch'
page = 0

# authentication information & other request parameters
params_id = OrderedDict({
    "publisher": "2034728625430383",
    "v": "2",
    "format": "json",
    # "callback": "newquery",
    "q": "data scientist",
    "sort": "relevance",
    "st": "employer",
    "jt": "fulltime",
    "start": page*25,
    "limit": "300", # Maximum number of results returned per query. Default is 10
    "fromage": "30",
    "highlight": "0",
    "filter": "1",
    "latlong": "1",
    "co": "us",
    # programmatically get the IP of the machine
    "userip": requests.get("https://api.ipify.org?format=json").json()['ip'],  
    "useragent": myUserAgent
})

results = pd.DataFrame()

for page in range(0, 15):    
    params_id['start'] = page*25
    # request the API
    response_id = requests.get(basepath_id, params=params_id, headers={"User-Agent": myUserAgent})                               
    this_results = pd.DataFrame(response_id.json()['results'])
    results = results.append(this_results, ignore_index=True)

# scrape job description text
job_summary = []
for this_url in results['url']:
    site = requests.get(this_url)
    soup_obj = BeautifulSoup(site.text, "lxml")
    job_summary.append(soup_obj.find('span', {'id': 'job_summary'}).text)


    
results['job_summary'] = job_summary


# write to sqllite
engine = create_engine('sqlite:///indeedpost.sqlite')
results.to_sql('ds_post', engine, index=False)

# read from sqlite
engine = create_engine('sqlite:///indeedpost.sqlite')
results = pd.read_sql_table('ds_post', engine)
# read_sql_query
# read_sql







# np.sum(results.duplicated())
response_id.status_code # check the response code (should be 200) 
response_id.json().keys()
response_id.json()['totalResults']
len(response_id.json()['results']) # list

results = pd.DataFrame(response_id.json()['results'])


site = requests.get(results['url'][0])
soup_obj = BeautifulSoup(site.text, "lxml")
soup_obj.find('span', {'id': 'job_summary'}).text ## all text
# soup_obj.find('span', {'id': 'job_summary'}).findAll('b') ## bold tag
# soup_obj.find('span', {'id': 'job_summary'}).contents[0].strip() ## element by element




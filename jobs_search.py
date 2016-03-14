from bs4 import BeautifulSoup 
from time import sleep 
import pandas as pd 
import requests
import re
import os

titles=['data scientist','data engineer','data analyst','business analyst','business intelligence engineer','research scientist','statistician','business intelligence analyst','machine learning engineer']

baseurl='http://www.indeed.com/jobs'

total=[]

for title in titles:
    search_para={'q':'title:"'+title+'"', 'jt':'fulltime', 'sr':'directhire'}

    this_titl = requests.get(baseurl, params=search_para)
    soup = BeautifulSoup(this_titl.text,"html.parser")
    
    # Total number of jobs
    
    t_div = soup.find('div', {'id': 'searchCount'}).text
    job_numbers = re.findall('\d+', t_div)
    if len(job_numbers) > 3: 
        total.append(int(job_numbers[2])*1000 + int(job_numbers[3]))
    else:
        total.append(int(job_numbers[2])) 
    
    # Salaries

    s_div = soup.find('div', {'id': 'SALARY_rbo'})
    s_li = s_div.findAll('li')
    xlab = []
    yfreq = []
    
    for s in s_li:
        xlab.append(s.a.text.strip().encode('utf-8'))
        s.a.extract()
        yfreq.append(int(re.search(r"\d+", s.text).group(0)))
    
    
    salaries = pd.DataFrame({'Salary Estimate':xlab,'Counts':yfreq})
    
    filename = '_'.join(title.split())+'_sal.csv'
    filename = os.path.join('/Users/chelsyx/Documents/Projects/indeed_dsjobs/search_data',filename)
    salaries.to_csv(filename, sep=',', index=False)
    
    sleep(1)
from bs4 import BeautifulSoup 
from time import sleep 
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd 
import requests
import re
import os

titles=['data scientist','data engineer','data analyst','business analyst','business intelligence engineer','research scientist','statistician','business intelligence analyst','machine learning engineer']

baseurl='http://www.indeed.com/jobs'

datadir = '/Users/chelsyxie/Desktop/dsjobs/search_data'

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

    s_li = soup.find('div', {'id': 'SALARY_rbo'}).findAll('li')
    
    # Handle hidden list
    if len(s_li)==0:
        browser = webdriver.Firefox()
        browser.get(this_titl.url)
        try:
            elem = browser.find_element_by_xpath('//*[@id="SALARY_rbo"]/ul')
        except NoSuchElementException:
            elem = browser.find_element_by_xpath('//*[@id="rb_Salary Estimate"]/div/span')
            elem.click()
            sleep(0.2)
            elem = browser.find_element_by_xpath('//*[@id="SALARY_rbo"]/ul')

        subSoup = BeautifulSoup(elem.get_attribute("outerHTML"),"html.parser")
        s_li = subSoup.findAll('li')
        browser.quit()
    
    xtag = []
    counts = []
    
    for s in s_li:
        xtag.append(s.a.text.strip().encode('utf-8'))
        s.a.extract()
        counts.append(int(re.search(r"\d+", s.text).group(0)))
    
    
    salaries = pd.DataFrame({'Salary Estimate':xtag,'Counts':counts})
    
    filename = '_'.join(title.split())+'_sal.csv'
    filename = os.path.join(datadir,filename)
    salaries.to_csv(filename, sep=',', index=False)
    
    # Location

    l_li = soup.find('div', {'id': 'LOCATION_rbo'}).findAll('li')
    
    # Handle hidden list
    if len(l_li)==0:
        browser = webdriver.Firefox()
        browser.get(this_titl.url)
        try:
            elem = browser.find_element_by_xpath('//*[@id="LOCATION_rbo"]/ul')
        except NoSuchElementException:
            elem = browser.find_element_by_xpath('//*[@id="rb_Location"]/div/span')
            elem.click()
            sleep(0.2)
            elem = browser.find_element_by_xpath('//*[@id="LOCATION_rbo"]/ul')

        subSoup = BeautifulSoup(elem.get_attribute("outerHTML"),"html.parser")
        l_li = subSoup.findAll('li')
        browser.quit()
    
    xtag = []
    counts = []
    
    for l in l_li:
        xtag.append(l.a.text.strip().encode('utf-8'))
        l.a.extract()
        counts.append(int(re.search(r"\d+", l.text).group(0)))
    
    
    locations = pd.DataFrame({'Location':xtag,'Counts':counts})
    
    filename = '_'.join(title.split())+'_loc.csv'
    filename = os.path.join(datadir,filename)
    locations.to_csv(filename, sep=',', index=False)
    
    sleep(1)
  
    
titlCnts = pd.DataFrame({'Title':titles,'Counts':total})
titlCnts.to_csv(os.path.join(datadir, 'title_counts.csv'), sep=',', index=False)

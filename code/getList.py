
# coding: utf-8


from requests import get
from bs4 import BeautifulSoup
import json
import pandas as pd
"""
This script is used to scrape data from apartments.com website for useful listings

Sample usage:

url = 'https://www.apartments.com/east-village-lower-east-side-new-york-ny/?bb=5gp3tw00vHgg_4vI'
get_all_page(url,3)

"""


# This function scrapes a list of building address/name/urls
def scrape_page(url):
    # get all the info
    response = get(url)
    # parse using beautiful soup
    html_soup = BeautifulSoup(response.text, 'html.parser')
    # specify info we need
    building_containers = html_soup.find_all('div', class_ = 'mainWrapper')
    building_list = building_containers[0].script.text
    # convert string to dictionary
    json_acceptable_string = building_list.replace("'", "\"")
    building = json.loads(json_acceptable_string)
    # get dataframe we need
    return pd.DataFrame.from_dict(building['about'])

# Using 'next' url to update new list in given map area

def get_all_page(url,page):
    for i in range(1,page+1):
        if i == 1:
            building_info = scrape_page(url)
        else:
            url_new = str(url.split('/',-1)[0]+'/'+url.split('/',-1)[1]+'/'+url.split('/',-1)[2]+'/'+url.split('/',-1)[3]
                          +'/'+str(i)+'/'
                          +url.split('/',-1)[4])
            building_new = scrape_page(url_new)
            building_info = building_info.append(building_new,ignore_index=True)
            
    return building_info

def get_num(url):
    response = get(url)
    # parse using beautiful soup
    html_soup = BeautifulSoup(response.text, 'html.parser')
    # specify info we need
    page_num = html_soup.find_all('div', class_ = 'paging')
    next_url = page_num[0].find('a',attrs ={'data-page':'2'}).text
    return page_num



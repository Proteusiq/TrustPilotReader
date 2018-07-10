#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This code implements basic data scraping of TrustPilot [default:Danish] Reviews .

It is a prototype to be used for academic reasons only.
TrustPilot offers APIs to gather their data
 

How to use it:

1. Initiate the class with either (a) passing a dictionary of companies as keys
    and companies TrustPilot id as items or (b) adding them with dictionary syntax.

    e.g. a. id_dict = {'Skat':'470bce96000064000501e32d','DR':'4690598c00006400050003ee'}
            d = GetReviews(id_dict)
         
         b. d = GetReviews()
            d['Skat'] = '470bce96000064000501e32d' 
    
    To get TrustPilot's company id, open www.trustpilot.com on your browser
    right click to inspect the page, then select Network. Search the name
    of the company on TrustPilot webpage. Filter: json
    https://www.trustpilot.com/review/IDISHERE/jsonld
   

2. Gather Data 
    You can pass in different language e.g. Norwegian. Default is 'dk'
    
    retured_dict = d.GatherData('no')

3. Save Data
    You can pass location and file_name. Default is pwd and 'TrustPilotData' as name
    d.SaveData()

4. Reading data
    df = pd.DataFrame(returned_dict)

    or

    df = pd.DataFrame(d.dictData)

    or from stored source
    df = pd.read_pickle('TrustPilotData.pkl', compression='gzip')


#TODOs:
    Allow different saving formats e.g. df.to_XXX
    Add more features
    Write a better documetation

"""

__author__ = "Prayson W. Daniel"
__copyright__ = "Copyright 2018, Prayson W. Daniel"
__credits__ = []
__license__ = "Creative Commons Attribution 3.0 Unported (CC BY 3.0): http://creativecommons.org/licenses/by/3.0/"
__version__ = "1.0"
__maintainer__ = "Prayson W. Daniel"


from collections import defaultdict
import pandas as pd
import requests


class GetReviews:
    '''
    Prototype Module for gathering data from TrustPilot.
    Use only for teaching purposes. TrustPilot offers APIs to gather their data
    '''

    def __init__(self, companies_ids=None):

        if companies_ids:
            self.companies_id = companies_ids
        else:
            self.companies_id = {}

        self.dictData = defaultdict(list)
        print('TrustPilot companies ids loaded')

    def __str__(self):
        print('Companies and Ids to Mine')
        df = pd.DataFrame([self.companies_id]).T
        df.rename(index=str, columns={0: 'Ids'}, inplace=True)
        return df.to_string()

    def __len__(self):
        return len(self.companies_id)

    def __delitem__(self, key):
        del self.companies_id[key]

    def __setitem__(self, key, item):
        self.companies_id[key] = item

    def PageReview(self, reviewid, company, www='dk', verbose=True):

        rdata = requests.get(
            'https://{}.trustpilot.com/review/{}/jsonld?page=1'.format(www, reviewid)).json()
        reviewpages = (int(rdata['aggregateRating']['reviewCount']) // 20) + 1
        print('Company: {}. Data from {}.trustpilot.com'.format(company, www))
        j = 1
        while j <= reviewpages:

            self.payload = {'page': j}
            if verbose:
                print('Mining data from page {j}:{i} in progress ...'.format(
                    j=j, i=reviewpages))

            rdata = requests.get('https://{}.trustpilot.com/review/{}/jsonld'.format(www, reviewid),
                                 params=self.payload).json()

            for i, _ in enumerate(rdata['review']):
                self.dictData['reviewerName'].append(
                    rdata['review'][i]['author']['name'])
                self.dictData['headline'].append(
                    rdata['review'][i]['headline'])
                self.dictData['inLanguage'].append(
                    rdata['review'][i]['inLanguage'])
                self.dictData['datePublished'].append(
                    rdata['review'][i]['datePublished'])
                self.dictData['reviewBody'].append(
                    rdata['review'][i]['reviewBody'])
                self.dictData['ratingValue'].append(
                    rdata['review'][i]['reviewRating']['ratingValue'])
                self.dictData['Company'].append(company)
                i += 1
            if verbose:
                print('Mining {c} data from page {j}:{i} completed of {www}.trustpilot.com'.format(
                    c=company, j=j, i=reviewpages, www=www))
            j += 1

    # Reading query to df

    def GatherData(self, www='dk'):
        for company, review in self.companies_id.items():
            GetReviews.PageReview(self, review, company, www)

        return self.dictData
    # Writing file to desired location

    def SaveData(self, location=None, file_name='TrustPilotData'):
        #location = '/home/danpra/models/'

        get_location = location if location else ''

        if self.dictData:
            df = pd.DataFrame(self.dictData)
        else:
            print('Firing GatherData')
            GetReviews.GatherData(self)
            df = pd.DataFrame(self.dictData)

        df.to_pickle('{}{}.pkl'.format(get_location, file_name),
                     compression='gzip')

        print('File saved:{}{}.pkl\nFile contains {} rows'.format(
            get_location, file_name, df.shape[0]))

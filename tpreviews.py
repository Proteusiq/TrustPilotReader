#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This code implements basic data scraping of TrustPilot [default:Danish] Reviews .

It is a prototype to be used for academic reasons only.
TrustPilot offers APIs to gather their data
 
How to use it: README.md
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

    def page_review(self, reviewid, company, www='dk', verbose=True):

        rdata = requests.get(
            'https://{}.trustpilot.com/review/{}/jsonld?page=1'.format(www, reviewid)).json()
        # Change in API 17-08-2017 from rdata being dictionary to a list where 0 element is like original flow
        # Next line is added to adopt this changes
        rdata = rdata[0] # Added 17-08-2017 07:50 a.m    
        reviewpages = (int(rdata['aggregateRating']['reviewCount']) // 20) + 1
        print('Company: {}. Data from {}.trustpilot.com'.format(company, www))
        j = 1
        while j <= reviewpages:

            self.payload = {'page': j}
            if verbose:
                print('Mining data from page {j}:{i} in progress ...'.format(
                    j=j, i=reviewpages))

            rdata = requests.get('https://{}.trustpilot.com/review/{}/jsonld'.format(www, reviewid),
                                 params=self.payload)
            
            # Check if we caught a fish
            if rdata.ok:
                rdata = rdata.json()
                rdata = rdata[0] # Added 17-08-2017 07:50 a.m 

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

            else:
                pass # Todo: Do something if we have error in connection

    # Reading query to df

    def gather_data(self, www='dk'):
        for company, review in self.companies_id.items():
            GetReviews.page_review(self, review, company, www)

        return self.dictData
    # Writing file to desired location

    def save_data(self, location=None, file_name='TrustPilotData'):
        #location = '/home/danpra/models/'

        get_location = location if location else ''

        if self.dictData:
            df = pd.DataFrame(self.dictData)
        else:
            print('Firing GatherData')
            GetReviews.gather_data(self)
            df = pd.DataFrame(self.dictData)

        df.to_pickle('{}{}.pkl'.format(get_location, file_name),
                     compression='gzip')

        print('File saved:{}{}.pkl\nFile contains {} rows'.format(
            get_location, file_name, df.shape[0]))

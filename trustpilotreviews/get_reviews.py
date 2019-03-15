#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This code implements basic data scraping of TrustPilot [default:Danish] Reviews .

It is a prototype to be used for academic reasons only.
TrustPilot offers APIs to gather their data
 
"""


from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

import dataset
import pandas as pd
import requests

class GotData:
    '''Pretty Output
    Getting the .ok and .content requests syntax
    '''

    def __init__(self, ok, business_name, business_id):
        self.ok = ok
        self.business_name = business_name
        self.business_id = business_id
	
    def __repr__(self):
        if self.ok:
            return '[200] Data Found'
        else:
            return '[404] Data Not Found'


class GetReviews:
    '''
    Prototype Module for gathering data from TrustPilot.
    Use only for teaching purposes. TrustPilot offers APIs to gather their data

    example:

    >>> import numpy as np
    >>> from .get_review import GetReviews
    >>> # Dictionary from Data 
    >>> lines = np.genfromtxt('businesses_ids.csv', delimiter=',',
                        dtype=str, skip_header=1)
    >>> csv_dict = {key: item for key, item in lines}
    >>>
    >>> d = GetReviews(csv_dict)
    >>> d.gather_data('no') # Get Norwegian Reviews
    
    '''

    def __init__(self, businesses_ids=None, language=None, verbose=True):
        
        self.verbose = verbose
        while language is None:
            language = input('Select language:\n\tdk for danish'
                            '\n\tno for norwegian\n\tse for swedish'
                            '\n\tfi for finish\n\ten for english\n> ')
            try:                 
                if language.lower() not in ('dk','no','se','fi','en'):
                    language = None # Restore None
                    raise ValueError('Invalid selection')
            except ValueError as v:
                print(f'{v.args[0]}. Trying again ...')
                
  
        else:
            lang = {'dk':'Danish','no':'Norwegian','se':'Swedish',
                    'fi':'Finish','en':'English'}
            print(f'\n{lang[language.lower()]:>10} selected')

            self.www = 'www' if language.lower() == 'en' else language.lower()  
                         
        
        if businesses_ids is not None:
            print('Receiving businesses Ids')
            self.businesses_id = businesses_ids
            print(self.businesses_id)
        elif businesses_ids is None:
            print('Waiting businesses Ids ...')
            self.businesses_id = {}

        self.dictData = defaultdict(list)  
        

    def __repr__(self):
        print('businesses and Ids to Mine')
        df = pd.DataFrame([self.businesses_id]).T
        df.rename(index=str, columns={0: 'Ids'}, inplace=True)
        return df.to_string()

    def __len__(self):
        return len(self.businesses_id)

    def __delitem__(self, key):
        del self.businesses_id[key]

    def __setitem__(self, key, item):
        self.businesses_id[key] = item

    def get_id(self,query):
        '''Returns Business Id
       
        This function returns and add matched id of a given business 
        given business website name to be mined.

        Parameters
        
        query : str
            query requires the full business website name as
            appears in trustpilot page.
        

        Returns
        
        object
            object of .ok and .content is return.
            if business id is found .ok value is True
            and .content value equals business id. if not, .ok
            value is False, and .content value is None.

        Raises
        
        ConnectionError
            when a connection fails, ConnectionError is raised

        Code Example:

        >>> from trustpilotreviews import GetReviews
        >>> t = GetReviews.GetReviews()
        >>> mate_id = t.get_id('www.mate.bike')
        >>> if mate_id.ok:
                print(mate.business_id)

        '''
        
        url = 'https://www.trustpilot.com/businessunit/search'
        params = {'country':self.www,'query':query} 
        r = requests.get(url, params=params)
        
        if r.ok:
            data = r.json()
            for items in data['businessUnits']:
                if items['name']['identifying']==params['query']:
                    
                    business_id = GotData(
                        True, items['displayName'].strip(), items['id'])
                    self.businesses_id[items['displayName']] = items['id']
                    break
            else:
                business_id = GotData(False,None,None)
            return business_id
        else:
            raise ConnectionError('Connection Error')


    def get_ids(self,queries):
        '''Returns Business Ids
       
        Similiar to get_ids, this function takes in list of websites
        returns a Pandas dataFrame of __matched__ websites and their ids.  
        

        Parameters
        
        queries : list of business websites
            queries requires the full business website names as
            appears in trustpilot page in a list.
        

        Returns
        
        Pandas DataFrame
            DataFrame of __matched__ websites and their ids.

        Raises
        
        ConnectionError
            when a connection fails, ConnectionError is raised

        Code Example:

        >>> from trustpilotreviews import GetReviews
        >>> t = GetReviews()
        >>> ids = t.get_ids(['www.ford.dk','www.mate.bike'])
        >>> print(ids) # same as print(t) as ids are added to que
        >>> data = t.get_reviews() # mine data for
    
        '''
        
        id_data = defaultdict(list)

        def mult_get_id(query):
            response = self.get_id(query)
            if response.ok:
                id_data[response.business_name].append(response.business_id)
                
        with ThreadPoolExecutor(max_workers=len(queries)) as executor:
            for business_id in queries:
                executor.submit(mult_get_id, business_id)

        
        return pd.DataFrame(id_data).T.rename({0:'ids'},axis=1)
        

    def page_review(self, reviewid, business):
        '''
        generate DataFrame populated with TrustPilot data
        '''
        rdata = requests.get(
            f'https://{self.www}.trustpilot.com/review/{reviewid}/jsonld?page=1')
        # Change in API 17-08-2017 from rdata being dictionary to a list where 0 element is like original flow
        # Next line is added to adopt this changes
        
        if not rdata.ok:
            raise ConnectionError('connection failed')

        rdata = rdata.json()
        rdata = rdata[0] # Added 17-08-2017 07:50 a.m 
         
        reviewpages = (int(rdata['aggregateRating']['reviewCount']) // 20) + 1
        
        print(f'business: {business}. {reviewpages}'
            f' pages-reviews from {self.www}.trustpilot.com')

        
        j = 1
        while j <= reviewpages:
            
            self.payload = {'page': j}
            if self.verbose:
                print(f'Mining data from page {j}:{reviewpages} in progress ...')

            rdata = requests.get(f'https://{self.www}.trustpilot.com/review/{reviewid}/jsonld',
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
                    self.dictData['business'].append(business)
                    i += 1
                if self.verbose:
                    print(f'Mining {business} data from page {j}:{reviewpages} '
                          f'completed of {self.www}.trustpilot.com')
                j += 1

            else:
                pass # Todo: Do something if we have error in connection

    # Reading query to df

    def gather_data(self, review, business):
        '''
        singe gathering. Used in multiprocess
        '''
        self.page_review(review, business)
        
        return self.dictData


    def get_reviews(self):
        '''
        gather data using multithreads
        '''
        # Maximum works of three threads
        with ThreadPoolExecutor(max_workers=len(self.businesses_id)+2) as executor:
            for business, review in self.businesses_id.items():
                executor.submit(self.gather_data, review, business)
        
        return self.dictData

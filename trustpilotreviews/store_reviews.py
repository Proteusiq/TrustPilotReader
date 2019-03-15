#!/usr/bin/env python3
# -*- coding: utf-8 -*-




import dataset
import pandas as pd

from .get_review import GetReviews

# Writing file to desired location

class LoadReviews(GetReviews):

    def send_db(self,location='data', db_name='reviews',
                table_name='trustdata'):
        '''Send data to a data base
       
        This function save mined data to disk

        Parameters
        ----------
        location : string
            path to the folder
        db_name : string
            name of a database
        table_name : string
            name of a table in a daabase

        Returns
        -------
        None
            No value is return


        How to read from database

        >>> import dataset
        >>> from stuf import stuf
        >>> with dataset.connect('sqlite:///mydatabase.db', row_type=stuf) as db:
        >>>     result = db.query('SELECT business, COUNT(*) c FROM trustdata GROUP BY ratingValue')
        >>>     for row in result:
        >>>         print(f"{row['business']:^20} | {row['c']:^20}")
        '''
        with dataset.connect(f'sqlite:///{location}/{db_name}.db') as db:
            print(f'loading to data into {table_name} table in {db_name}.db ')
            data = pd.DataFrame(self.dictData).T.to_dict()
            data_d = [data[i] for i in data] # dataset expects
            db[table_name].insert_many(data_d)
            print(f'loading data completed')
        
        print(f'File saved:{location}{db_name}.db')
    # Writing file to desired location
    
    def save_data(self, location='/data', file_name='TrustPilotData'):
        '''Save Data to Disk
       
        This function save mined data to disk

        Parameters
        ----------
        location : string
            path to the folder
        filename : string
            name of the file

        Returns
        -------
        None
            No value is return

        Raises
        ------
        ValueError
            raised when there is no data to save
       
        '''    
        #location = '/projectname/data/'

        if self.dictData:
            df = pd.DataFrame(self.dictData)
            df.drop_duplicates(inplace=True)
            df.to_pickle(f'{location}/{file_name}.pkl')

            print(f'File saved:{location}{file_name}.pkl'
                f'\nFile contains {df.shape[0]} rows')
            
        else:
            raise ValueError('no data to save found')
        

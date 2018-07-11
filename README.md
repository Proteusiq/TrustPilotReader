# TrustPilotReader
Unofficial TrustPilot Review Collector. Academic Use Only

#Unmatured Documetation :)

This code implements basic data scraping of TrustPilot [default:Danish] Reviews .

It is a prototype to be used for academic reasons only.
TrustPilot offers APIs to gather their data
 

#How to use it:

1. Initiate the class with either (a) passing a dictionary of companies as keys
    and companies TrustPilot id as items or (b) adding them with dictionary syntax.

    e.g. a. ```python
            id_dict = {'Skat':'470bce96000064000501e32d','DR':'4690598c00006400050003ee'}
            d = GetReviews(id_dict)

            # This ids dictionary can be loaded from text files e.g.
            lines = np.genfromtxt('companies_ids.csv', delimiter=',',
                                     dtype=str,skip_header=1) #skipped header
            csv_dict = {key:item for key, item in lines} 
         ```
         b. ```python
            d = GetReviews()
            d['Skat'] = '470bce96000064000501e32d'
            ``` 
    To get TrustPilot's company id, open www.trustpilot.com on your browser
    right click to inspect the page, then select Network. Search the name
    of the company on TrustPilot webpage. Filter: json
    https://www.trustpilot.com/review/IDISHERE/jsonld
   

2. Gather Data 
    You can pass in different language e.g. Norwegian. Default is 'dk'
    ```python
    retured_dict = d.gather_data('no')
    ```
3. Save Data
    You can pass location and file_name. Default is pwd and 'TrustPilotData' as name
    ```python
    d.save_data()
    ```
4. Reading data
    ```python
    df = pd.DataFrame(returned_dict)
    ```
    or
    ```python
    df = pd.DataFrame(d.dictData)
    ```
    or from stored source

    ```python
    df = pd.read_pickle('TrustPilotData.pkl', compression='gzip')
    ```
# A full example:

```python
import numpy as np
from tpreviews import GetReviews


# Dictionary from Data 
lines = np.genfromtxt('companies_ids.csv', delimiter=',',
                      dtype=str, skip_header=1)
csv_dict = {key: item for key, item in lines}

d = GetReviews(csv_dict)
d.gather_data('no') # Get Norwegian Reviews
d.save_data(file_name='NoTrustPilotData')
```

#TODOs:
    *Allow different saving formats e.g. df.to_XXX
    *Add more features
    *Write a better documetation


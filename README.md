# TrustPilotReader
Unofficial TrustPilot reviews collector. For Academic Use Only. READ: [TrustPilot Terms of Use](https://legal.trustpilot.com/end-user-terms-and-conditions)

# Disclamer:
You, and you alone, are responsible for following TrustPilot terms and using this tool to gather their data. Respect
their servers and be thoughtful when gathering large amount of data. 


# Unmatured Documetation :)

This code implements basic data scraping of TrustPilot [default:Danish] Reviews .

It is a prototype to be used for academic reasons only.
TrustPilot offers APIs to gather their data
 

# How to use it:

# 1. Initiat Class 

Initiate the class with either (a) passing a dictionary of companies as keys
and companies TrustPilot id as items or (b) adding them with dictionary syntax.

e.g.
```python
            # way a
            id_dict = {'Skat':'470bce96000064000501e32d','DR':'4690598c00006400050003ee'}
            d = GetReviews(id_dict)

            # ids dictionary can be loaded from text files e.g.
            lines = np.genfromtxt('companies_ids.csv', delimiter=',',
                                     dtype=str,skip_header=1) #skipped header
            csv_dict = {key:item for key, item in lines}
            d = GetReviews(csv_dict)
            
            # way b 
            d = GetReviews()
            d['Skat'] = '470bce96000064000501e32d'
```
        

To get TrustPilot's company id, open www.trustpilot.com on your browser,
right click to inspect the page, then select Network. Search the name
of the company on TrustPilot webpage. Filter: json. Seee IDISHERE:

https://www.trustpilot.com/review/IDISHERE/jsonld   

## 2. Gather Data

You can pass in different language e.g. Norwegian. Default is 'dk'
```python
    retured_dict = d.gather_data('no')
 ```
## 3. Save Data

You can pass location and file_name. Default is pwd and 'TrustPilotData' as name
```python
    d.save_data()
```
## 4. Reading Data

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

# TODOs:
   * Allow different saving formats e.g. df.to_XXX
   * Split page_review funciton into connection and data parsing (better way to handler bad requests)
   * Add more features
   * Write a better documetation

## [TrustPilot Terms of Use](https://legal.trustpilot.com/end-user-terms-and-conditions)

![c091684c-879c-4d6e-90c6-92fbc53cb676](https://user-images.githubusercontent.com/14926709/43354373-980e2882-924b-11e8-8b85-237f3e4b1dde.jpeg)

# TrustPilotReader
Unofficial TrustPilot reviews collector. For Academic Use Only. READ: [TrustPilot Terms of Use](https://legal.trustpilot.com/end-user-terms-and-conditions)

# Disclamer:
You, and you alone, are responsible for following TrustPilot terms and using this tool to gather their data. Respect
their servers and be thoughtful when gathering large amount of data. 


# Unmatured Documetation :)

This code implements basic data scraping of TrustPilot [default:Danish] Reviews .

It is a prototype to be used for academic reasons only.
TrustPilot offers APIs to gather their data
 
# Get it from PyPI
```bash
pip install trustpilotreviews
```


# How to use it:

Import package

```python
from trustpilotreviews import GetReviews
```

# 1. Initiat Class 

Initiate the class with either (a) passing a dictionary of companies as keys
and companies TrustPilot id as items or (b) adding them with dictionary syntax.

e.g.
```python
# way a: Using dictionary with business ids
id_dict = {'Skat':'470bce96000064000501e32d','DR':'4690598c00006400050003ee'}
d = GetReviews(id_dict)

# ids dictionary can be loaded from text files e.g.
lines = np.genfromtxt('data/business_ids.csv', delimiter=',',
                            dtype=str,skip_header=1) #skipped header
csv_dict = {key:item for key, item in lines}
d = GetReviews(csv_dict)

# way b: Using dictionary assignment 
d = GetReviews()
d['Skat'] = '470bce96000064000501e32d'
```
        
No business ids, no problem:

```python
from trustpilotreviews import GetReviews

# Initiate it. Language will be required
t = GetReviews()

# Pass in web-page address as it appears in trustpilot.com
mate_id = t.get_id('www.mate.bike')

# Check if everything is ok
if mate_id.ok:
    print(mate.business_id)

# Gather data from that id
data = t.get_reviews() 
    
 ```
 
 Having multiple websites, well, no problem:
 
 ```python
from trustpilotreviews import GetReviews

t = GetReviews()

# pass multiple web-pages as a list
ids = t.get_ids(['www.ford.dk','www.mate.bike'])

print(ids) # same as print(t) as ids are added to que

# gather data for those ids  
data = t.get_reviews()   
 ```

Want to save it on a database instead of Pandas, done:

 ```python
from trustpilotreviews import GetReviews

t = GetReviews()
ids = t.get_ids(['www.ford.dk','www.mate.bike'])

# mine data for those ids 
t.get_reviews()

# send them to in memory database
t.send_db('../data/','reviews')   
 ```
 
 
## 2. Reading Data


```python
df = pd.DataFrame(t.dictData)
```
or from stored source

```python
df = pd.read_pickle('TrustPilotData.pkl')
```
# A full example:

```python
import numpy as np
from trustpilotreviews import GetReviews


# Dictionary from Data 
lines = np.genfromtxt('companies_ids.csv', delimiter=',',
                      dtype=str, skip_header=1)
csv_dict = {key: item for key, item in lines}

d = GetReviews(csv_dict) # Select no for Norwegian Reviews
d.gather_data()

# Saves as pandas dataframe pickle
d.save_data(file_name='NoTrustPilotData')
```

# TODOs:
   * Allow different saving formats e.g. df.to_XXX
   * Split page_review funciton into connection and data parsing (better way to handler bad requests)
   * Add more features
   * Write a better documetation

## [TrustPilot Terms of Use](https://legal.trustpilot.com/end-user-terms-and-conditions)

![c091684c-879c-4d6e-90c6-92fbc53cb676](https://user-images.githubusercontent.com/14926709/43354373-980e2882-924b-11e8-8b85-237f3e4b1dde.jpeg)

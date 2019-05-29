Using if.dk as example

Two way get data:

Using requests 
Get business_id

    import requests

    business_id = '4cbaa4df000064000104ab29'
    URL = f'https://dk.trustpilot.com/review/{business_id}/jsonld'
    params = {'page':1}

    r = requests.get(URL, params=params)
    print(r.json())

Using HTLM Dom( requests and BeautifulSoup) 

#e.g.

    import json
    from requests import Session
    from bs4 import Beautiful
    URL = 'https://dk.trustpilot.com/review/www.if.dk'

    session = Session()
    r = session.get(URL)
    soup = BeautifulSoup(r.text)
    data = soup.find('script',{'type':'application/ld+json'})
    print(json.loads(data.getText(strip=True)[:-1]))



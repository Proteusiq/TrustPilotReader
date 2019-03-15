import numpy as np
from get_reviews import GetReviews

comp_dict = {'Mate': '587381110000ff00059a7856',
             'Spigo': '46d2b21a0000640005009a08'}

# Initiating with dictionary
t = GetReviews(comp_dict, language='dk')

#Using Default values
t.get_reviews()
t.send_db('../data/','reviews')

 # Get Norwegian Reviews
#t.save_data(file_name='../data/dkTrustPilotData')

# Dictionary from Data 
# lines = np.genfromtxt('companies_ids.csv', delimiter=',',
#                       dtype=str, skip_header=1)
# csv_dict = {key: item for key, item in lines}

# d = GetReviews(csv_dict)
# d.gather_data('no') # Get Norwegian Reviews
# d.save_data(file_name='data/NoTrustPilotData')
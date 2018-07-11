import numpy as np
from tpreviews import GetReviews

comp_dict = {'Mate': '587381110000ff00059a7856',
             'Spigo': '46d2b21a0000640005009a08'}

# Initiating with dictionary
#t = GetReviews(comp_dict)

#Using Default values
#t.save_data()

# Dictionary from Data 
lines = np.genfromtxt('companies_ids.csv', delimiter=',',
                      dtype=str, skip_header=1)
csv_dict = {key: item for key, item in lines}

d = GetReviews(csv_dict)
d.gather_data('no') # Get Norwegian Reviews
d.save_data(file_name='NoTrustPilotData')


from TrustPilot import GetReviews

comp_dict = {'Mate': '587381110000ff00059a7856',
             'Spigo': '46d2b21a0000640005009a08'}

# Initiating with dictionary
t = GetReviews(comp_dict)

#Using Default values
t.save_data()
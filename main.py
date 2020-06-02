from gsp import GSP
threshold = 5 # minimum support
level = 3 # number of levels for GSP
g = GSP(threshold, './Data_GSP/')
g.get_support_items(level)

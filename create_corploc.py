import os


cwd = os.getcwd()
corpus_location = cwd + '/lyrics/'


with open('corp_loc.txt', 'w') as f:
    f.write(corpus_location)

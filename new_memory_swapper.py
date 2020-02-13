#!\Users\fleke\pythonstuff env python

import re
# e3wdeimport qb

sample_dict = {'123456':'40480'}
sample_job = {'id':'123456', 'reservations':'host.total=3, host=nuke', 'requirements':'nuke=1'}

keys = sample_dict.keys()
values = sample_dict.values()

re_req_searcher = re.findall(r'\d{4,6}', sample_job['requirements'])

if len(re_req_searcher) == 0:
    req_placer = str(sample_job['requirements']) + ', host.memory.total>' + str(sample_dict['123456'])
    sample_job['requirements'] = req_placer
elif len(re_req_searcher) == 1:
    if re_req_searcher[0] == 
re_req_sub = re.sub(r'\d{4,6}', str(sample_dict['123456']), str(sample_job['requirements']))
print(re_req_sub)

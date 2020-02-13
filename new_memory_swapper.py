#!/amay/bin/env python2.7

import re
import qb

sample_dict = {123456:40480}
sample_job = {'id':123456, 'reservations': 'host.total=3, host=nuke', 'requirements':'nuke=1, host.memory.total>42802'}

keys = sample_dict.keys()
values = sample_dict.values()

re_req_finder = re.findall(r'\d{4,6}', sample_job['requirements'])

if len(re_req_finder) == 0:
        from_scratch_req = sample_job['requirements'] + ', host.memory.total>' + str(sample_dict[123456])
        print from_scratch_req
        #qb.modify({'requirements':from_scratch_req}, jobid)
elif len(re_req_finder) == 1:
        if re_req_finder[0] == sample_dict[123456]:
                print simple_dict[123456]
                print 'Correct!'
        elif re_req_finder[0] != sample_dict[123456]:
                re_req_substituter = re.sub(r'\d{4,6}', str(sample_dict[123456]), sample_job['requirements'])
                print 'Incorrect.'
                print re_req_substituter
                #qb.modify({'requirements':re_req_substituter}, jobid)

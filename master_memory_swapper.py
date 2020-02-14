#!/****/bin/env python 2.7.5

import qb
import __future__
import re
from os import listdir
from os.path import isfile, join
import sys
import time
import argparse

#######################################3

ACTIVE = ['running']
jobs = qb.jobinfo(status=ACTIVE, agenda=True, subjobs=True)

id_list = []

for j in jobs:
    if j['subjobs'][0]['status'] == 'running':
        if j['todotally']['failed'] > 0:
            id_list.append(j['id'])

iter_list = [ i // 1000 * 1000 for i in id_list]
iter_list = sorted(list(dict.fromkeys(iter_list)))

job_family = {}

for iterable in iter_list:
    for i in id_list:
        prop_i = i // 1000 * 1000
        if prop_i == iterable:
            job_family.setdefault(iterable,[]).append(i)

print job_family

path = '/renders/render_logs/job/'
out_files = []
memory_dict = {}

SIG_finder = re.compile(r"SIGSEGV")
error_finder = re.compile(r"\d{6}?(?=MB ERROR)")
time_list = []

for i in job_family:
    error_list = []

    for job_id in job_family[i]:
        start_time = time.time()
        path_new = path + str(i) + '/' + str(job_id)
        dir_files = [f for f in listdir(path_new) if isfile(join(path_new, f))]

        for k in dir_files:
            if '.out' in k:
                out_file_text = open(path_new + '/' + k).read(5 * 10 ** 7) # arbitrary memory limit
                if(SIG_finder.search(out_file_text)):
                    all_error_list = list(map(int, error_finder.findall(out_file_text)))
                    if all_error_list:
                        all_error_list.sort(reverse = True)
                        error_list.append(all_error_list[0])

        if error_list:
            error_list.sort(reverse = True)
            memory_dict.setdefault(job_id, int(error_list[0] * 1.1 // 1000 * 1000))

        job_time = time.time()-start_time
        time_list.append(time.time()-start_time)

print 'This is our target dictionary: ',
print memory_dict

for k, v in memory_dict.items():
    print k, v

####################################

for jobid in memory_dict.keys():
    target_job_obj = qb.jobinfo(id=jobid) # generates iterable job object.
    re_req_finder = re.findall(r'\d{4,6}', target_job_obj[0]['requirements'])
    if len(re_req_finder) == 0: # add requirement line entirely
        scratch_req_builder = target_job_obj[0]['requirements'] + ', host.memory.total>', str(memory_dict[jobid])
        print scratch_req_builder
        #qb.modify({'requirements':scratch_req_builder}, jobid)
    elif len(re_req_finder) == 1:
        if re_req_finder[0] == memory_dict[jobid]:
            print target_job_obj[0]['requirements']
        elif re_req_finder[0] != memory_dict[jobid]: # replace memory with correct number
            sub_req_builder = re.sub(r'\d{4,6}', str(memory_dict[jobid]), target_job_obj[0]['requirements'])
            print sub_req_builder
            #qb.modify({'requirements':sub_req_builder}, jobid)

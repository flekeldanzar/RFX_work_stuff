#!/amay/bin/env python

import qb
import __future__
import re
from os import listdir
from os.path import isfile, join
import sys
import time
import argparse
#########################################

ACTIVE = ['running']
jobs = qb.jobinfo(status=ACTIVE, agenda=True, subjobs=True)
'''
parser = argparse.ArgumentParser(description='Find Memory Allocation Errors in work.')
parser.add_argument('')
'''
#########################################

# parse down target jobs by confirming failed frames

# initialize empty list which will hold iterable running ids. this will eventually hold only FAILING ids
id_list = []

# iterates over jobs and finds important information: reservation/requirement, jobid, subjob status
for j in jobs:
    
    #print j['subjobs'][0]['status']
    if j['subjobs'][0]['status'] == 'running':
        if j['todotally']['failed'] > 0:
            id_list.append(j['id'])


#print id_list

# from our id_list, we will now generalize the top and bottom id floors, and create
# another list incrementing all reference idfloors by 1000.

iter_list = [i // 1000 * 1000 for i in id_list]
iter_list = sorted(list(dict.fromkeys(iter_list))) # is there a better way to create a sorted list without data-type conversion?
#iter_list = range(proper_list[0], proper_list[1], 1000)

#print iter_list

########################################

# the following code is intended to construct a dictionary for easy referencing during
# our outlog directory searches. the iter_list (job floors) will act as keys, and the id_list (jobid)
# will act as the associated values. Ex: job_family = {floor_A:[job_a, job_b], floor_B:[job_c, job_d], ... }

job_family = {} # our 'job family' which will be used for organized searching

for iterable in iter_list:
    # job_family[it] = [] # generates a key named by job floor, with values of an empty list.
    
    for i in id_list: # for each jobid in list of jobids...
        prop_i = i // 1000 * 1000 #int(str(i)[:3] + '0' * 3)
        #print prop_i
        #print job_family.keys()
        if prop_i == iterable:
            # job_family[it].append(i)
            job_family.setdefault(iterable,[]).append(i)

    #print prop_i[:3]

#print job_family # This list will be used for most subsequent computations.

##############################################

# the following code will attempt to manipulate a path by taking advantage of the formatting of
# the job_family dictionary. Afterwards, it will parse down the listed directed to exclusively .out files, and
# finally, it will run a read on the content of each file with the goal of obtaining a SIGSEGV|ABRT error
# and storing the associated memory value as a variable.

path = '/renders/render_logs/job/'
out_files = []
memory_dict = {}

SIG_finder = re.compile(r"SIGSEGV")
error_finder = re.compile(r"\d\d\d\d\d\d?(?=MB ERROR)") # Might need to be generalized to accept any digit span.
time_list = []
for i in job_family:  # Family level that contains the first 3 of the job family
    error_list =[]  
    for job_id in job_family[i]:  # The actual job number id
	start_time = time.time()
        path_new = path + str(i) + '/' + str(job_id)
        dir_files = [f for f in listdir(path_new) if isfile(join(path_new, f))]
        
        for k in dir_files: # this code is ugly, but gets the job done	  
            if '.out' in k:	      
	      out_file_text = open(path_new + '/' + k).read(5 * 10**7) # memory limit on the read can be changed.
	      
              if(SIG_finder.search(out_file_text)):		
		all_error_list = list(map(int, error_finder.findall(out_file_text)))
		if all_error_list:
		  all_error_list.sort(reverse = True)
		  error_list.append(all_error_list[0])

	if error_list:
	  #print error_list
	  error_list.sort(reverse = True)
	  memory_dict.setdefault(job_id, int(error_list[0] * 1.1 //1000 * 1000)) # The arithmatic is  arbitrary, will change.
	
	job_time = time.time()-start_time
	#print job_time #toggle to view overall computation time
	time_list.append(time.time()-start_time)            

print 'This is our target dictionary: ',
print memory_dict

for i, k in memory_dict.items():
    print i, k


##########################

# The final step of this program will be to take the key and value portions of our memory_dict and insert them in some
# function (like qb.modify(<jobid>, 'reservations')) in order to automate the process of changing the memory requirements
# to some required minimum to prevent errors. The following code will just show an example of a dummy function which
# does something like what is outlined above with our memory_dict:

for jobid in memory_dict.keys():

    target_job_obj = qb.jobinfo(id=jobid) # generates iterable job object. It is a list of a single class.

    if target_job_obj[0]['cluster'] == '/nuke': # exclusively for handling /nuke jobs.
        nuke_req_checker = re.findall(r'host.memory.total>', target_job_obj[0]['requirements'])
	nuke_reserv_checker = re.findall(r'host.memory=', target_job_obj[0]['reservations'])
	if len(nuke_req_checker) == 0:
            req_nuker  = target_job_obj[0]['requirements'] + ', host.memory.total>' + str(memory_dict[jobid])
            qb.modify({'requirements':req_nuker}, jobid)
	if len(nuke_reserv_checker) == 0:
	    reserv_nuker = target_job_obj[0]['reservations'] + ', host.memory=' + str(memory_dict[jobid])
	    qb.modify({'reservations':reserv_nuker}, jobid)
	print req_nuker
	print reserv_nuker
    
    else:
        re_req_finder = re.findall(r'\d{4,6}', target_job_obj[0]['requirements'])

        if len(re_req_finder) == 0: # add requirement line entirely
            scratch_req_builder = target_job_obj[0]['requirements'] + ', host.memory.total>', + str(memory_dict[jobid])
            print 'Changing ' + target_job_obj[0]['requirements'] + ' to: ' + scratch_req_builder
            qb.modify({'requirements':scratch_req_builder}, jobid)
        elif len(re_req_finder) == 1:
            if re_req_finder[0] == memory_dict[jobid]:
                #print target_job_obj[0]['requirements']
                pass
            elif re_req_finder[0] != memory_dict[jobid]: # replace memory with correct number
                sub_req_builder = re.sub(r'\d{4,6}', str(memory_dict[jobid]), target_job_obj[0]['requirements'])
                print 'Changing ' + target_job_obj[0]['requirements'] + ' to: ' + sub_req_builder
                qb.modify({'requirements':sub_req_builder}, jobid)

        re_reserv_finder = re.findall(r'\d{4,6}', target_job_obj[0]['reservations'])

        if len(re_reserv_finder) == 0:
            scratch_reserv_builder = target_job_obj[0]['reservations'] + ', host.memory=', str(memory_dict[jobid])
            print 'Changing ' + target_job_obj[0]['reservations'] + ' to: ' + scratch_reserv_builder
            qb.modify({'reservations':scratch_reserv_builder}, jobid)
        elif len(re_reserv_finder) == 1:
            if re_reserv_finder[0] == memory_dict[jobid]:
                #print target_job_obj[0]['reservations']
                pass
            elif re_reserv_finder[0] != memory_dict[jobid]:
                sub_reserv_builder = re.sub(r'\d{4,6}', str(memory_dict[jobid]), target_job_obj[0]['reservations'])
                print 'Changing ' + target_job_obj[0]['reservations'] + ' to: ' + sub_reserv_builder
		qb.modify({'reservations':sub_reserv_builder}, jobid)

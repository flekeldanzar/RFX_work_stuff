#! <header here>

import re
import qb

###########################

target_memory = 40480
re_requirements = re.findall(r'\d{4,6}'
re_reservations = re.findall(r'\d{4,6}'
# dictionary yielded from previous code. All keys are jobid, all values are optimal memory allocation in MB.
sample_dict = {
  123456:20480
  }

# partial list of headers commonly found in jobs from qb.jobinfo(blahblahblah)...
sample_job =  {
  'id':123456,
  'reservations':'host=nuke',
  'requirements':'host.total=3'
  }

for k, v in sample_job.items():
 

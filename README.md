# RFX_work_stuff
Various python/bash/tcsh code useful for sorting through Qube! databases.

Hi.

The following repository is exclusively for the purposes of experimenting with various python/bash/tcsh scripts useful within the scope of
parsing through frame data organized by the Qube! render farm manager. Should any kind stranger choose to overview the cobbled together code found within this repository and provide constructive insight, I would recommend downloading the qb module from pipelineFX,since nearly every python-based script will require it to function.

For security purposes, all variables which reference job id's, titles, cluster information, etc. will be purely fictional. Most variables are constructed specifically for targeted experimentation and should therefore be viewed as drastically simplified in comparison to their actual real life counterparts.

For those of you who have read to this point, the following list is comprised of ideas I would like to see set in motion, in order of importance. Anything with a single greater-than (>) will indicate that the project is started, a double greater-than (>>) means the project is nearly completed but needs 'formalization', an exclamation point (!) means the project has been successfully completed, and a (x) means the project is currently unapproachable with my current knowledge.

1. Automate the updating of reservations/requirements for SIGABRT/SIGSEGV flags in outlog files. (>)
2. Automate searching for failed frames (black frames) in RV. ()
3. Track and enumerate frame retries on independent job ID. (>>)


-flek

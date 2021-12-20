import sys
import time
import socket
import os
import queue
import multiprocessing	

import state
import controlSimple

import numpy as np
import argparse
from datetime import datetime


###############################################################

#! This is the main script in the python threading introduction framework.

#! NOTE every example here will have a main script

###############################################################



start_time = datetime.now()

#! Initialize the controller class thread
control_thread = controlSimple.Controller(start_time)

#! Initialize the threads list
threads = []
threads.append(control_thread) # add the control thread to the threads list


#! Start the control thread
#
#  Note since we append control_thread to the threads list, they are both looking
#  at the same memory location. Thus, what we do to contorl_thread we are in effect
#  doing to threads['control_thread'], and vice versa.
control_thread.start()
print("Start Control")



#! Define a function that checks to see if the threads in the threads list are
#  still running.
def hasLiveThreads(threads):
    return True in [t.is_alive() for t in threads]


#! Start while loop that will run constantly until our threads have been destroyed,
#  which is done by using a keyboard interrupt.
while hasLiveThreads(threads):
    try:
        [t.join(1) for t in threads
         if t is not None and t.is_alive()] #! this basically joins the seperate threads
                                            #  with the main thread which basically
                                            # destroys the other threads. (Still trying to figure
                                            #                             out exactly what it does)
    except KeyboardInterrupt:
        print("Killing threads")
        for t in threads:
            t.stop()


print("Exiting Main")

import sys
import time
import socket
import os
import queue
import multiprocessing	

import state
import controlSimple
import logger

import numpy as np
import argparse
from datetime import datetime


###############################################################

#! This is the main script in the python threading introduction framework.

#! NOTE every example here will have a main script

###############################################################




log_path = '' # Define the log path. Be sure to update this value or you might get an error!!!!!
              #        Note: '' will log in the current folder
num_vehicle = 1 # Number of "basic vehicles" to be logged
my_id = 1


start_time = datetime.now()


#! Initialize the queues
log_queue = multiprocessing.Queue() # Initialize the logging queue


#! Initialize the controller class thread
control_thread = controlSimple.Controller(start_time, log_queue)

#! Initialize the logging class thread
file_suffix = '_v' + str(int(my_id))
logging_thread = logger.Logger(log_queue, log_path, num_vehicle, start_time, file_suffix)


#! Initialize the threads list
threads = []
threads.append(control_thread) # add the control thread to the threads list
threads.append(logging_thread) # add the logging thread to the threads list

#! Start the control thread
#
#  Note since we append control_thread to the threads list, they are both looking
#  at the same memory location. Thus, what we do to contorl_thread we are in effect
#  doing to threads['control_thread'], and vice versa.
control_thread.start()
print("Start Control")


#! Start the logging thread
logging_thread.start()
print("Started Logging")





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

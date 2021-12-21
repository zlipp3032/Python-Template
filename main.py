import sys
import time
import socket
import os
import queue
import multiprocessing	

from state import *
import logger

import numpy as np
import argparse
from datetime import datetime


###############################################################

#! This is the main script in the python logging introduction framework.

#! We aim to create a .csv file and log data to it in a loop like fashion.

###############################################################




log_path = '' # Define the log path. Be sure to update this value or you might get an error!!!!!
              #        Note: '' will log in the current folder
num_vehicle = 1 # Number of "basic vehicles" to be logged
my_id = 1  # Unique identifier of each vehicle.


start_time = datetime.now()


#! Initialize the logging class thread
file_suffix = '_v' + str(int(my_id))

#logging_thread = logger.Logger(log_queue, log_path, num_vehicle, start_time, file_suffix)



this_state = FullVehicleState()


Ts = 0.02
num_loops = 100
counter = 0
#! Main control loop. We use the threading.Event() function as our control parameter
#  for this loop.
while(counter < num_loops ):
    loop_start_time = datetime.now()
    counter += 1
    print("Counter: ", counter)
    
    ######################################################
    #! Do loop stuff here



    
    ######################################################
    
    
    time_to_wait = max(Ts - (datetime.now() - loop_start_time).total_seconds(),1E-6)
    print("time 2 wait:", time_to_wait)            
    print("Press ctrl-c to kill this thread. \n\n")
    time.sleep(time_to_wait)







print("Exiting Main")

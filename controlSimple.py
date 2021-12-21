import time
import logging
from state import *
import os
import queue
import threading
import recordtype
import math as m
from numpy import linalg as LA
from datetime import datetime, timedelta
import numpy as np
import copy
import json


###############################################
#! This is the main control thread class, where the main flight control loop is running.

#! In this version of the code, we simply run a timed loop at a constant set sampling frequency.

#! We print the loop number and the time_to_wait variable. We compare the time_to_wait
#  variable to the set loop time (self.Ts) to ensure the the loop is running at our
#  desired rate. 

###############################################

#! Initialize the controller thread
class Controller(threading.Thread):
    def __init__(self, start_time, log_queue ): #If you want to have an input to this class initializstion, put it here. 
        threading.Thread.__init__(self)
        
        self.start_time = start_time
        self.Ts = 0.1 # Loop time
        

        self.vehicle_state = FullVehicleState() # Set the self.vehicle_state parameter as the
                                                #     FullVehicleState() class from state.py
        self.vehicle_state.start_time = datetime.now() # Set the start time for vehicle_state     
        self.log_queue = log_queue # Set the logging queue for the class as the same memory addresss of the main log_queue
        self.stop_request = threading.Event()
 
        
    #! Set the stop class function
    def stop(self):
        self.stop_request.set()
        print("Stop flag set - Control")


    #! Set the run class function. This is where the main control loop resides! You can call
    #  other functions from this main loop. This will be shown in other examples.
    def run(self):
        #! Main control loop. We use the threading.Event() function as our control parameter
        #  for this loop.
        while(not self.stop_request.is_set()):
            loop_start_time = datetime.now()
            self.vehicle_state.counter += 1
            print("Counter: ", self.vehicle_state.counter)

            ######################################################
            #! Do loop stuff here
            self.PushToLoggingQueue()

            ######################################################
            
            
            time_to_wait = max(self.Ts - (datetime.now() - loop_start_time).total_seconds(),1E-6)
            print("time 2 wait:", time_to_wait)            
            print("Press ctrl-c to kill this thread. \n\n")
            time.sleep(time_to_wait)

        self.stop()
        print("Control Stopped")





    def PushToLoggingQueue(self):
        msg = Message()
        msg.type = 'UAV_LOG'
        msg.send_time = time.time()
        msg.content = {}
        msg.content['this_state'] = copy.deepcopy( self.vehicle_state )
        #msg.content['other_states'] = copy.deepcopy( self.state_vehicles )
        self.log_queue.put( msg )

        





        

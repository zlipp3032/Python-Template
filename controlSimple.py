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

#! In this version of the code, we build off of the previous branch on the github (thread_intro).

###############################################

#! Initialize the controller thread
class Controller(threading.Thread):
    def __init__(self, start_time, log_queue ): #If you want to have an input to this class initializstion, put it here. 
        threading.Thread.__init__(self)
        
        self.start_time = start_time
        self.Ts = 0.1 # Loop time
        self.stop_request = threading.Event()
        self.vehicle_state = FullVehicleState() # Set the self.vehicle_state parameter as the
                                                #     FullVehicleState() class from state.py
        self.vehicle_state.start_time = datetime.now() # Set the start time for vehicle_state

        #! Create the log queue in the controller class
        self.log_queue = log_queue # Set the logging queue for the class as the same memory addresss of the main log_queue
        
    #! Set the stop class function
    def stop(self):
        self.stop_request.set()
        print("Stop flag set - Control")


    #! Set the run class function. This is where the main control loop resides! You can call
    #  other functions from this main loop.
    def run(self):
        #! Main control loop. We use the threading.Event() function as our control parameter
        #  for this loop.
        while(not self.stop_request.is_set()):
            loop_start_time = datetime.now()
            self.vehicle_state.counter += 1
            print("Counter: ", self.vehicle_state.counter)

            ######################################################
            #! Do loop stuff here

            #! Push the current self.vehicle_state to the logging queue
            #  by calling the control class' function PushToLoggingQueue
            self.PushToLoggingQueue() # Note: Notice that we use 'self.'
                                      #       This is because it is the control class' function. We can remove
                                      #       this by making the this functino a global function.

            ######################################################
            
            
            time_to_wait = max(self.Ts - (datetime.now() - loop_start_time).total_seconds(),1E-6)
            print("time 2 wait:", time_to_wait)            
            print("Press ctrl-c to kill this thread. \n\n")
            time.sleep(time_to_wait)

        self.stop()
        print("Control Stopped")




        
    #! This function places the current state of the vehicle to the logging queue
    def PushToLoggingQueue(self):
        #! Initiate the message variable
        msg = Message() 
        msg.type = 'UAV_LOG'
        msg.send_time = time.time()
        msg.content = {}

        #! Note that we use a deepcopy of the vehicle state. This basically means we are creating
        #  a new heap of memory and storing the data at the current memory address at this new
        #  memory address with no strings attached.
        msg.content['this_state'] = copy.deepcopy( self.vehicle_state )
        #msg.content['other_states'] = copy.deepcopy( self.state_vehicles ) # This is will be needed when we use communication

        #! Push the current message (msg) to the logging queue
        self.log_queue.put( msg )

        





        

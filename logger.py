import collections
from state import *
import socket
import queue
import logging
import multiprocessing
import os
import time
from datetime import datetime
import signal
import copy


###############################################
#! This is the logging class thread.

#! We use the multiprocessing library to create a new process thread on the CPU for logging data.
#  This is to promote putting more processing time in the control loop itself.    this

###############################################

#! Initialize the logging thread
class Logger(multiprocessing.Process):
    def __init__(self, log_queue, log_path, n, start_time, file_suffix):
        multiprocessing.Process.__init__(self)
        self.log_queue = log_queue
        self.stop_request = multiprocessing.Event()
        self.expected_MAVs = n #! This value is the number of agents that are in each experiment. MAV
                               #  stands for 'micro air vehicle' and is a specific type of message
                               #  protocol that is sent by each UAV
        self.start_time = start_time

        #! Create the file. We use the current YYMMDD__HHMMSS format. We log as CSV file
        self.file = open(os.path.join(log_path, self.start_time.strftime('%Y_%m_%d__%H_%M%S_log') + file_suffix + '.csv'), 'w' )
        self.header_written = False
        self.last_logged = 0
        self.num_items_per_self = 0 # Number of items to log for myself
        self.num_items_per_other = 0 # Number of items to log for other vehicles (i.e., these pertain to BasicVehicleState() )


        

    def stop(self):
        self.stop_request.set()
        print('Stop flag set - Log')


        
    def run(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        while( not self.stop_request.is_set() ):    #! Not sure why we use two loops here, but we do.
            while( not self.stop_request.is_set() ):
                try:
                    #! Check to see if there are any messages in the queue
                    msg = self.log_queue.get(True, 0.5)

                    #! If there is a messge in the queue, we send it to the logging function
                    self.LogMessage(msg)

                #! If the queue is empty, we just wait a millisecond and try again.
                #  "If you get knocked down, then get back up again, cause nothing should ever bring you down!" --Chumba Wumba
                except queue.Empty :
                    time.sleep(0.001)
                    break

        #! Flush the file and close it. Note if we don't properly close the file, it may not write any readble data to the disk.        
        self.file.flush()
        os.fsync( self.file.fileno() )
        self.file.close()
        print( 'Log Stopped.' ) 
            


    #! Log message 
    def LogMessage(self, msg):
        #state_vehicles = msg.content['other_states']
        this_state     = msg.content['this_state']
        #print(this_state.GetCSVLists().keys()) # for debugging
        if not self.header_written:
            self.WriteHeaderString( this_state )
            self.header_written = True

        out_string  = str( datetime.now() ) + ','
        out_string += str( (datetime.now() - this_state.start_time).total_seconds() ) + ',' #! relative time since start
                                                                                            #! I think python handles thread timing
                                                                                            #   differently than c/c++, this is why we
                                                                                            #   are able to compute the relative time
                                                                                            #   this way. But I also have no idea. -Zack

        #! This sets the msg,content values to the correct CSV string.
        out_string += ','.join( map( str, this_state.GetCSVLists().values() ) )
        out_string += '\n'

        #! Write the full csv string to the file.
        #  This could probable be done in a binary format which would increase speed and memory usage.
        self.file.write( out_string )



    #! This function creates the headers based on the values we want to log in the state.py headers values.
    def WriteHeaderString( self, this_state ):
        header_string =  ''
        header_string += 'time,rel_time'
        n = self.expected_MAVs # see above

        #! Convert the headers odict type to a list
        this_list = list(this_state.GetCSVLists().keys())

        #! Number of items to be logged
        self.num_items_per_self = len( this_list ) # This can be used in the log message function

        #! Put each header label into the string
        for i in range(0,self.num_items_per_self):
            header_string += ',' + this_list[i]

        header_string += '\n'

        #! Write the header string to the CSV file
        #print(header_string) # For debuggin --- If you want to make sure you are able to see what the headers are
        self.file.write( header_string )
        
        

                                                                    








        

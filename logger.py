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



class Logger(multiprocessing.Process):
    def __init__(self, log_queue, log_path, n, start_time, file_suffix):
        multiprocessing.Process.__init__(self)
        self.log_queue = log_queue
        self.stop_request = multiprocessing.Event()
        self.expected_MAVs = n
        self.start_time = start_time


        self.file = open(os.path.join(log_path, self.start_time.strftime('%Y_%m_%d__%H_%M%S_log') + file_suffix + '.csv'), 'w' )
        self.header_written = False
        self.last_logged = 0
        self.num_items_per_self = 0
        self.num_items_per_pther = 0


        

    def stop(self):
        self.stop_request.set()
        print('Stop flag set - Log')


        
    def run(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        while( not self.stop_request.is_set() ):
            while( not self.stop_request.is_set() ):
                try:
                    msg = self.log_queue.get(True, 0.5)
                    #print(msg) # This is for debugging
                    self.LogMessage(msg)
                except queue.Empty :
                    time.sleep(0.001)
                    break
        self.file.flush()
        os.fsync( self.file.fileno() )
        self.file.close()
        print( 'Log Stopped.' ) 
            

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
                                                                                            #   this way. - Zack

        out_string += ','.join( map( str, this_state.GetCSVLists().values() ) )

        out_string += '\n'
                                                            
        self.file.write( out_string )



    def WriteHeaderString( self, this_state ):
        header_string =  ''
        header_string += 'time,rel_time'
        n = self.expected_MAVs
        this_list = list(this_state.GetCSVLists().keys())
        self.num_items_per_self = len( this_list ) # This can be used in the log message function

        for i in range(0,self.num_items_per_self):
            header_string += ',' + this_list[i]

        header_string += '\n'

        print(header_string)
        self.file.write( header_string )
        
        

                                                                    








        

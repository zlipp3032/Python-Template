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

start_time = datetime.now()

control_thread = controlSimple.Controller(start_time)

threads = []
threads.append(control_thread)

control_thread.start()
print("Start Control")


def hasLiveThreads(threads):
    return True in [t.is_alive() for t in threads]

while hasLiveThreads(threads):
    try:
        [t.join(1) for t in threads
         if t is not None and t.is_alive()]
    except KeyboardInterrupt:
        print("Killing threads")
        for t in threads:
            t.stop()


print("Exiting Main")

# Logging Introduction

This branch builds off of the threads_intro branch. We aim to build a logging thread that will create a .csv file and log our states to it with headers.

# Required Libraries
To run this example code, you will need to install some libraries. You can install the libraries that are not on your computer by using the 'pip install' command. See documentation for installing pip to your computer if it is not already installed. 

Some of the libaries needed to run the code are as follows:
- numpy
- threading
- datetime
- recordtype
- multiprocessing
- queue
- argparse
- json
- copy

Note that some of the libraries that are imported into this code are not used. This is because I am too lazy to go through a figure out which ones we don't need. Just trying to be honest.


# Running the code
- clone the repository
- Navigate to the project root directory
- Change to threads intro branch by running 'git checkout logger_intro'
- Run the command 'python main.py'


# Reading the data
- This can be done in Matlab using 'readtable('path/to/file.csv')
- This can be done in Python using Pandas.read_table('path/to/table').........I think. Haven't tested this, but it is something like this....
- In both instances, you should be able to get to the resepective column of data using the prescribed column headers

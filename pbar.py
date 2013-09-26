#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Super minimal progress bar to monitor long running processes.
    Features:
    - shows the spent time and the estimated time till completion
    - progress bar adapts to length of terminal window

    ## usage example
    from pbar import ProgressBar
    rangevalue = 40
    
    progressbar = ProgressBar(rangevalue, 'explicit update')
    for new_value in range(rangevalue):
        .. do things..
        pbar.update(new_value)    
    
    progressbar = ProgressBar(rangevalue, 'implicit update by 1')
    for i in range(rangevalue):
        .. do things..
        pbar.update()

    code taken from here: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console?lq=1
    and here: http://pypi.python.org/pypi/progressbar/2.2
    
    get the newest version here: https://gist.github.com/shackenberg/3716039
    by Ludwig Schmidt-Hackenberg
"""
import sys
import time
from datetime import timedelta
import os

 
class ProgressBar(object):

    def __init__(self, maxval, title=None):
        self.maxval = maxval - 1 
        self.start_time = time.time()
        self.state = 0
        _, self.ncolumns = os.popen('stty size', 'r').read().split()
        # gets the width of the terminal window
        if title is not None:
            self.title = title + ' '
        else:
            self.title = ''
    
    def update(self, currentval=None):
        if currentval is not None:
            self.state = currentval            
        
        elapsed_time = time.time() - self.start_time
        elapsed_time_pretty = str(timedelta(seconds=round(elapsed_time)))
        
        if elapsed_time > 3:
            estimated_time_left = elapsed_time * (self.maxval / float(self.state) - 1)
            estimated_time_left_pretty = str(timedelta(seconds=round(estimated_time_left)))
            progress = int(round(self.state * 100.0 / self.maxval))
            overhead = 25 + len(elapsed_time_pretty) + len(self.title) + len(estimated_time_left_pretty)
            max_bar_length = int(self.ncolumns) - overhead
            bar_length = progress * max_bar_length / 100
            output_string = '\r{4}[{0}] {1}% in {2} - {3} remaining'.format('#'*bar_length, progress,                                                                             
                                                                            elapsed_time_pretty, 
                                                                            estimated_time_left_pretty, 
                                                                            self.title)
            sys.stdout.write(output_string)
        else:
            progress = int(round(self.state * 100.0 / self.maxval))
            overhead = 35 + len(elapsed_time_pretty) + len(self.title)
            max_bar_length = int(self.ncolumns) - overhead
            bar_length = progress * max_bar_length / 100
            output_string = '\r{3}[{0}] {1}% in {2}'.format('#'*bar_length, progress,
                                                            elapsed_time_pretty, self.title)
            sys.stdout.write(output_string)
        sys.stdout.flush()
        self.state += 1
        if self.state == self.maxval + 1:
            print
 
if __name__ == '__main__':
    ## usage example
    from time import sleep
    rangevalue = 40
    
    progressbar = ProgressBar(rangevalue, 'explicit update')
    for new_value in range(rangevalue):
        sleep(0.1)
        progressbar.update(new_value)    
    
    progressbar = ProgressBar(rangevalue, 'implicit update by 1')
    for i in range(rangevalue):
        sleep(0.1)
        progressbar.update()

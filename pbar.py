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
        try:
            self.ncolumns = self.get_width_of_terminal()
        except:
            self.ncolumns = 80
        if title is not None:
            self.title = title + ' '
        else:
            self.title = ''
        self.time_last_update = 0

    def get_width_of_terminal(self):
        _, ncolumns = os.popen('stty size', 'r').read().split()
        return ncolumns
    
    def update(self, currentval=None):
        if currentval is not None:
            self.state = currentval
        current_time = time.time()
        complete_elapsed_time = current_time - self.start_time
        complete_elapsed_time_pretty = str(timedelta(seconds=round(complete_elapsed_time)))
        time_since_last_update = current_time - self.time_last_update
        if (time_since_last_update > 1) | (self.state == self.maxval):
            if (complete_elapsed_time > 3) & (self.state > 0):
                estimated_time_left = complete_elapsed_time * (self.maxval / float(self.state) - 1)
                estimated_time_left_pretty = str(timedelta(seconds=round(estimated_time_left)))
                progress = int(round(self.state * 100.0 / self.maxval))
                overhead = 25 + len(complete_elapsed_time_pretty) + len(self.title) + len(estimated_time_left_pretty)
                max_bar_length = int(self.ncolumns) - overhead
                bar_length = progress * max_bar_length / 100
                output_string = '\r{4}[{0}] {1}% in {2} - {3} remaining'.format('#'*bar_length, progress,
                                                                                complete_elapsed_time_pretty,
                                                                                estimated_time_left_pretty,
                                                                                self.title)
                sys.stdout.write(output_string)
            else:
                progress = int(round(self.state * 100.0 / self.maxval))
                overhead = 35 + len(complete_elapsed_time_pretty) + len(self.title)
                max_bar_length = int(self.ncolumns) - overhead
                bar_length = progress * max_bar_length / 100
                output_string = '\r{3}[{0}] {1}% in {2}'.format('#'*bar_length, progress,
                                                                complete_elapsed_time_pretty, self.title)
                sys.stdout.write(output_string)

            self.time_last_update = current_time
            sys.stdout.flush()
        self.state += 1
        if self.state == self.maxval + 1:
            print

if __name__ == '__main__':
    ## usage example
    from time import sleep
    example_rangevalue = 40
    example_title_example_one =  'explicit update'
    progressbar = ProgressBar(example_rangevalue, example_title_example_one)
    for new_value in range(example_rangevalue):
        sleep(0.1)
        progressbar.update(new_value)    
    
    example_title_example_two = 'implicit update by 1'
    progressbar = ProgressBar(example_rangevalue, example_title_example_two)
    for i in range(example_rangevalue):
        sleep(0.1)
        progressbar.update()

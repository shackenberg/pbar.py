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

    get the newest version here: https://github.com/shackenberg/pbar.py
    by Ludwig Schmidt-Hackenberg
"""
import sys
import time
from datetime import timedelta
import os

 
class ProgressBar(object):

    def __init__(self, max_value, title=None, start_state=0, max_refeshrate=0.1):
        self.max_value = max_value
        self.start_time = time.time()
        self.state = start_state
        self.lenght = self.automatically_set_length_pbar()
        self.title = self.prepare_title(title)
        self.time_last_update = 0
        self.max_refreshrate = max_refeshrate
        self.is_last_update = False

    def automatically_set_length_pbar(self):
        try:
            return self.get_width_of_terminal()
        except:
            rule_of_thumb_standard_value = 80
            return rule_of_thumb_standard_value

    def get_width_of_terminal(self):
        _, ncolumns = os.popen('stty size', 'r').read().split()
        return ncolumns

    def prepare_title(self, title):
        if title is None:
            return ''
        else:
            return title + ' '

    def update(self, current_value=None):
        self.update_state(current_value)
        current_time = time.time()
        time_since_last_update = current_time - self.time_last_update
        if self.state == self.max_value:
            self.is_last_update = True
        if (time_since_last_update > self.max_refreshrate) | self.is_last_update:
            output_string = self.build_output_string(current_time)
            self.print_pbar(output_string)
            self.time_last_update = current_time
        if self.is_last_update:
            self.jump_to_newline()

    def update_state(self, current_value):
        if current_value is not None:
            self.state = current_value + 1
        else:
            self.state += 1

    def time_div_to_short_str(self, time_div):
        return str(timedelta(seconds=round(time_div)))

    def compute_bar_length(self, overhead, progress):
        max_bar_length = int(self.lenght) - overhead
        return progress * max_bar_length / 100

    def computed_estimate_time_left(self, complete_elapsed_time):
        estimated_time_left = complete_elapsed_time * (self.max_value / float(self.state) - 1)
        return estimated_time_left

    def build_output_string(self, current_time):
        progress = int(round(self.state * 100.0 / self.max_value))
        complete_elapsed_time = current_time - self.start_time
        complete_elapsed_time_pretty = self.time_div_to_short_str(complete_elapsed_time)

        if (complete_elapsed_time > 3) & (self.state > 0):
                estimated_time_left = self.computed_estimate_time_left(complete_elapsed_time)
                estimated_time_left_pretty = self.time_div_to_short_str(estimated_time_left)
                estimated_time_left_pretty_formated = " - " + estimated_time_left_pretty + " remaining"
                len_fillers = 13
        else:
                estimated_time_left_pretty_formated = ''
                len_fillers = 35

        carriage_return = "\r"
        overhead = len_fillers + \
                   len(complete_elapsed_time_pretty) + \
                   len(self.title) + \
                   len(estimated_time_left_pretty_formated)
        bar_length = self.compute_bar_length(overhead, progress)
        progressbar_string = '[' + '#' * bar_length + ']'
        progress_str = " " + str(progress) + "% in "
        complete_elapsed_time_pretty = str(complete_elapsed_time_pretty)

        ordered_output_string_fields = [carriage_return,
                                self.title,
                                progressbar_string,
                                progress_str,
                                complete_elapsed_time_pretty,
                                estimated_time_left_pretty_formated]

        output_string =  "".join(ordered_output_string_fields)
        return output_string

    def print_pbar(self, output_string):
        sys.stdout.write(output_string)
        sys.stdout.flush()

    def jump_to_newline(self):
        print

if __name__ == '__main__':
    ## usage example
    from time import sleep
    example_rangevalue = 40
    example_title_example_one =  'explicit update'
    progressbar = ProgressBar(example_rangevalue, example_title_example_one)
    for new_value in range(example_rangevalue):
        time.sleep(0.1)
        progressbar.update(new_value)

    example_title_example_two = 'implicit update by 1'
    progressbar = ProgressBar(example_rangevalue, example_title_example_two)
    for i in range(example_rangevalue):
        time.sleep(0.1)
        progressbar.update()

    example_title_example_two = 'slow updates'
    example_rangevalue = 4
    progressbar = ProgressBar(example_rangevalue, example_title_example_two)
    for i in range(example_rangevalue):
        time.sleep(3.8)
        progressbar.update()
Super minimal progress bar to monitor long running processes.

Features are:
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

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

root = Tk()

window_label = Label(root, text="Grid Practice")
window_label.grid(row=0, columnspan=2)

cvs = dict([  ##repository for all key placeholder values in the game
    ('dimension', 630),  ##pixels for the active grid
    ('side', 9),  ##number of columns and rows. sidexside = the number of cells
    ('xstart', 0),  ##top left corner starting point for x in window of main game grid
    ('ystart', 0),  ##same for y
    ('xbump', 0),  ##how many cells has the grid grown by on the x axis to encompass the growth of the simulation?
    ('ybump', 0),  ##same for the y axis
    ('reboot', False),
    ##do we need a fresh start to the main simulation in id_changes or to pick up where we left off after the grid grew?
    ('p_original', 0),
    ('p_start', 0),
    ##if rebooting, what was the p starting value when we were in the id_changes + process_changes previously
    ('p_end', 0),  ##same but for p ending - the p values cover the x range of cells surrounding an active cell
    ('q_original', 0),
    ('q_start', 0),  ## same for q starting - the q values cover the y range of cells surrounding an active cell
    ('q_end', 0),  ## same for q ending
    ('s_start', 0),
    ## same for s starting - s values cover the x values for the cells surrounding the p and q cells to see if the p and q cells should activate
    ('s_end', 0),  ##same for s ending
    ('t_start', 0),  ##same for t starting - t are the y values (counterpart to s)
    ('t_end', 0),  ## same for t ending
    ('r_value', 0),  ## if reboot, save the counter value for tracking stuff that is dying
    ('key_value', None),  ## last key called prior to changing the grid size - saving for reboot to start over
    ('u_value', 0),
    ('repeater', False),
    ('continue', True),
    ('u_bool', False),
    ('r_bool', False)
])

x_start = cvs['xstart']  ##x starting point for creating window
y_start = cvs['ystart']  ##same for y
dimension = cvs['dimension']  ## pixel length of game window
x_end = y_end = dimension  ## end of x y ranges in pixels
side = cvs['side']
canvas_manager = Canvas(root, bg="gray", height=dimension, width=dimension)
canvas_manager.grid(row=1, column=0, rowspan=200)


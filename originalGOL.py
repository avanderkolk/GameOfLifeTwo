try:
    from Tkinter import *
except ImportError:
    from tkinter import *

from random import random, randint
from math import floor
from tkinter.colorchooser import *
import time
import traceback
import threading

root = Tk()

window_label = Label(root, text="Conway's Game of Life")
window_label.grid(row=0, columnspan=2)


class canvas_and_grid:

    def canvas_designer(self):
        print("line 1, canvas_designer")
        val = DoubleVar(0.0)
        self.x_start = cvs['xstart']  ##x starting point for creating window
        self.y_start = cvs['ystart']  ##same for y
        dimension = cvs['dimension']  ## pixel length of game window
        self.x_end = self.y_end = dimension  ## end of x y ranges in pixels
        side = cvs['side']  ## number of columns and rows on the grid (always a square)

        self.canvas_manager = Canvas(root, bg="gray", height=dimension, width=dimension)  ##main canvas for game play

        self.control_panel = Canvas(root, bg="light gray", height=dimension,
                                    width=450)  ## canvas to the right of the game field holds buttons n stuff
        self.monitor_port = Canvas(root, bg="black", height=250,
                                   width=450)  ## simulated screen that updates flash across TBD 1/31/19
        self.canvas_manager.grid(row=1, column=0, rowspan=200)
        self.control_panel.grid(row=1, column=1, rowspan=150, sticky=N)
        self.monitor_port.grid(row=1, column=1, rowspan=480, sticky=S)

        self.generate_optionmenu()  ## call listbox function used to choose how to play the game

        side = self.create_environment()  ## function to let the player determine how many columnns and rows they want on the field

        self.cell_size = int(round(dimension / side))  ## compute pixels in a single cell on the grid
        font_size = int(round(9 / side * 12))  ## proportion font to fit a smaller or larger cell

        for x in range(self.x_start, self.x_end,
                       self.cell_size):  ## x pixel values for the cells on the grid (actually, these are the y values....oops
            for y in range(self.y_start, self.y_end, self.cell_size):  ## y pixel values
                ## formulate the 'key' for the cell dict converting pixels to cell coordinate values
                self.cell_address = "(" + "{:.0f}".format((x + self.cell_size) / self.cell_size,
                                                          0) + "," + "{:.0f}".format(
                    (y + self.cell_size) / self.cell_size, 0) + ")"
                ## create the cell using pixel values and the inactive color
                self.grid_rectangle = self.canvas_manager.create_rectangle(x, y, x + self.cell_size, y + self.cell_size,
                                                                           fill=colors['inactive'][1], outline="white",
                                                                           width=1, tags=self.cell_address)
                self.canvas_manager.itemconfig(self.grid_rectangle)
                ## put text in the middle of the new cell using the address calculated above to populate the field
                self.canvas_text = self.canvas_manager.create_text(x + (self.cell_size / 2), y + (self.cell_size / 2),
                                                                   fill="white", text=self.cell_address,
                                                                   font=('helvetica', font_size, "bold"))
                self.canvas_manager.itemconfig(self.canvas_text)
                ## create the cells within the cell dict - key is cell address, tuple of values is name of color, #ff0... for official color value
                ## 0 or 1 for a flag for a function below to assign a course of action and then the x and y coordinate values for the cell
                cells[self.cell_address] = 'inactive', colors['inactive'][1], 0, int(
                    (x + self.cell_size) / self.cell_size), int((y + self.cell_size) / self.cell_size)
        self.canvas_manager.grid(row=1, column=0)

        ## button to pick the colors for each possible state: active, inactive...
        btnBck = Button(root, text="Select Color", command=lambda: [active_canvas.getColors()])
        btnBck.grid(row=3, column=1, sticky=W)

        ## slider to determine how fast the game processes through the cell life stages
        scale = Scale(root, orient=HORIZONTAL, to=100, sliderlength=25, length=200, variable=val,
                      command=active_canvas.setScaleVal)
        scale.grid(row=4, column=1, columnspan=4, sticky=W)
        scale.set(50)

        ## button to change the quantity of cells per column/row
        btnGrid = Button(root, text="Change grid",
                         command=lambda: [active_canvas.create_environment, active_canvas.canvas_designer()])
        btnGrid.grid(row=7, column=1, sticky=E)

        ## button to manually progress through the cell iterations
        b = Button(root, text="Next", width=20, command=self.setValueTrue)
        b.grid(row=9, column=1, sticky=W)
        ##        b.bind('<Button-1>',self.setValueTrue)
        dashboard_messages.append("creating canvas")

    def redraw_canvas(self, reason_code=False):
        ##        print("line 1, redraw_canvas")
        global cells
        status = True  ## not used

        self.x_end = cvs['xstart'] + cvs['dimension']  ## calculate the full width of the game canvas and the last x
        self.y_end = cvs['ystart'] + cvs['dimension']  ## same for y



        self.cell_size = int(
            round(cvs['dimension'] / cvs['side']))  ## figure out the cell size in px based on total dimension/side
        self.font_size = int(round(9 / cvs['side'] * 12))  ## pro rate the font size

        for x in range(cvs['xstart'], self.x_end, self.cell_size):  ## iterate through x values in pixels
            for y in range(cvs['ystart'], self.y_end, self.cell_size):  ## iterate through y values (pixels)
                if (x + self.cell_size) / self.cell_size + cvs['xbump'] > -0.25 and (
                        x + self.cell_size) / self.cell_size + cvs['xbump'] < 0:
                    a = 0  ## eliminate -0s for the x value
                else:
                    a = (x + self.cell_size) / self.cell_size + cvs[
                        'xbump']  ## otherwise x # of pixels & cellsize / cell size = x coordinate of cell
                if (y + self.cell_size) / self.cell_size + cvs['ybump'] > -0.25 and (
                        y + self.cell_size) / self.cell_size + cvs['ybump'] < 0:
                    b = 0  ## eliminate -0s for y value
                else:
                    b = (y + self.cell_size) / self.cell_size + cvs['ybump']  ## same for y coordinate of cell
                self.cell_address = "(" + "{:.0f}".format(a, 0) + "," + "{:.0f}".format(b,
                                                                                        0) + ")"  ## create cell address based on x and y above

                if self.cell_address not in cells:  ## if the new cell is not in the cell dict...
                    fill_color = colors['inactive'][
                        1]  ## its a new edge so it has to be inactive and set color accordingly
                    cells[self.cell_address] = 'inactive', colors['inactive'][1], 0, a, b  ## assign values to cell
                else:
                    fill_color = cells[self.cell_address][
                        1]  ## if the cell already exists though, just assign the color for the cell that exists
                ##                print("the redraw canvas cell being colored is ", self.cell_address)
                self.canvas_refresh(self.cell_address, x, y, self.cell_size, fill_color,
                                    self.font_size)  ##call the actual refresh

        cells_same = False  ## does not appear to be used
        return False
        dashboard_messages.append("redrawing the canvas and cell size is " + str(self.cell_size))

    def canvas_refresh(self, address_in, x_in, y_in, cell_size_in, fill_color_in, font_size_in):
        #        print("line 1, canvas_refresh")
        remove_rectangle = self.canvas_manager.find_withtag(address_in)
        self.canvas_manager.delete(remove_rectangle)
        self.grid_rectangle = self.canvas_manager.create_rectangle(x_in, y_in, x_in + cell_size_in, y_in + cell_size_in,
                                                                   fill=fill_color_in, outline="white", width=1,
                                                                   tags=self.cell_address)
        self.canvas_manager.itemconfig(self.grid_rectangle)
        self.canvas_text = self.canvas_manager.create_text(x_in + (cell_size_in / 2), y_in + (cell_size_in / 2),
                                                           fill="white", text=address_in,
                                                           font=('helvetica', font_size_in, "bold"))
        self.canvas_manager.itemconfig(self.canvas_text)
        self.canvas_manager.update()
        dashboard_messages.append("called canvas refresh")

    def color_cells(self, cells, repeater=False):
        ##        print("line 1, color_cells")
        global paused  ## not really used? declared in main and referenced here.
        global temp_cells  ## these are the values coming out of the id_changes process
        global cvs
        dashboard_messages.append("in color cells right before temp_cells test and temp_cells is " + str(
            temp_cells) + " and cvs[repeater] is " + str(cvs['repeater']))
        if temp_cells:  ## values in list?
            self.repeat_colors()  ## if yes, call repeat colors which will actually apply the color
            ##            if cvs['repeater'] and not paused: ## if there are still more changes needed,...
            if cvs['repeater']:  ## if there are still more changes needed,...
                dashboard_messages.append(
                    "calling id_changes from color_cells because there are more changes to review")
                self.id_changes(cells)  ## call id_changes to kickoff the assessment process

        else:
            ##
            if cvs['repeater']:  ## if repeater is true but not paused, closeout the game
                print("hit closeout game in color_cells")
                self.closeoutGame()
            else:
                for key in cells:  ## if repeater has not yet been set then just run the color updates from here - only at beginning of a round typically
                    color_rectangle = self.canvas_manager.find_withtag(key)
                    self.canvas_manager.itemconfigure(color_rectangle, fill=cells[key][1])
                    self.canvas_manager.update()
                    dashboard_messages.append("first pass through coloring the cells")

    ##                    self.id_changes(cells)

    def repeat_colors(self, counter=0):
        ##        print("line 1, repeat_colors")
        ##        global y
        global speed_constant  ## value for the slider to set how fast the square colors update
        global step_play  ## flag set when the scale is set to 0 indicating manual click of button to progress through color updates
        global next_step  ## ????

        ##        print("speed_constant at the start of repeat_colors is ", speed_constant)

        if not step_play:  ## if not manual processing by button click, proceed through temp_cells...
            temp_cells.sort()
            while temp_cells:  ## as long as temp_cells is not empty, keep processing...
                ##                print("inside repeat_colors and showing temp_cells ", temp_cells)
                repeat_color_rectangle = self.canvas_manager.find_withtag(temp_cells[counter][0])
                self.canvas_manager.itemconfigure(repeat_color_rectangle, fill=temp_cells[counter][1])
                self.canvas_manager.update()
                dashboard_messages.append(
                    "updating cell " + str(temp_cells[counter][0]) + " to color " + str(temp_cells[counter][1]))

                n, o = self.get_x_y(temp_cells[counter][0])  ## convert key to actual x and y coordinates

                if temp_cells[counter][1] == colors['emerging'][
                    1]:  ## if temp cells is emerging, change it to active for next round
                    cells[temp_cells[counter][0]] = 'active', colors['active'][
                        1], 0, n, o  ## change to active in cells dict and assign n and o from above
                    temp_cells[counter][1] = colors['active'][1]  ## add the new values to temp_cells
                ##                    counter = 0
                elif temp_cells[counter][1] == colors['dying'][1]:  ## if the cell is dying,...
                    cells[temp_cells[counter][0]] = 'inactive', colors['inactive'][
                        1], 0, n, o  ## update the value in cells to inactive...
                    temp_cells[counter][1] = colors['inactive'][1]  ## make it inactive for next round here
                ##                    counter = 0
                else:
                    ##                    print("removing the values from temp_cells and the value being removed is ", temp_cells[counter])
                    temp_cells.remove(temp_cells[counter])  ## if already inactive, remove the cell from the cells dict
                ##                counter = counter + 1
                ##                print("the value of y is ", y, " and the value of counter is ", counter)
                ##                print("inside repeat_colors the value of step_play is ", step_play, " and the value of next_step is ", next_step )
                ##            if not step_play:
                ####                print("speed constant is ", speed_constant)
                ##                print("temp cells from inside of repeat_colors is ", temp_cells)
                time.sleep(speed_constant)  ## slider speed dictates how long it takes between updates

        else:  ## manual process selected
            if temp_cells:  ## if values in temp_cells
                self.manual_color_move()  ## call manual color move
                ##                print("in then else part of the repeat colors logic")
                root.after(200, self.repeat_colors)  ## repeat after 200 ms
            ##                print("is this the last place it stops in repeat colors?")
            else:
                ##                print("or does it stop here in repeat colors")
                step_play = False  ## if no temp cell values left, set step play to false and head back to id changes
                ##                print("calling idchanges from the else in the else in repeat colors")
                self.id_changes(cells)

    ##    def basic_cell_update(self,tag,color):
    ##        print("basic_cell_update")

    def manual_color_move(self, manual_counter=0):
        ##        print("line 1, manual_color_move")
        global manual_move
        y = manual_counter
        ##        print("in manual color move temp cells is: ", temp_cells)
        x = len(temp_cells)
        ##        print("x the length of temp cells is ", x, " and manual_counter is ", manual_counter)
        ##        if manual_counter == 0:
        manual_temp_cells = iter(temp_cells)
        ##            print("manual temp cells is ", manual_temp_cells)
        var = IntVar()
        button = Button(root, text="Click Me", command=lambda: var.set(1))
        button.place(relx=.5, rely=.5, anchor="c")
        ##        if step_play:

        ##            while manual_temp_cells:
        ##        if temp_cells:
        ##        print("waiting...")
        button.wait_variable(var)
        ##                print("temp cells .next worked and manual_temp_cells is ", next(manual_temp_cells))
        man_temp_val = a, b = next(manual_temp_cells)
        ##        print("a and b are ",a," and ",b," respectively")
        repeat_color_rectangle = self.canvas_manager.find_withtag(a)
        self.canvas_manager.itemconfigure(repeat_color_rectangle, fill=b)
        self.canvas_manager.update()

        n, o = self.get_x_y(a)

        if temp_cells[temp_cells.index(man_temp_val)][1] == colors['emerging'][1]:
            ##            cells[temp_cells[manual_counter][0]] = 'active', colors['active'][1], 0, n, o
            cells[a] = 'active', colors['active'][1], 0, n, o
            temp_cells[temp_cells.index(man_temp_val)][1] = colors['active'][1]
        ##            temp_cells.append((a,colors['active'][1]))
        ##            temp_cells.remove(temp_cells.index(man_temp_val))
        elif temp_cells[temp_cells.index(man_temp_val)][1] == colors['dying'][1]:
            ##            cells[temp_cells[manual_counter][0]] = 'inactive', colors['inactive'][1], 0, n, o
            cells[a] = 'inactive', colors['inactive'][1], 0, n, o
            temp_cells[temp_cells.index(man_temp_val)][1] = colors['inactive'][1]
        ##            temp_cells.append((a,colors['inactive'][1]))
        ##            temp_cells.remove(temp_cells.index(man_temp_val))
        else:
            ##            print("temp cells index is ", temp_cells.index(man_temp_val))
            ##            print("temp cells is ", temp_cells)
            temp_cells.remove(man_temp_val)

    ##                print("manual temp cell 0 is ", manual_temp_cells[0], " and manual temp cell 1 is ", manual_temp_cells[1])
    ##                print("temp cells .next worked and manual_temp_cells is ", next(manual_temp_cells))
    ##                next(manual_temp_cells)
    ##        print("done waiting.")
    ##        y = y + 1
    ##        print("manual counter = ", y)
    ##            root.after(200, self.manual_color_move, y)

    def closeoutGame(self):
        ##        print("line 1, closeoutGame")
        global selection  ## variable for the entry value in the closeout game field
        global bob
        global cvs
        cvs['continue'] = False

        self.stop_top = Toplevel()  ## create a new top level window to hold the value of the closeout question
        self.stop_top.geometry("%dx%d%+d%+d" % (500, 300, 250, 200))  ## set dimensions

        self.stop_top.title("you have either reached nirvana or an infinite loop...")

        selection = StringVar()  ## default in the value for the entry input
        selection.set('x')  ## default to x which is meaningless
        answerQ = Label(self.stop_top, text='Infite loop: You good?:')
        answerQ.grid(row=1, column=0)

        answerA = Entry(self.stop_top, width=1, textvariable=selection)  ## create the entry space on the window
        answerA.grid(row=1, column=1)

        ##        print("right before the stop_top.grab_set in closeout game")
        self.stop_top.grab_set()  ## give the closeout window the focus until answered
        self.stop_top.lift()  ## it appear front and center
        ##        print("right after stop_top.grab_set and stop_stop.lift")
        ##        print("in closeout game and the value of cells is ", cells, " and the value of temps_cells is ", temp_cells)

        selection.trace_id = selection.trace('w',
                                             self.my_tracer)  ## put a trace_id on selection to monitor whatever gets typed

    ##        print("selection.trace_id = ", selection.trace_id)

    def my_tracer(self, a, b, c):  ## the a,b,c are default values specified by the trace
        ##        print("line 1, my_tracer")
        global selection  ## same selection variable as above
        global bob

        ##        print("in the trace a.get() = ", a, " b = ",b, " and c = ", c)

        aL = selection.get()  ## gathering the value from the closeout game function for the entry variable

        if len(aL) < 1:
            aL = 'x'  ## default the value to x always
        if aL[0] == 'y':  ## y causes the game to stop and restart a clean canvas and await a prompt from the user
            responseLabel = Label(self.stop_top, text='Ok, that will cause the program to start over')
            responseLabel.grid(row=2, column=0)
            cvs['side'] = 9  ## reset defaults
            ## button tells the app to close the window and to redo the whole canvas and make everything new and waiting
            buttonStart = Button(self.stop_top, text="Start Over",
                                 command=lambda: [self.stop_top.destroy(), self.canvas_designer()])
            buttonStart.grid(row=4, column=1)
        elif aL[0] == 'n':  ## just a garbage answer to handle a no
            responseLabel = Label(self.stop_top, text='No worries bruh, let''s keep rockin'' and rollin'' ')
            responseLabel.grid(row=2, column=0)
            ## closes the top window and restarts the closeout function
            buttonRepeat = Button(self.stop_top, text="Repeat",
                                  command=lambda: [self.stop_top.destroy(), self.closeoutGame()])
            buttonRepeat.grid(row=4, column=1)
        else:
            responseLabel = Label(self.stop_top,
                                  text='Du-huuude, you got to enter ''y'' or ''n''')  ## setup to handle a garbage answer
            responseLabel.grid(row=2, column=0)

    def get_x_y(self, cell_address):  ## function to convert cell address from a key as a string to actual numbers
        ##        print("line 1, get_x_y")
        j = (cell_address.find("(") + 1)  ## find open parantheses
        k = cell_address.find(",")  ## find comma
        l = k + 1  ## get the actual start for the slice
        m = cell_address.find(")")  ## find close paran
        x = int(cell_address[j:k])  ## convert x to an int
        y = int(cell_address[l:m])  ## convert y to an int
        dashboard_messages.append("getting the x and y coordinates for " + str(x) + " and " + str(y))
        return (x, y)  ## return the x and y values

    def reset_cell_color(self, cells):  ## called when game starts over and everything needs to be inactive again
        ##        print("line 1, reset_cell_color")
        dashboard_messages.append("running reset_cell_color to turn everything back to inactive")
        for key in cells:
            n, o = self.get_x_y(key)  ## go through all cells and convert to inactive
            cells[key] = 'inactive', colors['inactive'][1], 0, n, o
        self.color_cells(cells)  ## call colors to update

    def recolor_cells(self, cells,
                      color_state):  ## called from the color picker when inactive, active, emerging, dying changes
        ##        print("line 1, recolor_cells")
        what_happened.append("running recolor cells func color")
        for key in cells:
            n, o = self.get_x_y(key)
            if cells[key][
                0] == color_state:  ## if the cell is of the type that the color was just changed for, reset it to the passed in value
                cells[key] = color_state, colors[color_state][1], 0, n, o  ## reset
        self.color_cells(cells)  ## call color cells to actually change

    def print_to_dashboard(self,
                           counter=0):  ## function to have running commentary in the dashboard...not working as of 2/1/19
        ##        print("line 1, print_to_dashboard")
        self.monitor_port = Canvas(root, bg="black", height=250, width=450)
        self.monitor_port.grid(row=1, column=1, rowspan=480, sticky=S)

        ##        for i in dashboard_messages:

        ##            if dashboard_messages[i]["y"] >=15:
        ##                new_value = dashboard_messages[i]["y"] - 15
        ##                dashboard_messages[i]["y"] = new_value

        ##        d = len(dashboard_messages) + 1
        ##        dashboard_messages[d] = {}
        ##        dashboard_messages[d]["x"] = 5
        ##        dashboard_messages[d]["y"] = 545
        ##        new_message = text_message + other_data
        ##        dashboard_messages[d]["message"] = new_message

        ##        for i in dashboard_messages:
        print("inside print to dashboard ", dashboard_messages[counter])
        self.dashboard_text = self.monitor_port.create_text(100, 150, fill="white", width="185",
                                                            text=dashboard_messages[counter])
        self.monitor_port.itemconfig(self.dashboard_text, anchor=SW)
        self.monitor_port.update()
        counter = counter + 1
        if dashboard_messages:
            root.after(25, self.print_to_dashboard, counter)

    def change_canvas(self, x, y):
        ##        print("line 1, change_canvas")
        redraw = False  ## trigger flag as to whether the canvas needs to be redrawn
        redraw_status = True  ## flag to tell process_changes whether cells dict grew

        max_X = 0  ## this is the initial value to set to sort the max and min for active x and y values
        min_X = 0  ## same
        max_Y = 0  ## same
        min_Y = 0  ## same

        for key in cells:
            if cells[key][0] == 'active':  ## if in cells dict and active...
                if cells[key][3] > max_X:  ## if bigger than the previous max, set this as the max
                    max_X = cells[key][3]
                elif cells[key][3] < min_X:  ## if less than the minimum x, set this as min
                    min_X = cells[key][3]
                if cells[key][4] > max_Y:  ## if y max, set it here
                    max_Y = cells[key][4]
                elif cells[key][4] < min_Y:  ## if y min set it here
                    min_Y = cells[key][4]

        ##        print("max_X, min_X, max_Y, min_Y are ", max_X, min_X, max_Y, min_Y, " respectively")

        if ((min_X - 2) <= ((cvs['xstart'] / (cvs['dimension'] / cvs['side'])) + cvs['xbump']) and (max_X + 4) >= (
                cvs['side'] + cvs['xbump']) or (min_X - 4) <= (
                (cvs['xstart'] / (cvs['dimension'] / cvs['side'])) + cvs['xbump']) and (max_X + 2) >= (
                cvs['side'] + cvs['xbump'])):  ##1
            ## if the minimum value of x, less an additional 2, is less than the xstart value as converted from pixels to x cell values (adding in any "bump"
            ## factor, which is the value of the cumulative change to this point). If the max + 4 is greater than the cvs side and any bump factor, expand the whole
            ## canvas by 4 added cubes...or, if x-4 is less than the combined length and bump and x + 2 is greater than the length + bump, grow the canvas
            cvs['side'] = cvs['side'] + 4  ## add to the whole canvas, all sides because the cells are growing outward
            redraw = True  ## we need to restart the id_changes process because the canvas grew
            reason_code = "criteria1"  ## not really used?
        ##            print("reason code in change_canvas is ", reason_code)
        elif (min_X - 2) <= (cvs['xstart'] / (cvs['dimension'] / cvs['side']) + cvs[
            'xbump']):  ##2 if the cells are just growing to the left, add negative values
            reason_code = "criteria2"
            redraw = True  ## same
            cvs['xbump'] = cvs['xbump'] - 2  ## just move the visible fields to the left, not changing the whole canvas
        ##            print("reason code in change_canvas is ", reason_code)
        elif (max_X + 2) >= (cvs['side'] + cvs['xbump']):  ##3 if the cells are growing the right...
            reason_code = "criteria3"
            redraw = True  ## same
            cvs['xbump'] = cvs['xbump'] + 2  ## just add values to the right
        ##            print("reason code in change_canvas is ", reason_code)
        ##        if  ( (min_Y-2) <= (cvs['ystart']/(cvs['dimension']/cvs['side']) + cvs['ybump']) and (max_Y+4) >= (cvs['side'] + cvs['ybump']) or (min_Y-4) <= (cvs['ystart']/(cvs['dimension']/cvs['side']) + cvs['ybump']) and (max_Y+2) >= (cvs['side'] + cvs['ybump'])  ): ##4
        elif ((min_Y - 2) <= (cvs['ystart'] / (cvs['dimension'] / cvs['side']) + cvs['ybump']) and (max_Y + 4) >= (
                cvs['side'] + cvs['ybump']) or (min_Y - 4) <= (
                      cvs['ystart'] / (cvs['dimension'] / cvs['side']) + cvs['ybump']) and (max_Y + 2) >= (
                      cvs['side'] + cvs['ybump'])):  ##4
            ## same logic as above for the x values except that growing up and down instead of left and right
            cvs['side'] = cvs['side'] + 4  ## grow the whole canvas in this case
            reason_code = "criteria4"
            redraw = True  ## same logic as with the x
        ##            print("reason code in change_canvas is ", reason_code)
        elif (min_Y - 2) <= (cvs['ystart'] / (cvs['dimension'] / cvs['side']) + cvs[
            'ybump']):  ##5 if only growing from the top down, add rows to the top (negative values)
            reason_code = "criteria5"
            redraw = True  ## same
            cvs['ybump'] = cvs['ybump'] - 2  ## ditto to x logic
        ##            print("reason code in change_canvas is ", reason_code)
        elif (max_Y + 2) >= (cvs['side'] + cvs['ybump']):  ##6 only growing from the bottom up
            reason_code = "criteria6"
            redraw = True  ## same
            cvs['ybump'] = cvs['ybump'] + 2  ## ditto to y logic
        ##            print("reason code in change_canvas is ", reason_code)
        if redraw:
            redraw_status = self.redraw_canvas(
                reason_code)  ## set the redraw_status flag based on whether we redrew it or not
        ##            self.redraw_canvas(reason_code) ## redraw the canvas

        return redraw_status  ## pass this back to process_changes to see if the loop there needs to break because cells dict changed

    def id_changes(
            self,
            cells,
            status=True
    ):
        ##        print("line 1, id_changes")
        x = 0

        ##        speed_factor = .01
        ##        global speed_factor
        global cvs
        global cells_less_one, cells_less_two
        global temp_cells
        global logfile
        population = iter(cells.keys())
        if cvs['reboot']:
            counter = cvs['key_value']
        ##            print("counter based on cvs[keyvalue]= ", cvs['key_value'])
        ##        else:
        ##            counter = iter(cells.keys())

        ##        print("cells starting off ", cells.get()[1])
        ##        print("the value of cvs reboot is ", cvs['reboot'])
        ##        print("does it get to the point it is running before the if reboot statement?")
        if not cvs[
            'reboot']:  ## this flag tells us whether we grew the # of cells on the grid in the last round. if no, take the routine path...
            ##            print("first line inside the reboot if")
            while cells and cvs['continue']:
                ##                print("first line inside the while in idchanges")
                try:
                    counter = next(population)
                ##                    print("counter in the try is ", counter)
                except Exception:
                    error_message = traceback.format_exc()
                    print("the error message is ", error_message)
                    print("inside of the except in the while in id changes")
                    ##                    if not cvs['u_bool'] and not cvs['r_bool']:
                    ##                        self.closeoutGame()
                    ##                    print("cells is ", cells, " and cells less one is ", cells_less_one)
                    cellwrite1 = "cells are: " + str(cells)
                    logfile.write(cellwrite1)
                    cellwrite2 = "cells_less_one are: " + str(cells_less_one)
                    logfile.write(cellwrite2)
                    cellwrite3 = "cells_less_two are: " + str(cells_less_two)
                    logfile.write(cellwrite3)
                    if cells == cells_less_one:
                        print("cells = cells less one")
                    if cells == cells_less_two:
                        print("cells = cells_less_two")
                    if cells_less_one == cells_less_two:
                        print("cells_less_one = cells_less_two")
                    if (cells == cells_less_one or cells == cells_less_two):
                        cvs['continue'] = False
                        temp_cells = []
                        cvs['repeater'] = True
                        print("inside if cells == cells_less_one")
                        print("temp cells is ", temp_cells)
                    ##                    else:
                    ##                        cells_less_one = cells
                    cells_less_two.clear()
                    cells_less_two = {**cells_less_one}
                    cells_less_one.clear()
                    cells_less_one = {**cells}
                    print("ready to run color cells from insdie of the while loop")
                    self.color_cells(cells, cvs['repeater'])

                ##                    self.build_change_list()
                ##                    print("print statement right before the cvs[] in the while and value of rootbeer is ", rootbeer)
                ####                    break
                ####                    rootbeer = False
                ##                    print("print statement right after the rootbeer and value of rootbeer is ", rootbeer)

                ##                print("counter is ", counter)
                ##                print("cells[counter] is ", cells[counter])
                ##            for key in cells: ## go through every key in cells and...
                if cells[counter][0] == 'active':  ## if it is active...
                    n, o = self.get_x_y(counter)  ## determine the actual x and y integer values
                    cvs['p_original'] = cvs[
                        'p_start'] = n - 1  ## assign those out to P & Q for the loop ranges that follow in the process step
                    cvs['p_end'] = n + 2  ## same
                    cvs['q_original'] = cvs['q_start'] = o - 1  ## same
                    cvs['q_end'] = o + 2  ## same
                    cvs['r_value'] = 0  ## value that identifies whether a cell is dying
                    cvs['u_value'] = 0
                    cvs['key_value'] = counter  ## the key that is driving the review
                    ##                    self.process_changes() ## really should be called process review as this is where the "life and death" decisions are made
                    status_check = self.process_changes()  ## if process changes returns false from the last break review then we know the cells dict changed/grew
                    ##                    print("in id changes no reboot status check before the if statement is ", status_check)
                    if not status_check:  ## if the cells dict changed/grew
                        ##                        print("value of status check is ", status_check)
                        ##                        print("calling id changes from right inside of id changes at the bottom of the while")
                        self.id_changes(
                            cells)  ## start the whole thing over because otherwise we will get an error re: the fact cells dict changed quantity of key-value pairs
        ##                    if keep_rolling:
        ##                        print("we made it to the first keep_rolling in idchanges")
        ##                        self.gamecloseout()
        ##            self.build_change_list()
        ##            print("running in idchanges afteer build change list is called")
        ##            print("this is next after the break??")

        else:  ## start over where we left off after cells dict grew...
            ##            print("in id changes and running the reboot version (the else)")
            ##            self.process_changes() ## restart life/death review
            ##            print("inside the else in id changes is this next after the break???")
            status_check = self.process_changes()  ## if false that means the cells dict grew and need to start all the way over
            ##            print("in id changes with reboot status check before the if statement is ", status_check)
            if not status_check:  ## cells grew?
                ##                print("value of status check is ", status_check)
                ##                print("calling id changes from inside the else inside of id_changes")
                self.id_changes(cells)  ## if it grew, restart at the beginning

    ##            if keep_rolling:
    ##                print("we made it to the second keep_rolling in idchanges")
    ##                self.gamecloseout()
    ##        print("this is the next after the break break???")

    def canvas_id_changes(self, pstrt, qstrt, ustrt, rstrt, sstrt,
                          tstrt):  ## restate the core values for the life death process - simplifying that process because called from multiple places
        ##        print("line 1, canvas_id_changes")
        global cvs
        cvs['p_start'] = pstrt
        cvs['q_start'] = qstrt
        cvs['s_start'] = sstrt
        cvs['t_start'] = tstrt
        cvs['u_value'] = ustrt
        cvs['r_value'] = rstrt

    def process_changes(self):

        ##        print("line 1, process_changes")
        ##        print("in process changes")
        ##        print("value of cells is ", cells)
        call_it = False  ## game over, closeout
        break_it = True

        global cvs  ## declare global settings
        ##        cvs['continue'] = False
        ##        redraw = False ## value that tells us whether we changed the canvas to accomodate growth of active cells
        cvs[
            'repeater'] = repeater = True  ## this flag tells us that we set cells to emerging and dying in the current round, therefore, we know we need to keep going (repeating, etc.)
        change_status = True  ## flag that tells us whether cells caused the canvas to grow or move...True means the canvas did not change...False means break and restart
        r = cvs[
            'r_value']  ## we are restarting the r count everytime we come into this function - either starting over or, first path through on a new cell from dict
        if not cvs['reboot']:
            cvs['p_start'] = cvs['p_original']
        ##        for p in range(cvs['p_start'],cvs['p_end']): ## this is the x value for all cells starting top left corner and counting x# of cells (based on sides variable)
        while cvs['p_start'] < cvs['p_end']:
            p = cvs['p_start']
            ##            print("value of p is ", p)
            ##            for q in range(cvs['q_start'],cvs['q_end']): ## this is the y value for all cells (again based on sides variable)
            if not cvs['reboot']:
                cvs['q_start'] = cvs['q_original']
            while cvs['q_start'] < cvs['q_end']:
                q = cvs['q_start']
                ##                print("value of q is ", q)
                cvs[
                    'u_value'] = u = 0  ## we count u (emerging) every time because this is a count of inactive cells touching active cells
                selected_cell = "(" + str(p) + "," + str(
                    q) + ")"  ## build x and y coordinates into a valid cell for all the cells surrounding an active cell
                ##                print("selected cell is ", selected_cell)
                change_status = self.change_canvas(p, q)  ## did we change the canvas?
                ##                print("change status in q is ", change_status)
                ##                self.change_canvas(p,q) ## process the canvas changes
                if not change_status:  ## if change canvas returns false we know it changed which means cells dict grew which means we need to restart
                    s = cvs[
                        's_start']  ## we have not declared new s & t values yet so set them up before the canvas id changes
                    t = cvs['t_start']  ## same
                    cvs['reboot'] = True  ## its a reboot
                    self.canvas_id_changes(p, q, u, r, s,
                                           t)  ## reset the key values in cvs that define the start/end points for the canvas / cells dict
                    ##                    print("first break in q")
                    ##                    exit.set()
                    cvs['continue'] = True
                    break  ## break out of this loop
                if cells[selected_cell][0] == 'active' or cells[selected_cell][
                    0] == 'dying':  ## was it an active cell at any time in this round
                    cvs['r_value'] = r = cvs['r_value'] + 1  ## count if yes
                ##                    print("right after the r_value is hit because the cell was either active or dying and r is ", r)
                ##                            self.print_to_dashboard("selected cell is " + selected_cell + " and r = " + str(r), " ")
                else:  ## if not an active cell is it touched by 3 active cells and should it come back to life
                    ##                    s = cvs['s_start'] ## x values
                    ##                    print("the value of s from cvs s_start is ", cvs['s_start'])
                    for s in range((p - 1), (
                            p + 2)):  ## this is the x value for all the cells surrounding the cells surrounging the active cells starting top left corner and counting side # of cells
                        ##                        print("value of s is ",s)
                        ##                        t = cvs['t_start'] ## y values
                        for t in range((q - 1), (
                                q + 2)):  ## this is the y value for all cells (# as specified by sides variable)
                            ##                            print("value of t is ",t)
                            change_status = self.change_canvas(s, t)  ## change cells dict / canvas?
                            ##                            self.change_canvas(s,t) ## process changes
                            new_cell = "(" + str(s) + "," + str(t) + ")"  ## (x, y)
                            ##                            print("the value of new cell is ", new_cell, " and the value of cells[new_cell][0] is ", cells[new_cell][0])
                            if cells[new_cell][0] == 'active' or cells[new_cell][
                                0] == 'dying':  ## active anytime this round?
                                cvs['u_value'] = u = cvs[
                                                         'u_value'] + 1  ## count if yes - will tell us whether we should add the new cell as emerging
                            ##                                print("the value of u is ", u)
                            if not change_status:
                                cvs['reboot'] = True  ## cells dict changed
                                self.canvas_id_changes(p, q, u, r, s, t)  ## redeclare all core canvas values
                                ##                                print("second break inside t")
                                ##                                exit.set()
                                cvs['continue'] = True
                                break  ## break out of this loop (t)

                        if not change_status:
                            cvs['reboot'] = True  ## see above
                            self.canvas_id_changes(p, q, u, r, s, t)  ## see above
                            ##                            print("third break in s")
                            ##                            exit.set()
                            cvs['continue'] = True
                            break  ## leaving the s loop
                    if change_status:  ## decide whether there were 3 active cells touching the inactive cell and change value to emerging if yes
                        cvs['reboot'] = False
                        if u > 2 and u < 4 and cells[selected_cell][
                            0] == 'inactive':  ## for selected cell we have counted every cell around it - if it is inactive and touching 3 active cells...
                            ##                            print("made it past the u condition in process changes and u is ",u)
                            ##                            print("this is cvs in u ", cvs)
                            n, o = self.get_x_y(selected_cell)  ## getting actual x y coordinates from the key value
                            cells[selected_cell] = 'emerging', colors['emerging'][
                                1], 1, n, o  ## the selected cell needs to be emerging (1 value is a flag that it changed this round
                            cvs[
                                'repeater'] = repeater = True  ## because this changed we know we will need to run the color change more than once
                            cvs['u_value'] = u = 0
                            cvs['continue'] = True
                            cvs['u_bool'] = True
                    if not change_status:
                        cvs['reboot'] = True
                        self.canvas_id_changes(p, q, u, r, s, t)
                        ##                        print("fourth break in q")
                        ##                        exit.set()
                        cvs['continue'] = True
                        break  ## breaking out of the q loop
                cvs['q_start'] = cvs['q_start'] + 1
            if not change_status:
                cvs['reboot'] = True
                self.canvas_id_changes(p, q, u, r, s, t)
                ##                print("fifth break in p")
                ##                exit.set()
                break_it = False
                cvs['continue'] = True
                ##                return False ## tells calling functions (id_changes) that cells dict changed so that loop will need to break too
                break  ## breaking out of the p loop
            cvs['p_start'] = cvs['p_start'] + 1
        if change_status:

            if r < 3 or r > 4:  ##Less than 3 because process will always count itself + only 1 other cell = dying (likewise self + >3 = >4 = death)
                n, o = self.get_x_y(cvs['key_value'])  ## get actual x and y from key
                cells[cvs['key_value']] = 'dying', colors['dying'][
                    1], 1, n, o  ## 1 is a flag meaning it changed this round, else 0
                ##                print("ran the r condition and the value of r is ", r)
                ##                print("this is cvs in r ", cvs)
                cvs['r_value'] = r = 0  ## we did our r analysis so reset to 0 to start count over
                cvs['repeater'] = repeater = True  ## value changed so we will need to repeat the colors process
                cvs['reboot'] = False  ## we changed the value of a cell but not the size of cells dict
                ##                print("dying cell as set by r is cvs[key_value] of ", cvs['key_value'])
                cvs['r_value'] = r = 0
                cvs['continue'] = True
                cvs['r_bool'] = True
        ##        print("change_status at the bottom of process changes is ", change_status)
        ##        if not change_status:
        ##            cvs['repeater'] = repeater = True ## because cells dict changed...this would be true if any of the breaks were triggered
        ##            ## it would be disregarded if no breaks and normal processing occurred
        ##            print("if not change status...")
        ##            self.canvas_id_changes(p,q,u,r,s,t)
        ##            break

        if repeater and not change_status:  ## repeater will always be true...either break triggered it or the previous if did...any value to this?
            ## this is basically saying if the break was triggered (repeater true and change status false) then restart at id_changes...
            ##            print("if repeater and change status then call self id changes")
            ##            print("calling idchanges from inside of process changes")
            self.id_changes(cells)
        else:  ## no break occurred?
            ##            print()
            ##            print("right before the conversion of cells to temp_cells at the bottom of process changes")
            for key in cells:  ## go through all the cells dict
                if cells[key][2] == 1 and [key, cells[key][
                    1]] not in temp_cells:  ## if u or r counts triggered any emerging or dying cells (1 flag)...
                    temp = [key, cells[key][1]]  ## temp cells members just have the key value (x,y) and the color
                    temp_cells.append(temp)  ## add these to temp_cells
                    n, o = self.get_x_y(key)  ## get actual x,y
                    ##                    print("inside the create temp_cells loop")
                    cells[key] = cells[key][0], cells[key][
                        1], 0, n, o  ## rewrite to cells with a 0 value to replace the 1 flag
        ##        print("the values for p and q are ", p, " and ", q)
        ##        print("temp cells at the bottom of process changes is ", temp_cells)
        ##        print("the value of cvs-continue is ", cvs['continue'])
        ##        if not cvs['u_bool'] and not cvs['r_bool']:
        ##            self.closeoutGame()
        return break_it

    def build_change_list(self):
        global cvs
        ##        print("line 1, build_change_list")
        ##        print("temp cells in build change list is ", temp_cells)
        if temp_cells:  ## does temp cells contain any members?
            ##                print("in process_changes and just created temp_cells and now checking prior to calling color cells")
            ##                print("print temp_cells in process changes ", temp_cells)
            ##                print("inside of the temp_cells condition in build change list")
            self.color_cells(cells, cvs[
                'repeater'])  ## if yes process the new colors and repeater will tell you whether anything changed...still necessary?
        else:
            ##            cvs['continue']: ## otherwise if we have gone through all this and temp cells is empty we know there are no more changes, the game is over or in an infite loop
            ##                print("temp cells in the else in the temps cells clause at the bottom of process changes", temp_cells)
            ##                time.sleep(10)
            ##            print("hit closeout game in build change list")
            self.id_changes(cells)

    ##        else:
    ##            self.closeoutGame()
    ####                cvs['continue'] = False
    ##            print("returning to build change list else after running closeoutgame")
    ##        ##        call_it = True
    ##return break_it, call_it

    ##        print("it just keeps going after the closeout game is called")

    def select_random(
            self,
            cells
    ):
        ##            print("line 1, select_random")
        self.reset_cell_color(cells)  ## call reset to make sure screen starts with default 9 cells, etc.
        m = n = round(cvs['side'] / 2)  ## get an approximation of the cell at the center
        key = '(' + str(m) + ',' + str(n) + ')'  ## assign those values to the key
        cells[key] = 'active', colors['active'][1], 1, int(m), int(n)  ## assign active values to the key
        ##            print("first random cell is ", cells[key])
        i = 0
        j = 0
        k = 0
        l = 0

        i = randint(2, 3)  ## pick whether there will be 3 or 4 cells in total randomized
        while j < i:  ## iterate through the quantity of additional cells
            k = randint(-1, 1) + m  ## k = x values which is randomized based on the range of -1 to 1
            l = randint(-1, 1) + n  ## l = y values (same otherwise)
            random_range = "(" + str(k) + "," + str(l) + ")"  ## assign new values to cell
            if cells[random_range][0] is not 'active':  ## is the cell already active?
                cells[random_range] = 'active', colors['active'][1], 1, int(k), int(l)  ## if not active, activate
                j = j + 1  ## next cell
        ##                    print("random cell is ", cells[random_range])
        self.color_cells(cells, False)  ## color the new cells active
        ##            print("calling idchanges from select_random")
        self.print_to_dashboard()
        self.id_changes(cells)  ## proceed to id_changes

    def select_with_mouse(
            self,
            cells
    ):
        print("line 1, select_with_mouse")
        self.reset_cell_color(cells)  ## reset to start with a clean board

        cell_side = cvs['dimension'] / cvs['side']  ## figure the pixel width of a cell
        print("debug")
        dashboard_messages.append("inside select_with_mouse")
        thread1 = threading.Thread(target=self.print_to_dashboard)
        thread1.start()

        def callback(event):
            print("callback in select with mouse")
            ## event.x and event.y get the location on the canvas of the mouse and dividing it by the cell length gets the cell coordinates
            mouse_click = "(" + str(floor(event.x / cell_side) + 1) + "," + str(floor(event.y / cell_side) + 1) + ")"
            if cells[mouse_click][0] != 'active':  ## make sure the cell is not already active
                cells[mouse_click] = 'active', colors['active'][1], 0, int(floor(event.x / cell_side) + 1), int(
                    floor(event.y / cell_side) + 1)
                ## set it to active and change the value in the cells dict
                self.color_cells(cells, False)  # color it

        b = Button(root, text="Done",
                   command=lambda: [print("calling idchanges from select with mouse"), self.id_changes(cells),
                                    b.grid_forget(), self.canvas_manager.unbind("<Button-1>", button_ID)])
        ## color the new active cells
        b.grid(row=2, column=1, sticky=W)
        button_ID = self.canvas_manager.bind("<Button-1>", str)  ## binding the mouse click to button 1 on the mouse
        self.canvas_manager.bind("<Button-1>", callback)  ## goes back to looking for x y events

    def create_environment(self):
        ##        print("line 1, create_environment")
        no_of_cubes = StringVar()  ##variable to hold the # of cubes in the entry field
        no_of_cubes = '9'  ##string for the number of cubes per side
        side = 9  ##actual default numeric value for # of sides
        e = Entry(root,
                  textvariable=no_of_cubes)  ##setup up entry field with a default value of 9 so that it does not return null?
        e.grid(row=7, column=1)
        labelEntry = Label(root, text="How many cubes per side?")
        labelEntry.grid(row=7, column=1, sticky=W)
        if len(e.get()) > 0:  ##verify the entry contains a value
            cvs['side'] = int(e.get())  ## convert to int and save to cvs
        return cvs['side']

    def generate_optionmenu(self):
        ##        print("line 1, generate_optionmenu")
        global var
        var = StringVar(root)  ## tie options to the root??
        ## values to choose from
        list_values = ["Select an option to get started", "Randomly assign cells", "Pick 3-4 adjoining cells",
                       "Pick a pattern(future)"]
        ## default to the first value in the list
        var.set(list_values[0])
        ## option menu tying var to the list of values and calling option menu loop to activate
        optionmenu = OptionMenu(root, var, *list_values, command=self.optionmenu_loop)
        optionmenu.grid(row=1, column=1, rowspan=1, sticky=W)

    def optionmenu_loop(
            self,
            value
    ):
        ##        print("line 1, optionmenu_loop")
        cvs['side'] = 9  ## always a reset when a new choice is picked from the list of values

        if value == "Randomly assign cells":  ## assess value and pick accordingly
            self.generate_optionmenu()  ## rerun the option menu to default appropriately
            self.select_random(cells)

        if value == "Pick 3-4 adjoining cells":  ## same
            self.generate_optionmenu()  ## same
            self.select_with_mouse(cells)

    def getColors(
            self,
    ):
        ##        print("line 1, getColors")

        top = Toplevel(height=300,
                       width=300)  ## create a window to hold the color buttons for the various states of the buttons
        top.title("About this application...")

        msg = Message(top, text="heebie jeebies")
        msg.grid(row=0, column=0)

        boxWidth = Entry(top, text='70')  ## set size for box
        boxWidth.grid(row=2, column=1)

        top.grab_set()  ## lock the main screen until the top level window is dealt with

        ## buttons for inactive, active, developing and dismiss - these will all trigger color picker and set themselves with a new color
        btnInactive = Button(top, text="Inactive Cells", bg=colors['inactive'][1],
                             command=lambda: [self.colorPicker('inactive_color', btnInactive)])
        btnInactive.grid(row=0, column=0)

        btnActive = Button(top, text="Active Cells", bg=colors['active'][1],
                           command=lambda: [self.colorPicker('active_color', btnActive)])
        btnActive.grid(row=0, column=1)

        btnBorn = Button(top, text="Developing Cells", bg=colors['emerging'][1],
                         command=lambda: [self.colorPicker('emerging_color', btnBorn)])
        btnBorn.grid(row=1, column=0)

        btnDying = Button(top, text="Dying Cells", bg=colors['dying'][1],
                          command=lambda: [self.colorPicker('dying_color', btnDying)])
        btnDying.grid(row=1, column=1)

        button = Button(top, text="Dismiss", command=top.destroy)  ## closes out the window
        button.grid(row=2, columnspan=2)

    def colorPicker(self, value_name, button):
        ##        print("line 1, colorPicker")
        color = askcolor()  ## calls the askcolor widget to get a color picker
        if value_name == 'inactive_color':  ## value passed to color picker
            colors['inactive'] = color  ## sets the color for this value
            self.recolor_cells(cells, 'inactive')  ## calls recolor to change the colors in the canvas
            button.config(bg=colors['inactive'][1])  ## changes the color of the button itself

        if value_name == 'active_color':
            colors['active'] = color
            self.recolor_cells(cells, 'active')
            button.config(bg=colors['active'][1])

        if value_name == 'emerging_color':
            colors['emerging'] = color
            self.recolor_cells(cells, 'emerging')
            button.config(bg=colors['emerging'][1])

        if value_name == 'dying_color':
            colors['dying'] = color
            self.recolor_cells(cells, 'dying')
            button.config(bg=colors['dying'][1])

    ##        self.print_to_dashboard(("value of cells in color pickier is " + cells),"")

    def setValueTrue(self):
        ##        print("line 1, setValueTrue")
        global next_step  ## flag that tells the program to iterate through based on button click
        next_step = True  ## default is true

    ##        print ("next step is ", next_step)
    ##        return next_step

    def setScaleVal(self, val):
        ##        print("line 1, setScaleVal")
        global speed_constant  ## the speed factor
        global step_play
        global next_step
        step_play = False
        next_step = False
        ##        print("scale value is ", val, " and the float(val) is ", float(val))
        if float(val) > 0.0:  ## if the value from the slider is > 0...
            speed_constant = float(val) / 100.0  ## set the constant to a %
        else:
            speed_constant = float(0.0)  ## otherwise, it is zero
            step_play = True  ## step play will tell the program to proceed based on button clicks (manual)
        ##            def callback_step(event):
        ##            print("inside the callback in setScaleVal")

        ##        print("made it to the end of setScaleVal and next_step = ", next_step, " and step play ", step_play)
        return speed_constant  ## send the value of the speed constant back to the repeat_colors function


##        self.print_to_dashboard(("the speed constant is " + str(speed_constant)),"")

###################################################
############   MAIN PROGRAM STARTS HERE
###################################################
temp_cells = list()

active_canvas = canvas_and_grid()
dashboard_messages = list()
cells = dict()
cells_less_one = dict([('1', 'derp')])
cells_less_two = dict([('2', 'yeet')])
##print("cells less one is ",cells_less_one)

y = 0

what_happened = []

colors = dict([  ##repository for all the colors in the game
    ('active', ((255.99609375, 255.99609375, 0.0), '#ffff00')),
    ('inactive', ((255.99609375, 0.0, 128.5), '#ff0080')),
    ('emerging', ((255.99609375, 128.5, 0.0), '#ff8000')),
    ('dying', ((192.75, 192.75, 192.75), '#c0c0c0'))
])

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

logfile = open('logGOL4.txt', 'a')

speed_contant = DoubleVar(0.0)  ## value for the slider

paused = False

active_canvas.canvas_designer()  ##start the game by building the grid

what_happened.append("in mainloop")

root.mainloop()
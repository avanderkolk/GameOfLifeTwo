## This code uses labels as the grid in an attempt to speed up processing.
## Turned out labels were actually much slower.
## This was the second attempt at GOL.
## Lesson from this project was to revisit the original GOL solution and revise it

import time
import tkinter as tk
from collections import Counter
from math import ceil
from random import randint


class GUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Conway's Game of Life")
        self.canvas_manager = tk.Canvas(bg="gray")
        self.canvas_manager.grid()
        self.frame = tk.Frame(self.canvas_manager, bg="Light Blue", bd=5, relief=tk.RIDGE, height=300, width=400)
        self.frame.grid(column=1, row=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.grid_propagate(0)
        self.frame_admin = tk.Frame(self.canvas_manager, bg="Light Blue", bd=5, relief=tk.RIDGE, height=300, width=210)
        self.frame_admin.grid(column=2, row=1, )
        self.frame_admin.rowconfigure(0, weight=1)
        self.frame_admin.columnconfigure(0, weight=1)
        self.frame_admin.grid_propagate(0)
        self.speed_control = tk.Scale(self.frame_admin, from_=100, to=1, orient="horizontal", label="Speed/ms")
        self.speed_control.set(50)
        self.speed_control.grid(column=1, row=0, sticky='N')
        self.generate_optionmenu()
        self.draw_grid()

    def draw_grid(self, cl=0, rw=0):
        global frame_height
        global frame_width
        global sides
        sides = max(min_max['max_column'] - min_max['min_column'], min_max['max_row'] - min_max['min_row'])
        frame_height = sides * 7.1 * 5
        frame_width = sides * 7.1 * 7
        self.frame.config(height=frame_height, width=frame_width)
        self.frame_admin.config(height=frame_height)
        print('draw_grid')
        column = cl
        row = rw
        max_column = max(min_max['max_column'], sides)
        max_row = max(min_max['max_row'], sides)
        if column < max_column:
            column_gap = min_max['min_column']
            if row < max_row:
                row_gap = min_max['min_row']
                cell = '(' + str(column + column_gap) + ',' + str(row + row_gap) + ')'
                grid[cell] = {}
                grid[cell]['row'] = rw
                grid[cell]['column'] = cl
                cell_color = colors['inactive']['color']
                text_color = colors['inactive']['text']
                self.label = tk.Label(self.frame, text=cell, bg=cell_color, fg=text_color, borderwidth=2, relief="solid", height=label_height, width=label_width)
                self.label.grid(row=row, column=column)
                grid[cell]['object'] = self.label
                row += 1
                if row == sides:
                    column += 1
                    row = 0
                self.frame.after(ceil(self.speed_calc()/2), self.draw_grid, column, row)
        else:
            if cells:
                self.draw_changes()

    def speed_calc(self):
        return self.speed_control.get()

    def draw_changes(self, it_dict=None):
        print('draw_changes')
        if it_dict is None:
            it_dict = iter(cells.items())
        cell = next(it_dict, -1)
        if cell != -1:
            cell_color = colors[cell[1]['status']]['color']
            text_color = colors[cell[1]['status']]['text']
            target = grid[cell[0]]['object']
            target.configure(text=cell[0], bg=cell_color, fg=text_color)
            self.frame.after(self.speed_calc()*2, self.draw_changes, it_dict)
        else:
            remove_inactive()
            cell_neighbors()


    def update_status(self):
        print("update_status")
        for cell in cells:
            if cells[cell]['status'] == 'emerging':
                cells[cell]['status'] = 'active'
            if cells[cell]['status'] == 'inactive':
                inactive_delete[cell] = cell
            if cells[cell]['status'] == 'dying':
                if str(cell) == '(4,2)':
                    print("debug")
                cells[cell]['status'] = 'inactive'

    def update_one_cell(self, cell_to_update, status):
        cell_color = colors[cells[cell_to_update]['status']]['color']
        text_color = colors[cells[cell_to_update]['status']]['text']
        target = grid[cell_to_update]['object']
        target.configure(text=cell_to_update, bg=cell_color, fg=text_color)

    def generate_optionmenu(self):
        global var
        var = tk.StringVar(self.root)

        list_values = [
            'Select a way to get started',
            'Pick 3-4 adjoining cells',
            'Randomly assign cells',
            'Pre-Programmed: Cross'
        ]
        ## default to the first value in the list
        var.set(list_values[0])
        ## option menu tying var to the list of values and calling option menu loop to activate
        optionmenu = tk.OptionMenu(self.frame_admin, var, *list_values, command=self.optionmenu_loop)
        optionmenu.grid(column=1, row=0, sticky='N')

    def optionmenu_loop(self, value):
        global sides, cells
        sides = 9  ## always a reset when a new choice is picked from the list of values

        if value == "Randomly assign cells":  ## assess value and pick accordingly
            self.generate_optionmenu()  ## rerun the option menu to default appropriately
            self.select_random()

        if value == "Pick 3-4 adjoining cells":  ## same
            self.generate_optionmenu()  ## same
            self.select_with_mouse()

        if value == "Pre-Programmed: Cross":  ## same
            self.generate_optionmenu()  ## same
            cells = cross
            self.draw_changes()

    def select_random(self):
        global sides
        global cells
        # self.reset_cell_color(cells)  ## call reset to make sure screen starts with default 9 cells, etc.
        m = n = round(sides / 2)  ## get an approximation of the cell at the center
        key = '(' + str(m) + ',' + str(n) + ')'  ## assign those values to the key
        active_cells[key] = {}
        active_cells[key]['status'] = 'active'
        i = 0
        j = 0
        k = 0
        l = 0

        i = randint(2, 3)  ## pick whether there will be 3 or 4 cells in total randomized
        while j < i:  ## iterate through the quantity of additional cells
            k = randint(-1, 1) + m  ## k = x values which is randomized based on the range of -1 to 1
            l = randint(-1, 1) + n  ## l = y values (same otherwise)
            random_range = "(" + str(k) + "," + str(l) + ")"  ## assign new values to cell
            active_cells[random_range] = {}
            if random_range in cells and cells[random_range] != 'active':  ## is the cell already active?
                active_cells[random_range]['status'] = 'active'  ## if not active, activate
                j = j + 1
            else:
                active_cells[random_range]['status'] = 'active'
                j = j + 1  ## next cell
        cells = active_cells
        self.draw_changes()

    def select_with_mouse(self):
        print("select with mouse")
        global button_ID

        def callback(event):
            print("in callback")
            for key, value in grid.items():
                if value['object'] == event.widget:
                    if key in cells and cells[key]['status'] != 'active':  ## make sure the cell is not already active
                        cells[key]['status'] = 'active'
                        break
                    else:
                        cells[key] = {}
                        cells[key]['status'] = 'active'
                        break
                ## set it to active and change the value in the cells dict
            self.update_one_cell(key, 'active')

        b = tk.Button(self.frame_admin, text="Done", command=lambda: [cell_neighbors(), self.canvas_manager.unbind("<Button-1>", button_ID)])
        b.grid(column=1, row=3, sticky='N')
        button_ID = self.root.bind("<Button-1>", str)  ## binding the mouse click to button 1 on the mouse
        self.root.bind("<Button-1>", callback)  ## goes back to looking for x y events


def remove_inactive():
    for k in inactive_delete.items():
        if k[0] in cells:
            cells.pop(k[0])
    inactive_delete.clear()

def cell_neighbors():
        print('cell_neighbors')
        neighbors = {}
        census = []
        for cell in cells:
            if cells[cell]['status'] == 'active':
                neighbors[cell] = {}
                neighbors[cell]['density'] = {}
                column, row = calc_row_column(cell)
                col_top_left = column - 1
                row_top_left = row - 1
                col_bottom_right = column + 1
                row_bottom_right = row + 1
                density = 0
                for c in range(col_top_left, col_bottom_right + 1):
                    for r in range(row_top_left, row_bottom_right + 1):
                        key = '(' + str(c) + ',' + str(r) + ')'
                        if key != cell:
                            census.append(key)
        born_dying(census)


def calc_row_column(cell_location):
    start = cell_location.find('(') + 1
    finish = cell_location.find(')')
    middle = cell_location.find(',')
    column = int(cell_location[start:middle])
    row = int(cell_location[(middle + 1):finish])
    return column, row


def born_dying(census_dict):
    print('born_dying')
    coming_and_going = dict(Counter(census_dict))
    for cell in coming_and_going:
        if cell in cells:
            cell_status = cells[cell]['status']
            if cell_status == 'inactive':
                if coming_and_going[cell] != 3:
                    inactive_delete[cell] = cell
                else:
                    cells[cell]['status'] = 'emerging'
            elif cell_status == 'dying':
                if coming_and_going[cell] != 3:
                    cells[cell]['status'] = 'inactive'
                else:
                    cells[cell]['status'] = 'emerging'
            elif cell_status == 'emerging':
                cells[cell]['status'] = 'active'
            elif cells[cell]['status'] == 'active':
                if coming_and_going[cell] < 2 or coming_and_going[cell] > 3:
                    cells[cell]['status'] = 'dying'
        else:
            if coming_and_going[cell] == 3:
                cells[cell] = {'status': 'emerging'}
    max_min()


def max_min():
    global sides
    print('max_min')
    max_column = min_max['max_column']
    max_row = min_max['max_row']
    min_column = min_max['min_column']
    min_row = min_max['min_row']
    max_min_flag = False
    for cell in cells:
        if cell in grid:
            if (cells[cell]['status'] == 'active' or cells[cell]['status'] == 'emerging') and grid[cell]['column'] + 2 > max(max_column, sides):
                min_max['max_column'] += 2
                max_column = min_max['max_column']
                if max_column > sides:
                    sides += 2
                max_min_flag = True
            if (cells[cell]['status'] == 'active' or cells[cell]['status'] == 'emerging') and grid[cell]['column'] - 2 < min(min_column, 0):
                min_max['min_column'] -= 2
                min_column = min_max['min_column']
                max_min_flag = True
            if (cells[cell]['status'] == 'active' or cells[cell]['status'] == 'emerging') and grid[cell]['row'] + 2 > max(max_row, sides):
                min_max['max_row'] += 2
                max_row = min_max['max_row']
                if max_row > sides:
                    sides += 2
                max_min_flag = True
            if (cells[cell]['status'] == 'active' or cells[cell]['status'] == 'emerging') and grid[cell]['row'] - 2 < min(min_row, 0):
                min_max['min_row'] -= 2
                min_row = min_max['min_row']
                max_min_flag = True
        else:
            cell_column, cell_row = calc_row_column(cell)
            if cell_column + 2 > max_column:
                min_max['max_column'] += 2
                max_column = min_max['max_column']
                max_min_flag = True
            if cell_column - 2 < min_column:
                min_max['min_column'] -= 2
                min_column = min_max['min_column']
                max_min_flag = True
            if cell_row + 2 > max_row:
                min_max['max_row'] += 2
                max_row = min_max['max_row']
                max_min_flag = True
            if cell_row - 2 < min_row:
                min_max['min_row'] -= 2
                min_row = min_max['min_row']
                max_min_flag = True
    if max_min_flag:
        grid.clear()
        app.draw_grid()
    else:
        print("grid dictionary is " + str(grid))
        app.draw_changes()


cells = {}

cross = {
    '(1,0)': {'status': 'active'},
    '(0,1)': {'status': 'active'},
    '(1,1)': {'status': 'active'},
    '(2,1)': {'status': 'active'},
    '(1,2)': {'status': 'active'},
    }

sides = 9
grid = {}
temp_dict = {}

label_height = 2
label_width = 5
frame_height = 300
frame_width = 300

min_max = {
    'min_column': 0,
    'min_row': 0,
    'max_column': sides,
    'max_row': sides
    }

colors = {
    'active': {'color': '#ffff00', 'text': '#000000'}, # yellow body with black text
    'inactive': {'color': '#ff0080', 'text': '#ffffff'}, # hot pink body with white text
    'emerging': {'color': '#ff8000', 'text': '#000000'}, # orange body with black text
    'dying': {'color': '#c0c0c0', 'text': '#000000'} # gray body with white text
}

inactive_delete = {}
active_cells = {}
census = []
speed = 20
speed_plus = 100

root = tk.Tk()
app = GUI(root)
root.mainloop()




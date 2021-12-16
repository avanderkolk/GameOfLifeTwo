import time
import tkinter as tk
from collections import Counter
from math import ceil, floor
from random import randint


class GUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Conway's Game of Life")
        self.canvas_manager = tk.Canvas(bg="gray", height=600, width=600)
        self.canvas_manager.grid()
        self.frame = tk.Frame(self.canvas_manager, bg="Light Blue", bd=5, relief=tk.RIDGE)
        self.frame.grid(column=1, row=1)
        self.frame_admin = tk.Frame(self.canvas_manager, bg="Light Blue", bd=5, relief=tk.RIDGE)
        self.frame_admin.grid(column=2, row=1)
        self.speed_control = tk.Scale(self.frame_admin, from_=100, to=1, orient="horizontal", label="Speed/ms")
        self.speed_control.set(50)
        self.speed_control.grid(column=1, row=1, sticky="N")
        self.generate_optionmenu()
        self.draw_grid()

    def draw_grid(self, cl=0, rw=0):
        global sides
        sides = max(min_max['max_column'] - min_max['min_column'], min_max['max_row'] - min_max['min_row'])
        print('draw_grid')
        column = cl
        row = rw
        max_column = max(min_max['max_column'], sides)
        max_row = max(min_max['max_row'], sides)
        # inactive_delete.clear()
        if column < max_column:
            column_gap = min_max['min_column']
            # print("debug")
            if row < max_row:
                row_gap = min_max['min_row']
                cell = '(' + str(column + column_gap) + ',' + str(row + row_gap) + ')'
                grid[cell] = {}
                grid[cell]['row'] = rw
                grid[cell]['column'] = cl
                # if cell in cells:
                #     cell_color = colors[cells[cell]['status']]['color']
                #     text_color = colors[cells[cell]['status']]['text']
                #     print(cells[cell])
                #     print("debug")
                #
                # else:
                cell_color = colors['inactive']['color']
                text_color = colors['inactive']['text']
                self.label = tk.Label(self.frame, text=cell, bg=cell_color, fg=text_color, borderwidth=2, relief="solid")
                self.label.grid(row=row, column=column)
                # update_status(cell)
                grid[cell]['object'] = self.label
                row += 1
                if row == sides:
                    column += 1
                    row = 0
                self.frame.after(ceil(self.speed_calc()/2), self.draw_grid, column, row)
        else:
            if cells:
                # remove_inactive()
                # cell_neighbors()
                self.draw_changes()

    def speed_calc(self):
        return self.speed_control.get()

    def draw_changes(self, it_dict=None):
        print('draw_changes')
        if it_dict is None:
            print("it_dict set by cells_items() function")
            it_dict = iter(cells.items())
        cell = next(it_dict, -1)
        print("debug")
        if cell != -1:
            print("cell is " + str(cell))
            cell_color = colors[cell[1]['status']]['color']
            text_color = colors[cell[1]['status']]['text']
            target = grid[cell[0]]['object']
            target.configure(text=cell[0], bg=cell_color, fg=text_color)
            # update_status(cell[0])
            self.frame.after(self.speed_calc()*2, self.draw_changes, it_dict)
        # if cell == -1:
        else:
            # self.update_status()
            remove_inactive()
            cell_neighbors()


    def update_status(self):
        print("update_status")
    # def update_status(self, it_dict=None):
    #     if it_dict is None:
    #         print("it_dict set by cells_items() function")
    #         it_dict = iter(cells.items())
    #     cell = next(it_dict, -1)
    #     print("cell[0] is " + str(cell[0]))
    #     print("debug")
    #     if cell != -1:
        for cell in cells:
            print("debug")
            # if str(cell) == '(1,-1)' or str(cell) == '(-1,1)' or str(cell) == '(3,1)' or str(cell) == '(1,3)':
            #     print("debug")
            # if cell[1]['status'] == 'emerging':
            #     cell[1]['status'] = 'active'
            #     app.update_one_cell(cell[0])
            # if cell[1]['status'] == 'inactive':
            #     inactive_delete[cell[0]] = cell
            # if cell[1]['status'] == 'dying':
            #     cell[1]['status'] = 'inactive'
            #     app.update_one_cell(cell[0])
            if cells[cell]['status'] == 'emerging':
                cells[cell]['status'] = 'active'
                # time.sleep(.5)
                # app.update_one_cell(cell, 'active')
                # time.sleep(.5)
            # if cells[cell]['status'] == 'emerging-test':
            #     cells[cell]['status'] = 'active'
            #     app.update_one_cell(cell, 'active')
            if cells[cell]['status'] == 'inactive':
                inactive_delete[cell] = cell
            if cells[cell]['status'] == 'dying':
                if str(cell) == '(4,2)':
                    print("debug")
                cells[cell]['status'] = 'inactive'
                # time.sleep(.5)
                # app.update_one_cell(cell, 'inactive')

            # if cells[cell]['status'] == 'dying-test':
            #     if str(cell) == '(4,2)':
            #         print("debug")
            #     cells[cell]['status'] = 'inactive'
            #     app.update_one_cell(cell, 'inactive')
            # self.frame.after(self.speed_calc() * 2, self.update_status, it_dict)
        print("done with update status")


    # def update_status(cell):
    #     if cell in cells:
    #         if cells[cell]['status'] == 'emerging':
    #             cells[cell]['status'] = 'active'
    #         if cells[cell]['status'] == 'inactive':
    #             inactive_delete[cell] = cell
    #         if cells[cell]['status'] == 'dying':
    #             cells[cell]['status'] = 'inactive'



    def update_one_cell(self, cell_to_update, status):
        print("debug")
        # cell_color = colors[cell_to_update[1]['status']]['color']
        cell_color = colors[cells[cell_to_update]['status']]['color']
        # cell_color = colors[status]['color']
        # text_color = colors[cell_to_update[1]['status']]['text']
        text_color = colors[cells[cell_to_update]['status']]['text']
        # text_color = colors[status]['text']
        target = grid[cell_to_update]['object']
        target.configure(text=cell_to_update, bg=cell_color, fg=text_color)

    def generate_optionmenu(self):
        ##        print("line 1, generate_optionmenu")
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
        optionmenu.grid(column=1, row=2, sticky='N')

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
        ##            print("line 1, select_random")
        # self.reset_cell_color(cells)  ## call reset to make sure screen starts with default 9 cells, etc.
        m = n = round(sides / 2)  ## get an approximation of the cell at the center
        key = '(' + str(m) + ',' + str(n) + ')'  ## assign those values to the key
        active_cells[key] = {}
        active_cells[key]['status'] = 'active'
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
            active_cells[random_range] = {}
            if random_range in cells and cells[random_range] != 'active':  ## is the cell already active?
                active_cells[random_range]['status'] = 'active'  ## if not active, activate
                j = j + 1
            else:
                active_cells[random_range]['status'] = 'active'
                j = j + 1  ## next cell
        ##                    print("random cell is ", cells[random_range])
        # self.color_cells(cells, False)  ## color the new cells active
        ##            print("calling idchanges from select_random")
        # self.id_changes(cells)  ## proceed to id_changes
        print("debug")
        cells = active_cells
        self.draw_changes()

    def select_with_mouse(self):
        print("select with mouse")
        global button_ID
        ##        print("line 1, select_with_mouse")
        # self.reset_cell_color(cells)  ## reset to start with a clean board

        # cell_side = ceil(600 / sides)  ## figure the pixel width of a cell
        print("debug")

        def callback(event):
            print("in callback")
            # x_value = event.x
            # y_value = event.y
            # ## event.x and event.y get the location on the canvas of the mouse and dividing it by the cell length gets the cell coordinates
            # mouse_click = "(" + str(floor(x_value / cell_side) + 1) + "," + str(floor(y_value / cell_side) + 1) + ")"
            print("trying to get widgets prionted " + "<tkinter.Label object " + str(event.widget) + ">")
            for key, value in grid.items():
                print("value object is " + str(value['object']))
                print("value event widget is " + str(event.widget))
                if value['object'] == event.widget:
                    if key in cells and cells[key]['status'] != 'active':  ## make sure the cell is not already active
                        # cells[mouse_click] = {}
                        cells[key]['status'] = 'active'
                        print("debug")
                        break
                    else:
                        cells[key] = {}
                        cells[key]['status'] = 'active'
                        print("debug")
                        break
                ## set it to active and change the value in the cells dict
                # self.color_cells(cells, False)  # color it
                # self.draw_changes()
                print("debug")
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

#
# def check_neighbors(cell):
#     column, row = calc_row_column(cell[0])
#     col_top_left = column - 1
#     row_top_left = row - 1
#     col_bottom_right = column + 1
#     row_bottom_right = row + 1
#     for c in range(col_top_left, col_bottom_right + 1):
#         for r in range(row_top_left, row_bottom_right + 1):
#             key = '(' + str(c) + ',' + str(r) + ')'
#             if key != cell[0]:
#                 census.append(key)
#             r += 1
#             if r == row_bottom_right + 1:
#                 c += 1
#                 r = row_top_left


def cell_neighbors():
        print('cell_neighbors')
        neighbors = {}
        census = []
        for cell in cells:
            # if cells[cell]['status'] == 'active' or cells[cell]['status'] == 'emerging':
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
                            if key in cells:
                                if cells[cell]['status'] == 'active' or cells[cell]['status'] == 'emerging':
                                    # neighbors[cell][key] = 'active'
                                    density += 1
                        #     else:
                        #         neighbors[cell][key] = 'dying'
                        # neighbors[cell]['density'] = density
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
    # app.update_status()
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
                    # cells[cell]['status'] = 'dying-test'
                    # app.update_one_cell(cell)
            # elif cells[cell]['status'] == 'inactive' and coming_and_going[cell] == 3:
            #     cells[cell] = {'status': 'emerging'}
                # cells[cell] = {'status': 'emerging-test'}
                # app.update_one_cell(cell)
            # if cells[cell]['status'] == 'emerging':
            #     cells[cell] = {'status': 'active'}
            # if cells[cell]['status'] == 'dying':
            #     cells[cell] = {'status': 'inactive'}
        else:
            if coming_and_going[cell] == 3:
                cells[cell] = {'status': 'emerging'}
                # app.update_one_cell(cell)
    max_min()


def max_min():
    global sides
    print('max_min')
    max_column = min_max['max_column']
    max_row = min_max['max_row']
    min_column = min_max['min_column']
    min_row = min_max['min_row']
    max_min_flag = False
    print("debug")
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
        # app.update_status()
        # remove_inactive()
        # cell_neighbors()
    else:
        print("grid dictionary is " + str(grid))
        app.draw_changes()
        # app.update_status()
        # remove_inactive()
        # cell_neighbors()

cells = {

    }

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
    'emerging-test': {'color': '#2ef429', 'text': '#000000'}, # lime green body with black text
    'dying': {'color': '#c0c0c0', 'text': '#000000'}, # gray body with white text
    'dying-test': {'color': '#cc8899', 'text': '#000000'} # purple body with white text
}

inactive_delete = {}
active_cells = {}
census = []
speed = 20
speed_plus = 100

root = tk.Tk()
app = GUI(root)
# root.geometry('800x600')
root.mainloop()




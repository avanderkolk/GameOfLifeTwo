import time
import tkinter as tk
from collections import Counter
from math import ceil


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
        self.speed_control = tk.Scale(self.canvas_manager, from_=100, to=1, orient="horizontal", label="Speed/ms")
        self.speed_control.set(100)
        self.speed_control.grid(column=2, row="1", sticky="N")
        self.draw_grid()

    def draw_grid(self, cl=0, rw=0):
        global sides
        sides = max(min_max['max_column'] - min_max['min_column'], min_max['max_row'] - min_max['min_row'])
        print('draw_grid')
        column = cl
        row = rw
        max_column = max(min_max['max_column'], sides)
        max_row = max(min_max['max_row'], sides)
        inactive_delete.clear()
        if column < max_column:
            column_gap = min_max['min_column']
            if row < max_row:
                row_gap = min_max['min_row']
                cell = '(' + str(column + column_gap) + ',' + str(row + row_gap) + ')'
                grid[cell] = {}
                grid[cell]['row'] = rw
                grid[cell]['column'] = cl
                if cell in cells:
                    cell_color = colors[cells[cell]['status']]['color']
                    text_color = colors[cells[cell]['status']]['text']
                    print(cells[cell])
                    print("debug")

                else:
                    cell_color = colors['inactive']['color']
                    text_color = colors['inactive']['text']

                self.label = tk.Label(self.frame, text=cell, bg=cell_color, fg=text_color, borderwidth=2, relief="solid")
                self.label.grid(row=row, column=column)
                update_status(cell)
                grid[cell]['object'] = self.label
                row += 1
                if row == sides:
                    column += 1
                    row = 0
                self.frame.after(ceil(self.speed_calc()/2), self.draw_grid, column, row)
        else:
            remove_inactive()
            cell_neighbors()

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
            update_status(cell[0])
            self.frame.after(self.speed_calc()*2, self.draw_changes, it_dict)
        if cell == -1:
            remove_inactive()
            cell_neighbors()


def update_status(cell):
    if cell in cells:
        if cells[cell]['status'] == 'emerging':
            cells[cell]['status'] = 'active'
        if cells[cell]['status'] == 'inactive':
            inactive_delete[cell] = cell
        if cells[cell]['status'] == 'dying':
            cells[cell]['status'] = 'inactive'


def remove_inactive():
    for k in inactive_delete.items():
        if k[0] in cells:
            cells.pop(k[0])
    inactive_delete.clear()


def check_neighbors(cell):
    column, row = calc_row_column(cell[0])
    col_top_left = column - 1
    row_top_left = row - 1
    col_bottom_right = column + 1
    row_bottom_right = row + 1
    for c in range(col_top_left, col_bottom_right + 1):
        for r in range(row_top_left, row_bottom_right + 1):
            key = '(' + str(c) + ',' + str(r) + ')'
            if key != cell[0]:
                census.append(key)
            r += 1
            if r == row_bottom_right + 1:
                c += 1
                r = row_top_left


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
                            if key in cells:
                                if cells[cell]['status'] == 'active':
                                    neighbors[cell][key] = 'active'
                                    density += 1
                            else:
                                neighbors[cell][key] = 'dying'
                        neighbors[cell]['density'] = density
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
            if cells[cell]['status'] == 'active':
                if coming_and_going[cell] < 2 or coming_and_going[cell] > 3:
                    cells[cell]['status'] = 'dying'
                if cells[cell]['status'] == 'inactive' and coming_and_going[cell] == 3:
                    cells[cell] = {'status': 'emerging'}
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
    else:
        print("grid dictionary is " + str(grid))
        app.draw_changes()

cells = {
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
    'active': {'color': '#ffff00', 'text': '#000000'},
    'inactive': {'color': '#ff0080', 'text': '#ffffff'},
    'emerging': {'color': '#ff8000', 'text': '#000000'},
    'dying': {'color': '#c0c0c0', 'text': '#000000'}
}

inactive_delete = {}
census = []
speed = 20
speed_plus = 100

root = tk.Tk()
app = GUI(root)

root.mainloop()




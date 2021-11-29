import tkinter as tk
COL_ORS = [
'IndianRed1','firebrick1', 'coral1', 'HotPink2', 'brown1',
'red2', 'gray1', 'VioletRed1', 'purple2', 'goldenrod1', 'SeaGreen1' , 'OliveDrab2', 'DarkGoldenrod1', 'DarkOrchid3',
'floral white', 'magenta4', 'pink4', 'LightYellow3', 'LightCyan3', 'turquoise2', 'OliveDrab4', 'thistle4'
]
class Color_Chart(tk.Frame):
    Mx_Rw = 32
    Fnt_Sz = 12

    print("running gridpractice2.com")

    def __init__(slf, r_t):
        tk.Frame.__init__(slf, r_t)

        rw = 0
        cl = 0

        slf.canvas_manager = tk.Canvas(r_t, bg="gray", height=600, width=600)
        # slf.canvas_manager = tk.Canvas(r_t, bg="gray")
        # slf.canvas_manager.grid(row=1, column=0, rowspan=600, columnspan=600)
        slf.canvas_manager.grid()

        # frame1 = tk.Frame(slf.canvas_manager, bg="Light Blue", bd=5, relief=tk.RIDGE, width=300)
        frame1 = tk.Frame(slf.canvas_manager, bg="Light Blue", bd=5, relief=tk.RIDGE)
        frame1.grid()
        while cl < 10:
            rw = 0
            for color in COL_ORS:
                label = tk.Label(frame1, text=color, bg=color, fg='white', font=("Times", slf.Fnt_Sz, "bold"), width=15)

                label.grid(row=rw, column=cl, sticky="ew")
                # label.grid()
                # slf.canvas_manager.create_text(text=color)
                rw += 1



                # if rw > slf.Mx_Rw:
                # if rw == len(COL_ORS) - 1:
                #     rw = 0
                #     cl += 1

            rw = 0
            cl += 1

                # slf.pack(expand=1, fill="both")

        # slf.canvas_manager.create_window(window=label)


        # if __name__ == '__main__':
r_t = tk.Tk()
r_t.title("Tkinter_Color_Chart")
app = Color_Chart(r_t)
r_t.mainloop()
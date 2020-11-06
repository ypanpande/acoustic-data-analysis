
import tkinter as tk
from tkinter import ttk, messagebox
#from Calender import Calendar
import tables as tb
#import datetime 
#import pytable_form as ptf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from test_class_plot2 import ScatterPlot

class LocAll:
    def __init__(self, root, h5path, filetime):
        self.root = root
        self.path = h5path
        self.filetime = filetime
        self.root.geometry('1550x1000+30+30')
        self.set_root_title()
        self.init_para()
        self.init_gui()
        self.show_figures()
    def set_root_title(self):
        self.root.title('Location with all methods')
    def init_para(self):
        self.methods = ['loc_seq6s','loc_geiger6s','loc_seq4s','loc_geiger4s']
    def init_gui(self):
        self.bar2 = ttk.LabelFrame(self.root, text = 'Figures Panel', width = 1540, height = 990, relief = 'sunken', borderwidth = 1)
        self.bar2.place(x = 5, y = 5, width = 1540, height = 990)

    def show_figures(self):
        self.create_figures()
        self.embed_figures()
    def create_figures(self):
        chose_data = self.get_chose_data()
        self.af, ax = plt.subplots(2,2, figsize = (9, 9), dpi = 100)
        
#        self.af = Figure(figsize=(16, 8.5), dpi=90)
#        ax1 = self.af.add_subplot(1,1, 1)
#        ax2 = self.af.add_subplot(2,2, 2)
#        ax3 = self.af.add_subplot(2,2, 3)
#        ax4 = self.af.add_subplot(2,2, 4)


#        self.af.suptitle('Heatmap of Location')
#        i = 0
        for i, k2 in enumerate(self.methods):
            loc = chose_data[k2]
            loc_x = loc[0][:]
            loc_y = loc[1][:]
            loc_x = loc_x[~np.isnan(loc_x)].tolist()
            loc_y = loc_y[~np.isnan(loc_y)].tolist()
        
#            aa = self.af.add_subplot(2,2, i+1)
#        self.af, ax1 = plt.subplots(figsize = (7.4, 3.8), dpi = 100)
            h = ScatterPlot(self.filetime, loc_x, loc_y)
            if i == 0:
                h.plot_heatmap(self.af, ax[0,0], k2)
            elif i == 1:
                h.plot_heatmap(self.af, ax[0,1], k2)
            elif i == 2:
                h.plot_heatmap(self.af, ax[1,0], k2)
            elif i == 3:
                h.plot_heatmap(self.af, ax[1,1], k2)
            
#            i += 1

    def get_chose_data(self):
        try:
            with tb.open_file(self.path, mode = 'r') as h5file:
                if '/wnew_table' in h5file:
                    nt = h5file.root.wnew_table
                    if nt.nrows:
                        chose_data = {k2: [nt.cols._f_col('{}/x'.format(k2))[:], nt.cols._f_col('{}/y'.format(k2))[:]] for k2 in self.methods}
                        return chose_data
                    else:
                        print('there is no data in table')
                        messagebox.showinfo('show_table_info', 'there is no data in table')
                        
                else:
                    print('there is no related data created')
                    messagebox.showinfo('show_table_info', 'there is no related data table')
                    
        except IOError: 
            print('open h5 file error')
            messagebox.showerror(title = 'h5 file', message = 'open h5 file error')

    def embed_figures(self):
        self.canvas_frame = ttk.Frame(self.bar2)
#        self.canvas_frame.place(x = 5, y = 160 , width = 1540, height = 780)      
        self.canvas_frame.pack(side=tk.TOP,fill=tk.BOTH, expand=1)
        canvas = FigureCanvasTkAgg(self.af, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar_frame = tk.Frame(self.bar2)
#        self.toolbar_frame.place(x = 5, y = 950 , width = 1540, height = 45)
        self.toolbar_frame.pack(fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, self.toolbar_frame)
        toolbar.update()
        

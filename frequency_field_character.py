

import tkinter as tk
from tkinter import ttk, messagebox
#from Calender import Calendar
import tables as tb
import datetime
#import pytable_form as ptf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandastable import Table

from plot_class import ScatterPlot

from time_field_character import TimeField, FreField
from accelaration_character import AccField, FirstCh
#from la1 import LocAll


def main():
    root = tk.Tk()
    h5path = '//Users//yupan//Downloads//Pro_test1//IKTS.h5'
    LocField(root, h5path, 'loc_seq6s')
    root.mainloop()


class LocField:
    def __init__(self, root, h5path=None, field=None, startdate='start date'):
        self.root = root
        self.path = h5path
        self.field = field
        self.startdate = startdate
        self.root.geometry('1550x1000+30+30')
        self.set_root_title()
        self.init_para()
        self.init_gui()
        self.show_figures()

    def set_root_title(self):
        self.root.title('Location with Method : {}'.format(self.field))

    def init_para(self):
        self.init_para_data()
        self.init_para_func()
        self.init_para_fig()
# =============================================================================
#  init_para         start
# =============================================================================

    def init_para_data(self):
        self.isrange_var = tk.IntVar()
        self.isrange_var.set(0)

        self.x1_var = tk.DoubleVar()
        self.x2_var = tk.DoubleVar()
        self.y1_var = tk.DoubleVar()
        self.y2_var = tk.DoubleVar()

        self.lrange = {'x1': self.x1_var, 'x2': self.x2_var,
                       'y1': self.y1_var, 'y2': self.y2_var}

    def init_para_func(self):
        self.func_var = tk.IntVar()
        self.func_var.set(1)

        self.cfunction = tk.StringVar()
        self.cfunction.set('count')
        self.Function = ['count', 'mean theta', 'mean az', 'mean maxAmp_t', 'mean Energy25',
                         'sum Energy25', 'mean ZeroCrossf', 'mean fre_peak', 'mean fre_centroid', 'mean fre_wpeak']
        self.pfunc = {'count': ['loc', 'count'], 'mean theta': ['mean', 'theta'], 'mean az': ['mean', 'az'],
                      'mean maxAmp_t': ['mean', 'maxAmp_t', 'timefield'], 'mean Energy25': ['mean', 'Energy25', 'timefield'],
                      'sum Energy25': ['sum', 'Energy25', 'timefield'], 'mean ZeroCrossf': ['mean', 'ZeroCrossf', 'timefield'],
                      'mean fre_peak': ['mean', 'fre_peak', 'frefield'], 'mean fre_centroid': ['mean', 'fre_centroid', 'frefield'], 'mean fre_wpeak': ['mean', 'fre_wpeak', 'frefield']}

        self.time_interval_var = tk.StringVar()
        self.time_interval_var.set('1 day')
        self.Time_interval = ['1 minute', '5 minutes',
                              '10 minutes', '30 minutes', '1 hour', '2 hours', '1 day']

    def init_para_fig(self):
        self.pcolormap = tk.StringVar()
        self.pcolormap.set('jet')
        self.pvmin = tk.IntVar()
        self.pvmin.set(0)
        self.pvmax = tk.IntVar()
        self.pvmax.set(100)
        self.plinewidth = tk.StringVar()
        self.plinewidth.set('0')
        self.pblock = tk.IntVar()
        self.pblock.set(100)
        self.colormap = ['jet', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
                         'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'hsv',
                         'gist_rainbow', 'rainbow', 'nipy_spectral', 'gist_ncar']
        self.vmin = [0, 5, 10, 20, 50, 100, -2, ]
        self.vmax = [10, 20, 50, 100, 200, 500, 1000, 2000, 360, 1]
        self.linewidth = ['0', '0.1', '0.2', '0.3',
                          '0.4', '0.5', '0.6', '0.7', '0.8', '0.9']
        self.block = [20, 40, 80, 100, 200]

        self.hrot = tk.IntVar()
        self.hrot.set(45)
        self.hwidth = tk.StringVar()
        self.hwidth.set('0.8')
        self.hcolor = tk.StringVar()
        self.hcolor.set('blue')
        self.hfontsize = tk.IntVar()
        self.hfontsize.set(8)
        self.rot = [0, 10, 20, 30, 40, 45, 50, 60, 70, 80, 90]
        self.width = ['0.1', '0.2', '0.3', '0.4',
                      '0.5', '0.6', '0.7', '0.8', '0.9']
        self.color = ['blue', 'green', 'red',
                      'cyan', 'magenta', 'yellow', 'black']
        self.fontsize = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
# =============================================================================
#       init_para     end
# =============================================================================

    def init_gui(self):
        self.init_gui_menubar()
        self.init_gui_bar1()
        self.init_gui_bar2()
        self.init_gui_bar3()
# =============================================================================
#     init_gui menubar
# =============================================================================

    def init_gui_menubar(self):
        menubar = tk.Menu(self.root)
        locmenu = tk.Menu(menubar, tearoff=0)
        locmenu.add_command(label='Data Table', command=self.loc_data_table)
#        locmenu.add_command(label = 'Geiger6s', command = self.loc_geiger6s)
#        locmenu.add_separator()
#        locmenu.add_command(label = 'Sequential4s', command = self.loc_sequential4s)
#        locmenu.add_command(label = 'Geiger4s', command = self.loc_geiger4s)
#        locmenu.add_separator()
#        locmenu.add_command(label = 'All Methods', command = self.loc_all_methods)
        menubar.add_cascade(label='Location', menu=locmenu)

        charmenu = tk.Menu(menubar, tearoff=0)
        charmenu.add_command(label='Time Field', command=self.time_field)
        charmenu.add_command(label='Freq Field', command=self.freq_field)
        menubar.add_cascade(label='Character', menu=charmenu)

        accemenu = tk.Menu(menubar, tearoff=0)
        accemenu.add_command(label='Acceleration', command=self.acceleration)
        menubar.add_cascade(label='Acceleration', menu=accemenu)

        firstchmenu = tk.Menu(menubar, tearoff=0)
        firstchmenu.add_command(label='First Channel',
                                command=self.firstchannel)
        menubar.add_cascade(label='Channel', menu=firstchmenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.about)
        helpmenu.add_command(label="Help", command=self.help_box)
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.root.config(menu=menubar)

# =============================================================================
#       init_gui  bar1
# =============================================================================
    def init_gui_bar1(self):
        self.bar1 = ttk.LabelFrame(self.root, text='Set Parameters Panel',
                                   width=1005, height=165, relief='ridge', borderwidth=1)
        self.bar1.place(x=5, y=5, width=1005, height=160)

        ttk.Label(self.bar1, text='Choose Range:').place(
            x=5, y=5, width=100, height=22)
        ttk.Radiobutton(self.bar1, text='Yes', variable=self.isrange_var, value=1,
                        command=self.choose_isrange).place(x=115, y=5,  width=50, height=22)
        ttk.Radiobutton(self.bar1, text='No', variable=self.isrange_var, value=0,
                        command=self.choose_isrange).place(x=175, y=5,  width=50, height=22)

        ttk.Label(self.bar1, text='x1:').place(x=5, y=27, width=20, height=50)
        self.scalex1 = tk.Scale(self.bar1, from_=-2000, to=1200, variable=self.x1_var, tickinterval=1600,
                                resolution=10, orient='horizontal', state='disabled', width=10)
        self.scalex1.place(x=30, y=27, width=250, height=50)
        self.scalex1.set(-2000)

        ttk.Label(self.bar1, text='y1:').place(x=5, y=77, width=20, height=50)
        self.scaley1 = tk.Scale(self.bar1, from_=-400, to=2000, variable=self.y1_var, tickinterval=1200,
                                resolution=10, orient='horizontal', state='disabled', width=10)
        self.scaley1.place(x=30, y=77, width=250, height=50)
        self.scaley1.set(-400)

        ttk.Label(self.bar1, text='x2:').place(
            x=310, y=27, width=20, height=50)
        self.scalex2 = tk.Scale(self.bar1, from_=-2000, to=1200, variable=self.x2_var, tickinterval=1600,
                                resolution=10, orient='horizontal', state='disabled', width=10)
        self.scalex2.place(x=335, y=27, width=250, height=50)
        self.scalex2.set(-2000)

        ttk.Label(self.bar1, text='y2:').place(
            x=310, y=77, width=20, height=50)
        self.scaley2 = tk.Scale(self.bar1, from_=-400, to=2000, variable=self.y2_var, tickinterval=1200,
                                resolution=10, orient='horizontal', state='disabled', width=10)
        self.scaley2.place(x=335, y=77, width=250, height=50)
        self.scaley2.set(-400)

        self.brange = ttk.Button(
            self.bar1, text='Range Confirm', state='disabled', command=self.range_confirm)
        self.brange.place(x=290, y=3, width=100, height=30)

        ttk.Separator(self.bar1, orient='vertical').place(
            x=615, y=5, width=5, height=130)

        ttk.Label(self.bar1, text='Functions:').place(
            x=650, y=5, width=100, height=25)
        ttk.Radiobutton(self.bar1, text='Heatmap', variable=self.func_var, value=1,
                        command=self.choose_func).place(x=760, y=5,  width=80, height=22)
        ttk.Radiobutton(self.bar1, text='Time vs Count', variable=self.func_var,
                        value=2, command=self.choose_func).place(x=850, y=5,  width=100, height=22)

        ttk.Label(self.bar1, text='Heatmap:').place(
            x=650, y=40, width=100, height=25)
        self.comfunc1 = ttk.Combobox(
            self.bar1, textvariable=self.cfunction, value=self.Function, width=150, state='randonly')
        self.comfunc1.place(x=760, y=40, width=150, height=25)
        self.comfunc1.current(0)
#        self.comfunc1.bind('<<ComboboxSelected>>', self.get_heatmap_function)

        ttk.Label(self.bar1, text='Time vs Count:').place(
            x=650, y=75, width=100, height=25)
        self.comfunc2 = ttk.Combobox(self.bar1, textvariable=self.time_interval_var,
                                     value=self.Time_interval, width=150, state='disabled')
        self.comfunc2.place(x=760, y=75, width=150, height=25)
        self.comfunc2.current(6)
#        self.comfunc2.bind('<<ComboboxSelected>>', self.get_time_interval)

        self.bshow = ttk.Button(
            self.bar1, text='Show Figures', command=self.show_figures)
        self.bshow.place(x=750, y=110, width=100, height=25)
# =============================================================================
#        init_gui  bar3
# =============================================================================

    def init_gui_bar3(self):
        self.bar3 = ttk.LabelFrame(
            self.root, text='Set Plot Style', width=520, height=165, relief='ridge', borderwidth=1)
        self.bar3.place(x=1020, y=5, width=520, height=160)
        ttk.Label(self.bar3, text='Colormap:').place(
            x=5, y=5, width=65, height=23)
        self.cplotcolor = ttk.Combobox(
            self.bar3, textvariable=self.pcolormap, value=self.colormap, width=100, state='randonly')
        self.cplotcolor.place(x=75, y=5, width=75, height=23)
        self.cplotcolor.current(0)
        self.cplotcolor.bind('<<ComboboxSelected>>', self.state_update)

        ttk.Label(self.bar3, text='Vmin:').place(
            x=5, y=33, width=65, height=23)
        self.cplotvmin = ttk.Combobox(
            self.bar3, textvariable=self.pvmin, value=self.vmin, width=100, state='randonly')
        self.cplotvmin.place(x=75, y=33, width=75, height=23)
        self.cplotvmin.current(0)
        self.cplotvmin.bind('<<ComboboxSelected>>', self.state_update)

        ttk.Label(self.bar3, text='Vmax:').place(
            x=5, y=61, width=65, height=23)
        self.cplotvmax = ttk.Combobox(
            self.bar3, textvariable=self.pvmax, value=self.vmax, width=100, state='randonly')
        self.cplotvmax.place(x=75, y=61, width=75, height=23)
        self.cplotvmax.current(3)
        self.cplotvmax.bind('<<ComboboxSelected>>', self.state_update)

        ttk.Label(self.bar3, text='Linewidth:').place(
            x=5, y=89, width=65, height=23)
        self.cplotwidth = ttk.Combobox(
            self.bar3, textvariable=self.plinewidth, value=self.linewidth, width=100, state='randonly')
        self.cplotwidth.place(x=75, y=89, width=75, height=23)
        self.cplotwidth.current(0)
        self.cplotwidth.bind('<<ComboboxSelected>>', self.state_update)

        ttk.Label(self.bar3, text='Block:').place(
            x=5, y=117, width=65, height=23)
        self.cblock = ttk.Combobox(
            self.bar3, textvariable=self.pblock, value=self.block, width=100, state='randonly')
        self.cblock.place(x=75, y=117, width=75, height=23)
        self.cblock.current(3)
        self.cblock.bind('<<ComboboxSelected>>', self.state_update)

        # =============================================================================
        #  plot style 2
        # =============================================================================
        ttk.Label(self.bar3, text='Rot:').place(
            x=175, y=5, width=65, height=23)
        self.chbins = ttk.Combobox(
            self.bar3, textvariable=self.hrot, value=self.rot, width=100, state='randonly')
        self.chbins.place(x=220, y=5, width=70, height=23)
        self.chbins.current(5)
        self.chbins.bind('<<ComboboxSelected>>', self.state_update)

        ttk.Label(self.bar3, text='Color:').place(
            x=175, y=35, width=65, height=23)
        self.chcolor = ttk.Combobox(
            self.bar3, textvariable=self.hcolor, value=self.color, width=100, state='randonly')
        self.chcolor.place(x=220, y=35, width=70, height=23)
        self.chcolor.current(0)
        self.chcolor.bind('<<ComboboxSelected>>', self.state_update)

        ttk.Label(self.bar3, text='Width:').place(
            x=175, y=65, width=65, height=23)
        self.chrwidth = ttk.Combobox(
            self.bar3, textvariable=self.hwidth, value=self.width, width=100, state='randonly')
        self.chrwidth.place(x=220, y=65, width=70, height=23)
        self.chrwidth.current(7)
        self.chrwidth.bind('<<ComboboxSelected>>', self.state_update)

        ttk.Label(self.bar3, text='Fontsize:').place(
            x=175, y=95, width=65, height=23)
        self.chrwidth = ttk.Combobox(
            self.bar3, textvariable=self.hfontsize, value=self.fontsize, width=100, state='randonly')
        self.chrwidth.place(x=220, y=95, width=70, height=23)
        self.chrwidth.current(3)
        self.chrwidth.bind('<<ComboboxSelected>>', self.state_update)

        self.bupdate = ttk.Button(
            self.bar3, text='Update Figures', command=self.update_figures, state='disabled')
        self.bupdate.place(x=300, y=50, width=100, height=25)

# =============================================================================
#        init_gui  bar2
# =============================================================================
    def init_gui_bar2(self):
        self.bar2 = ttk.LabelFrame(
            self.root, text='Figures Panel', width=1540, height=830, relief='sunken', borderwidth=1)
        self.bar2.place(x=5, y=170, width=1540, height=820)
# =============================================================================
#  show figures
# =============================================================================

    def show_figures(self):
        self.is_frame_free()
        self.create_figures()
        self.embed_figures()

    def create_figures(self):
        if self.func_var.get() == 1:

            loc = self.get_chose_data()
            self.af, ax = plt.subplots(figsize=(8, 7.7), dpi=100)

            loc_x = loc[0][:]
            loc_y = loc[1][:]
            index = self.get_range_index()
            loc_x1 = np.array(loc_x)[index]
            loc_y1 = np.array(loc_y)[index]
            if not self.isrange_var.get():
                if self.cfunction.get() == 'count':
                    #                    loc_x1 = loc_x[~np.isnan(loc_x)].tolist()
                    #                    loc_y1 = loc_y[~np.isnan(loc_y)].tolist()
                    h = ScatterPlot(self.startdate, loc_x1, loc_y1)
                    h.plot_heatmap(self.af, ax, self.field, vmin=self.pvmin.get(), vmax=self.pvmax.get(),
                                   cmap=self.pcolormap.get(), linewidths=float(self.plinewidth.get()))

                else:
                    if (self.cfunction.get() == 'mean theta') or (self.cfunction.get() == 'mean az'):
                        z = self.get_chose_data_c(
                            1, self.pfunc[self.cfunction.get()])
                        z1 = z[index]
#                        h = ScatterPlot('aa', loc_x1, loc_y1, z1, ca = self.pfunc[self.cfunction.get()][1])
#                        h.plot_heatmap(self.af, ax, self.field, vmin = self.pvmin.get(), vmax = self.pvmax.get(),
#                                       cmap = self.pcolormap.get(), linewidths = float(self.plinewidth.get()),
#                                       cha = self.pfunc[self.cfunction.get()][1], aspect = self.pfunc[self.cfunction.get()][0])

                    else:
                        ch = self.get_chose_data_c(0)[index]
                        zarray = self.get_chose_data_c(2, self.pfunc[self.cfunction.get()])[
                            np.array(index), :]
                        z1 = [zarray[k, v] for k, v in enumerate(ch)]
                        if self.cfunction.get() == 'mean maxAmp_t':
                            z1 = np.round(np.array(z1)/1000, 1)
                        elif self.cfunction.get() == 'mean Energy25':
                            z1 = np.round(np.array(z1)/1E9, 2)
                        elif self.cfunction.get() == 'sum Energy25':
                            z1 = np.round(np.array(z1)/1E10, 2)

                    h = ScatterPlot(self.startdate, loc_x1, loc_y1,
                                    z1, ca=self.pfunc[self.cfunction.get()][1])
                    h.plot_heatmap(self.af, ax, self.field, vmin=self.pvmin.get(), vmax=self.pvmax.get(),
                                   cmap=self.pcolormap.get(), linewidths=float(self.plinewidth.get()),
                                   cha=self.pfunc[self.cfunction.get()][1], aspect=self.pfunc[self.cfunction.get()][0])

            else:
                if self.cfunction.get() == 'count':
                    h = ScatterPlot(self.startdate, loc_x1, loc_y1, areatop=[self.x1_var.get(), self.y2_var.get()],
                                    areabottom=[
                                        self.x2_var.get(), self.y1_var.get()],
                                    block=self.pblock.get())
                    h.plot_heatmap(self.af, ax, self.field, vmin=self.pvmin.get(), vmax=self.pvmax.get(),
                                   cmap=self.pcolormap.get(), linewidths=float(self.plinewidth.get()), sensor=False)

                else:
                    if (self.cfunction.get() == 'mean theta') or (self.cfunction.get() == 'mean az'):
                        z = self.get_chose_data_c(
                            1, self.pfunc[self.cfunction.get()])
                        z1 = z[index]

                    else:
                        ch = self.get_chose_data_c(0)[index]
                        zarray = self.get_chose_data_c(2, self.pfunc[self.cfunction.get()])[
                            np.array(index), :]
                        z1 = [zarray[k, v] for k, v in enumerate(ch)]
                        if self.cfunction.get() == 'mean maxAmp_t':
                            z1 = np.round(np.array(z1)/1000, 1)
                        elif self.cfunction.get() == 'mean Energy25':
                            z1 = np.round(np.array(z1)/1E8, 1)
                        elif self.cfunction.get() == 'sum Energy25':
                            z1 = np.round(np.array(z1)/1E9, 1)

                    h = ScatterPlot(self.startdate, loc_x1, loc_y1, z1, areatop=[self.x1_var.get(), self.y2_var.get()],
                                    areabottom=[
                                        self.x2_var.get(), self.y1_var.get()],
                                    block=self.pblock.get(),
                                    ca=self.pfunc[self.cfunction.get()][1])
                    h.plot_heatmap(self.af, ax, self.field, vmin=self.pvmin.get(), vmax=self.pvmax.get(),
                                   cmap=self.pcolormap.get(), linewidths=float(self.plinewidth.get()),
                                   cha=self.pfunc[self.cfunction.get(
                                   )][1], aspect=self.pfunc[self.cfunction.get()][0],
                                   sensor=False)

        elif self.func_var.get() == 2:
            hist_data = self.hist_figure_data()
            if hist_data.empty:
                messagebox.showinfo(title='Data Info',
                                    message='There is No relevant event')
            else:
                self.af = Figure(figsize=(8, 7.7), dpi=100)
                ax = self.af.add_subplot(111)
                hist_data['count'].plot(kind='bar', title="Histogram: count vs. time (with {})".format(self.field),
                                        legend=False, fontsize=self.hfontsize.get(), ax=ax, rot=self.hrot.get(),
                                        color=self.hcolor.get(), width=float(self.hwidth.get()))

                for p in ax.patches:
                    ax.annotate(str(p.get_height()), (p.get_x() +
                                p.get_width()/2, p.get_height()))

                ax.set_xlabel("Time", fontsize=12)
                ax.set_ylabel('Count', fontsize=12)

    def get_chose_data(self):
        try:
            with tb.open_file(self.path, mode='r') as h5file:
                if '/wnew_table' in h5file:
                    nt = h5file.root.wnew_table
                    if nt.nrows:
                        chose_data = [nt.cols._f_col(
                            '{}/x'.format(self.field))[:], nt.cols._f_col('{}/y'.format(self.field))[:]]
                        return chose_data
                    else:
                        print('there is no data in table')
                        messagebox.showinfo(
                            'show_table_info', 'there is no data in table')

                else:
                    print('there is no related data created')
                    messagebox.showinfo('show_table_info',
                                        'there is no related data table')

        except IOError:
            print('open h5 file error')
            messagebox.showerror(title='h5 file', message='open h5 file error')

    def get_chose_data_c(self, level, flist=None):
        try:
            with tb.open_file(self.path, mode='r') as h5file:
                if '/wnew_table' in h5file:
                    nt = h5file.root.wnew_table
                    if nt.nrows:
                        if level == 1:
                            chose_data = nt.cols._f_col(
                                'oda/{}'.format(flist[1]))[:]
                        elif level == 0:
                            chose_data = nt.cols._f_col('shorttime_Ch')[:]
#                            chose_data = chose_data[:,0]
                        elif level == 2:
                            ch = ['ch0', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5']
                            chose_data = np.array(
                                [nt.cols._f_col('{}/{}/{}'.format(a, flist[2], flist[1]))[:] for a in ch]).T
                        return chose_data
                    else:
                        print('there is no data in table')
                        messagebox.showinfo(
                            'show_table_info', 'there is no data in table')

                else:
                    print('there is no related data created')
                    messagebox.showinfo('show_table_info',
                                        'there is no related data table')

        except IOError:
            print('open h5 file error')
            messagebox.showerror(title='h5 file', message='open h5 file error')

    def get_chose_data_d(self):
        try:
            with tb.open_file(self.path, mode='r') as h5file:
                if '/wnew_table' in h5file:
                    nt = h5file.root.wnew_table
                    if nt.nrows:
                        chose_data = {'filename': nt.cols._f_col('filename')[:],
                                      'shorttime_CH': nt.cols._f_col('shorttime_Ch')[:],
                                      'x': nt.cols._f_col('{}/x'.format(self.field))[:],
                                      'y': nt.cols._f_col('{}/y'.format(self.field))[:],
                                      'theta': nt.cols._f_col('oda/theta')[:]}
                        return chose_data
                    else:
                        print('there is no data in table')
                        messagebox.showinfo(
                            'show_table_info', 'there is no data in table')

                else:
                    print('there is no related data created')
                    messagebox.showinfo('show_table_info',
                                        'there is no related data table')

        except IOError:
            print('open h5 file error')
            messagebox.showerror(title='h5 file', message='open h5 file error')

    def get_measure_time_data(self):
        try:
            with tb.open_file(self.path, mode='r') as h5file:
                if '/wnew_table' in h5file:
                    nt = h5file.root.wnew_table
                    if nt.nrows:
                        if self.time_interval_var.get() == '1 day':
                            measD = nt.cols.meastimeD[:]
                            measuretime_data = [measD[i].decode(
                                'UTF-8') for i in range(nt.nrows)]
                        else:
                            #                        measD = nt.cols.meastimeD[:]
                            #                        measH = nt.cols.meastimeH[:]
                            measT = nt.cols.meastimeT[:]
    #                        measuretime_data = [measD[i].decode('UTF-8') + ' ' + measH[i].decode('UTF-8').replace('.',':') for i in range(nt.nrows)]
                            measuretime_data = [
                                measT[i][:-7].decode('UTF-8') for i in range(nt.nrows)]

                        return measuretime_data
                    else:
                        print('there is no data in table')
                        messagebox.showinfo(
                            'show_table_info', 'there is no data in table')

                else:
                    print('there is no related data created')
                    messagebox.showinfo('show_table_info',
                                        'there is no related data table')

        except IOError:
            print('open h5 file error')
            messagebox.showerror(title='h5 file', message='open h5 file error')

    def get_range_index(self):
        loc_data = self.get_chose_data()
        x = loc_data[0][:]
        y = loc_data[1][:]
        if self.isrange_var.get():
            self.range_confirm()
            return list(np.where((x >= int(self.x1_var.get())) & (x <= int(self.x2_var.get())) & (y >= int(self.y1_var.get())) & (y <= int(self.y2_var.get())))[0])
        else:
            return list(np.where(~np.isnan(x))[0])

    def get_time_interval(self):
        time_interval = self.time_interval_var.get()
        if time_interval == '1 minute':
            dt = '1Min'
        elif time_interval == '5 minutes':
            dt = '5Min'
        elif time_interval == '10 minutes':
            dt = '10Min'
        elif time_interval == '30 minutes':
            dt = '30Min'
        elif time_interval == '1 hour':
            dt = 'H'
        elif time_interval == '2 hours':
            dt = '2H'
        elif time_interval == '1 day':
            dt = 'D'
        return dt

    def hist_figure_data(self):
        row_index = self.get_range_index()
        if len(row_index) == 0:
            messagebox.showinfo(
                'Data Info', 'There is No event in the selected location range')
            return pd.DataFrame()
        else:
            time_interval = self.get_time_interval()

            measure_time = self.get_measure_time_data()
            count = [1 if x in row_index else 0 for x in range(
                len(measure_time))]
            if self.time_interval_var.get() == '1 day':
                measT = [datetime.datetime.strptime(
                    x, '%d.%m.%Y') for x in measure_time]
            else:
                measT = [datetime.datetime.strptime(
                    x, '%d.%m.%Y.%H.%M.%S') for x in measure_time]
#                measT = [datetime.datetime.strptime(x,'%H:%M:%S') for x in measure_time]

            f = pd.DataFrame({'time': measT, 'count': count})
#            f['time'] = measT
#            f['count'] = count
            f.index = f['time']
            k = f.resample('{}'.format(time_interval)).sum()
            k['time'] = k.index

            return k

    def embed_figures(self):
        self.canvas_frame = ttk.Frame(self.bar2)
#        self.canvas_frame.place(x = 5, y = 160 , width = 1540, height = 780)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas = FigureCanvasTkAgg(self.af, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar_frame = tk.Frame(self.bar2)
#        self.toolbar_frame.place(x = 5, y = 950 , width = 1540, height = 45)
        self.toolbar_frame.pack(fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, self.toolbar_frame)
        toolbar.update()

    def is_frame_free(self):
        try:
            self.canvas_frame.destroy()
            self.toolbar_frame.destroy()
        except:
            pass

# =============================================================================
# func
# =============================================================================

    def choose_isrange(self):
        if self.isrange_var.get():
            self.scalex1.config(state='active')
            self.scalex2.config(state='active')
            self.scaley1.config(state='active')
            self.scaley2.config(state='active')
            self.brange.config(state='!disabled')
#            self.comfunc1.config(state = 'disabled')
        else:
            self.scalex1.config(state='disabled')
            self.scalex2.config(state='disabled')
            self.scaley1.config(state='disabled')
            self.scaley2.config(state='disabled')
            self.brange.config(state='disabled')
#            self.comfunc1.config(state = 'randonly')

    def range_confirm(self):
        if (self.x1_var.get() < self.x2_var.get()) & (self.y1_var.get() < self.y2_var.get()):
            #            self.bottom_loc = [self.x1_var.get(), self.y1_var.get()]
            #            self.top_loc = [self.x2_var.get(), self.y2_var.get()]
            ttk.Label(self.bar1, text='({}, {}) -> ({}, {})'.format(int(self.x1_var.get()),
                                                                    int(self.y1_var.get()), int(self.x2_var.get()), int(self.y2_var.get()))).place(x=400, y=3, width=200, height=30)
        else:
            messagebox.showerror(title='range error',
                                 message='x1 is langer than x2')

    def choose_func(self):
        if self.func_var.get() == 1:
            self.comfunc1.config(state='randonly')
            self.comfunc2.config(state='disabled')
        elif self.func_var.get() == 2:
            self.comfunc1.config(state='disabled')
            self.comfunc2.config(state='randonly')
#    def get_heatmap_function(self, event = None):
#        pass
#    def get_time_interval(self, event = None):
#        pass
#    def show_figures(self):
#        pass

    def state_update(self, event=None):
        self.bupdate.config(state='!disabled')

    def update_figures(self):
        self.show_figures()
# =============================================================================
# menu functions
# =============================================================================

    def loc_data_table(self):
        dtawin = tk.Toplevel(self.root)
        dtawin.geometry('600x400+200+100')
        dtawin.title('Table: {}'.format(self.field))
        f = ttk.Frame(dtawin)
        f.pack(fill=tk.BOTH, expand=1)
        chose_data = self.get_chose_data_d()
        index = self.get_range_index()
        df = pd.DataFrame()
        for k in chose_data.keys():
            df[k] = list(chose_data[k][index])
            pt = Table(f, dataframe=df, showtoolbar=False, showstatusbar=True)
            pt.show()
#    def loc_sequential6s(self):
#        pass
#    def loc_geiger6s(self):
#        pass
#    def loc_sequential4s(self):
#        pass
#    def loc_geiger4s(self):
#        pass
#    def loc_all_methods(self):
#        pass

    def time_field(self):
        tf = tk.Toplevel(self.root)
        TimeField(tf, self.path, 'timefield', title=self.field,
                  isrange=True, index=self.get_range_index())

    def freq_field(self):
        ff = tk.Toplevel(self.root)
        FreField(ff, self.path, 'frefield', title=self.field,
                 isrange=True, index=self.get_range_index())

    def acceleration(self):
        af = tk.Toplevel(self.root)
        AccField(af, self.path, 'oda', title=self.field,
                 isrange=True, index=self.get_range_index())

    def firstchannel(self):
        cf = tk.Toplevel(self.root)
        FirstCh(cf, self.path, 'oda', title=self.field,
                isrange=True, index=self.get_range_index())

    def help_box(self):
        pass

    def about(self):
        pass


if __name__ == '__main__':
    main()

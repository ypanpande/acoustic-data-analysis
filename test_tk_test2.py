

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import tables as tb
from test_class_plot2 import ScatterPlot
import datetime
import pandas as pd
#import seaborn as sns
import matplotlib.pyplot as plt

PROGRAM_NAME = 'Data Analyse Panel'
#LOC_METHODS = ['--Choose Loc Method--','Sequential6s', 'Geiger6s','Sequential4s','Geiger4s']
LOC_METHODS = ['--Choose Loc Method--','loc_seq6s','loc_geiger6s','loc_seq4s','loc_geiger4s']
TIMEFIELD_PRAMETERS  = ['--Timefield Not Selected--','maxAmp_t', 'time_peak','Energy','ZeroCrossf','rise_time','RA']
FREFIELD_PRAMETERS = ['--Frefield Not Selected--','maxAmp_f', 'fre_peak','fre_centroid','fre_wpeak','Power']
DAY = [str(i+1).zfill(2) for i in range(31)]
MONTH = [str(i+1).zfill(2) for i in range(12)]
YEAR = ['2018', '2019','2020','2021','2022']
TIME_INTERVAL = ['--Choose Time Interval--','1 minute','5 minutes','10 minutes','30 minutes','1 hour','2 hours','1 day']
CH = ['-- Choose Channel--', 'ch0', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5']

class CH_s(tb.IsDescription):
    _v_pos = 2
    class picktimes(tb.IsDescription):
        pickt = tb.FloatCol()
        
     
_s()

    
class loc_s(tb.IsDescription):
    _v_pos = 1
    x = tb.FloatCol(pos = 0)
    y = tb.FloatCol(pos = 1)
    t0 = tb.FloatCol(pos = 2)
    res = tb.FloatCol(pos = 3)
    aver_res = tb.FloatCol(pos = 4)
    
    
    
class Resultnested(tb.IsDescription):
    foldername = tb.StringCol(32, pos = 0)
    filename = tb.StringCol(32, pos = 1)
    meastimeD = tb.StringCol(32, pos = 2)
    meastimeH = tb.StringCol(32, pos = 3)
    picktimearray = tb.FloatCol(shape = (6), pos = 4)
    shorttime_Ch = tb.UInt16Col(8, pos = 5)
    shorttime_t = tb.IQstatistic(pos = 6)
    loc_seq6s = loc_s()
    loc_geiger6s = loc_s()
    loc_seq4s = loc    


       
class graphpanel:
    def __init__(self, root):
        self.start_time_day = tk.StringVar()
        self.start_time_month = tk.StringVar()
        self.start_time_year = tk.StringVar()
        self.end_time_day = tk.StringVar()
        self.end_time_month = tk.StringVar()
        self.end_time_year = tk.StringVar()
        
        self.location_method = tk.StringVar()
        
        self.x1 = tk.StringVar()
        self.x2 = tk.StringVar()
        self.y1 = tk.StringVar()
        self.y2 = tk.StringVar()
        
        self.time_interval_var = tk.StringVar()
        
        self.heatmap_show_var = tk.BooleanVar()
        self.hist_show_var = tk.BooleanVar()
        self.timefield_show_var = tk.BooleanVar()
        self.frefield_show_var = tk.BooleanVar()
        
        self.channel = tk.StringVar()
        
        self.timefield_var = tk.StringVar()
        self.frefield_var = tk.StringVar()
        
        self.root = root
        self.root.title(PROGRAM_NAME)
        
        self.init_settings()
        self.init_gui()
        
        
    def init_settings(self):
        self.init_setting = {
                'start_time': '01012018',
                'end_time': '01012018',
                'loc_method':LOC_METHODS[0],
                'heatmap': 'false',
                'top_loc':[None,None],
                'bottom_loc': [None,None],
                'time_interval':TIME_INTERVAL[0],
                'timefield':TIMEFIELD_PRAMETERS[0],
                'hist': 'false',
                'frefield':FREFIELD_PRAMETERS[0],
                'channel':CH[0]
                }
        
    def init_gui(self):
        self.create_top_settings_bar()
        #self.create_right_settings_bar()
        self.create_heatmap_bar()
        self.create_hist_bar()
        self.create_timefield_bar()
        self.create_frefield_bar()
    
    def create_top_settings_bar(self):
        topbar_frame = tk.Frame(self.root, height = 50 , width  = 780, relief = 'ridge', borderwidth = 1)
        topbar_frame.grid(row = 0, column = 0, rowspan = 10, columnspan= 25, 
                     sticky= 'n'+'w'+'e'+'s', padx=4, pady=4)
        tk.Label(topbar_frame, text = 'Time Range:',font=("Helvetica", 11), bg = 'peach puff', relief = 'ridge', borderwidth = 1).grid(row = 1, column = 0, columnspan = 2, padx = 2, pady = 5)
        
        tk.Label(topbar_frame, text = 'From', font=("Helvetica", 10), fg = 'blue').grid(row = 4, column = 0, rowspan = 2, padx = 3, pady = 5)
        combo_start_day = ttk.Combobox(topbar_frame, textvariable = self.start_time_day, value = DAY, width = 2, state = 'randonly')
        combo_start_day.grid(row=4, column=1, rowspan = 2, padx = 3, pady = 5)
        combo_start_day.current(0)
        combo_start_day.bind('<<ComboboxSelected>>', self.start_time_day_changed)
#        tk.Spinbox(topbar_frame, from_=1, to=31, width=3,
#                textvariable=self.start_time_day, command=self.start_time_day_changed).grid(row=4, column=1, rowspan = 2, padx = 3, pady = 5)
        combo_start_month = ttk.Combobox(topbar_frame, textvariable = self.start_time_month, value = MONTH, width = 2, state = 'randonly')
        combo_start_month.grid(row=4, column=2, rowspan = 2, padx = 3, pady = 5)
        combo_start_month.current(0)
        combo_start_month.bind('<<ComboboxSelected>>', self.start_time_month_changed)
        
        
#        tk.Spinbox(topbar_frame, from_=1, to=12, width=3,
#                textvariable=self.start_time_month, command=self.start_time_month_changed).grid(row=4, column=2, rowspan = 2, padx = 3, pady = 5)
        combo_start_year = ttk.Combobox(topbar_frame, textvariable = self.start_time_year, value = YEAR, width = 4, state = 'randonly')
        combo_start_year.grid(row=4, column=3, rowspan = 2, columnspan=2, padx = 3, pady = 5)
        combo_start_year.current(0)
        combo_start_year.bind('<<ComboboxSelected>>', self.start_time_year_changed)
        
        
#        tk.Spinbox(topbar_frame, from_=2018, to=2022, width=5,
#                textvariable=self.start_time_year, command=self.start_time_year_changed).grid(row=4, column=3, rowspan = 2, columnspan=2, padx = 3, pady = 5)
        
        tk.Label(topbar_frame, text = 'To', font=("Helvetica", 10), fg = 'blue').grid(row = 4, column = 6, rowspan = 2, padx = 10, pady = 5)
        
        combo_end_day = ttk.Combobox(topbar_frame, textvariable = self.end_time_day, value = DAY, width = 2, state = 'randonly')
        combo_end_day.grid(row=4, column=7, rowspan = 2, padx = 3, pady = 5)
        combo_end_day.current(0)
        combo_end_day.bind('<<ComboboxSelected>>', self.end_time_day_changed)
        
#        tk.Spinbox(topbar_frame, from_=1, to=31, width=3,
#                textvariable=self.end_time_day, command=self.end_time_day_changed).grid(row=4, column=7, rowspan = 2, padx = 3, pady = 5)
        
        combo_end_month = ttk.Combobox(topbar_frame, textvariable = self.end_time_month, value = MONTH, width = 2, state = 'randonly')
        combo_end_month.grid(row=4, column=8, rowspan = 2, padx = 3, pady = 5)
        combo_end_month.current(0)
        combo_end_month.bind('<<ComboboxSelected>>', self.end_time_month_changed)
        
#        tk.Spinbox(topbar_frame, from_=1, to=12, width=3,
#                textvariable=self.end_time_month, command=self.end_time_month_changed).grid(row=4, column=8, rowspan = 2, padx = 3, pady = 5)
        
        combo_end_year = ttk.Combobox(topbar_frame, textvariable = self.end_time_year, value = YEAR, width = 4, state = 'randonly')
        combo_end_year.grid(row=4, column=9, rowspan = 2, columnspan=2, padx = 3, pady = 5)
        combo_end_year.current(0)
        combo_end_year.bind('<<ComboboxSelected>>', self.end_time_year_changed)
        
#        tk.Spinbox(topbar_frame, from_=2018, to=2022, width=5,
#                textvariable=self.end_time_year, command=self.end_time_year_changed).grid(row=4, column=9, rowspan = 2, columnspan=2, padx = 3, pady = 5)
        
        ttk.Separator(topbar_frame, orient = 'vertical').grid(row = 0, column = 11, rowspan = 10, sticky = 'ns', padx = 10)
        tk.Label(topbar_frame, text = 'Location Method:',font=("Helvetica", 11), bg = 'peach puff', relief = 'ridge', borderwidth = 1).grid(row = 1, column = 12, columnspan = 3, padx = 10, pady = 5)
        
        combo1 = ttk.Combobox(topbar_frame, textvariable = self.location_method, value = LOC_METHODS, width = 22, state = 'randonly')
        combo1.grid(row = 4, column = 12, rowspan = 2, columnspan = 3, padx = 10, pady = 2)
        #self.combo1['value'] = LOC_METHODS
        combo1.current(0)
        combo1.bind('<<ComboboxSelected>>', self.set_loc_method)
#        s = ttk.Style()
#        s.configure('TMenubutton', relief = 'sunken', borderwidth = 3, foreground = 'red', background = 'sky blue', highlightthickness = '20')
    
#    def create_right_settings_bar(self):
#        rightbar_frame = tk.Frame(self.root, height = 50, relief = 'ridge', borderwidth = 1)
#        rightbar_frame.grid(row = 0, column = 15, rowspan = 10, columnspan=10, 
#                     sticky= 'n'+'w'+'e'+'s', padx=4, pady=4)
        ttk.Separator(topbar_frame, orient = 'vertical').grid(row = 0, column = 16, rowspan = 10, sticky = 'ns', padx = 20)
        tk.Label(topbar_frame, text = 'Select Location Range(mm):', font=("Helvetica", 11), bg = 'peach puff', relief = 'ridge', borderwidth = 1).grid(row = 1, column = 17, columnspan = 5, padx = 2, pady = 5)
        tk.Label(topbar_frame, text = 'x1', font=("Helvetica", 10), fg = 'blue').grid(row = 4, column = 17, padx = 1, pady = 1)
        x1_entry = tk.Entry(topbar_frame, textvariable = self.x1, width = 8, validatecommand = self.x1_changed)
        x1_entry.grid(row = 4, column = 18, padx = 2, pady = 2)
        x1_entry.bind('<Return>', self.x1_changed)
        
        tk.Label(topbar_frame, text = 'x2', font=("Helvetica", 10), fg = 'blue').grid(row = 5, column = 17, padx = 1, pady = 5)
        x2_entry = tk.Entry(topbar_frame, textvariable = self.x2, width = 8)
        x2_entry.grid(row = 5, column = 18, padx = 2, pady = 5)
        x2_entry.bind('<Return>', self.x2_changed)
        
        tk.Label(topbar_frame, text = 'y1', font=("Helvetica", 10), fg = 'blue').grid(row = 4, column = 19, padx = 1, pady = 1)
        y1_entry = tk.Entry(topbar_frame, textvariable = self.y1, width = 8)
        y1_entry.grid(row = 4, column = 20, padx = 2, pady = 2)
        y1_entry.bind('<Return>', self.y1_changed)
        
        tk.Label(topbar_frame, text = 'y2', font=("Helvetica", 10), fg = 'blue').grid(row = 5, column = 19, padx = 1, pady = 5)
        y2_entry = tk.Entry(topbar_frame, textvariable = self.y2, width = 8)
        y2_entry.grid(row = 5, column = 20, padx = 2, pady = 5)
        y2_entry.bind('<Return>', self.y2_changed)
        
        confirm_button = ttk.Button(topbar_frame, text = 'Confirm', command = self.location_range_selected)
        confirm_button.grid(row = 5, column = 22, columnspan = 2, padx = 6, pady = 5)
        
        
        ttk.Separator(topbar_frame, orient = 'vertical').grid(row = 0, column = 24, rowspan = 10, sticky = 'ns', padx = 10)
        tk.Label(topbar_frame, text = 'Channel:',font=("Helvetica", 11), bg = 'peach puff', relief = 'ridge', borderwidth = 1).grid(row = 1, column = 25, columnspan = 3, padx = 10, pady = 5)
        
        combo_ch = ttk.Combobox(topbar_frame, textvariable = self.channel, value = CH, width = 22, state = 'randonly')
        combo_ch.grid(row = 4, column = 25, rowspan = 2, columnspan = 3, padx = 10, pady = 2)
        #self.combo1['value'] = LOC_METHODS
        combo_ch.current(0)
        combo_ch.bind('<<ComboboxSelected>>', self.set_channel)
        
    def create_heatmap_bar(self):
        heatmapbar_frame = tk.Frame(self.root, height = 450, width = 780, relief = 'ridge', borderwidth = 1)
        heatmapbar_frame.grid(row = 12, column = 0, rowspan = 10, columnspan=10, 
                     sticky= 'n'+'w'+'e'+'s', padx=4, pady=4)
        tk.Label(heatmapbar_frame, text = 'Heatmap', font=("Helvetica", 10), fg = 'blue').grid(row = 12, column = 0,  pady = 1)
        ttk.Checkbutton(heatmapbar_frame, text = 'Show', variable = self.heatmap_show_var, onvalue = 'true', offvalue = 'false', 
                       command = self.heatmap_show).grid(row = 12, column = 1,  pady = 1)
        self.heatmap_frame = tk.Frame(heatmapbar_frame, height = 390, width = 750,relief = 'groove', borderwidth = 0.5)
        self.heatmap_frame.grid(row = 13, column = 0, rowspan = 9, columnspan=10, 
                     sticky= 'n'+'w'+'e'+'s', padx=4, pady=4)
    def create_hist_bar(self):
        histbar_frame = tk.Frame(self.root, height = 450, width = 780, relief = 'ridge', borderwidth = 1)
        histbar_frame.grid(row = 24, column = 0, rowspan = 10, columnspan=10, 
                     sticky= 'n'+'w'+'e'+'s', padx=4, pady=4)
        tk.Label(histbar_frame, text = 'Histgramm (N vs time)', font=("Helvetica", 10), fg = 'blue').grid(row = 24, column = 0, pady = 1)
        ttk.Checkbutton(histbar_frame, text = 'Show', variable = self.hist_show_var, onvalue = 'true', offvalue = 'false', 
                       command = self.hist_show).grid(row = 24, column = 1,  pady = 1)
        
        combo_hist = ttk.Combobox(histbar_frame, textvariable = self.time_interval_var, value = TIME_INTERVAL, width = 22, state = 'randonly')
        combo_hist.grid(row = 24, column = 3,  columnspan = 3, padx = 1, pady = 2)
        combo_hist.current(0)
        combo_hist.bind('<<ComboboxSelected>>', self.set_time_interval)
        
        self.hist_frame = tk.Frame(histbar_frame, height = 390, width = 750,relief = 'groove', borderwidth = 0.5)
        self.hist_frame.grid(row = 25, column = 0, rowspan = 9, columnspan=10, 
                     sticky= 'n'+'w'+'e'+'s', padx=4, pady=4)
    def create_timefield_bar(self):
        timefieldbar_frame = tk.Frame(self.root, height = 450, width = 780, relief = 'ridge', borderwidth = 1)
        timefieldbar_frame.grid(row = 12, column = 15, rowspan = 10, columnspan=10, 
                     sticky= 'n'+'w'+'e'+'s', padx=4, pady=4)
        
        tk.Label(timefieldbar_frame, text = 'Hist time field', font=("Helvetica", 10), fg = 'blue').grid(row = 12, column = 15,  pady = 1)
        ttk.Checkbutton(timefieldbar_frame, text = 'Show', variable = self.timefield_show_var, onvalue = 'true', offvalue = 'false', 
                       command = self.timefield_show).grid(row = 12, column = 16,  pady = 1)
        combo2 = ttk.Combobox(timefieldbar_frame, textvariable = self.timefield_var, value = TIMEFIELD_PRAMETERS, width = 25, state = 'randonly')
        combo2.grid(row = 12, column = 17, columnspan = 3, padx = 1, pady = 2)
        combo2.current(0)
        combo2.bind('<<ComboboxSelected>>', self.set_timefield)
#        self.timefield_var.set(0)
#        ttk.OptionMenu(timefieldbar_frame, self.timefield_var, *TIMEFIELD_PRAMETERS).grid(row = 12, column = 16, columnspan = 2, padx = 1, pady = 2)
        self.timefield_frame = tk.Frame(timefieldbar_frame, height = 390, width = 750,relief = 'groove', borderwidth = 0.5)
        self.timefield_frame.grid(row = 13, column = 15, rowspan = 9, columnspan=10, 
                     sticky= 'n'+'w'+'e'+'s', padx=4, pady=4)
    def create_frefield_bar(self):
        frefieldbar_frame = tk.Frame(self.root, height = 450, width = 780, relief = 'ridge', borderwidth = 1)
        frefieldbar_frame.grid(row = 24, column = 15, rowspan = 10, columnspan=10, 
                     sticky= 'n'+'w'+'e'+'s', padx=4, pady=4)
        tk.Label(frefieldbar_frame, text = 'Hist frequency field', font=("Helvetica", 10), fg = 'blue').grid(row = 24, column = 15,  pady = 1)
        ttk.Checkbutton(frefieldbar_frame, text = 'Show', variable = self.frefield_show_var, onvalue = 'true', offvalue = 'false', 
                       command = self.frefield_show).grid(row = 24, column = 16,  pady = 1)
        combo3 = ttk.Combobox(frefieldbar_frame, textvariable = self.frefield_var, value = FREFIELD_PRAMETERS, width = 25, state = 'randonly')
        combo3.grid(row = 24, column = 17, columnspan = 3, padx = 1, pady = 2)
        combo3.current(0)
        combo3.bind('<<ComboboxSelected>>', self.set_frefield)

#        self.frefield_var.set('--Frefield Not Selected--')
#        ttk.OptionMenu(frefieldbar_frame, self.frefield_var, *FREFIELD_PRAMETERS).grid(row = 24, column = 16, columnspan = 2, padx = 1, pady = 2)
        self.frefield_frame = tk.Frame(frefieldbar_frame, height = 390, width = 750,relief = 'groove', borderwidth = 0.5)
        self.frefield_frame.grid(row = 25, column = 15, rowspan = 9, columnspan=10, 
                     sticky= 'n'+'w'+'e'+'s', padx=4, pady=4)
###########reset subpanel state######################################################
    def reset_heatmap_state(self):
        if self.heatmap_show_var.get():
            self.heatmap_show_var.set('false')
            self.not_show_heatmap()
    def reset_hist_state(self):
        if self.hist_show_var.get():
            self.hist_show_var.set('false')
            self.not_show_hist()
    def reset_timefield_state(self):
        if self.timefield_show_var.get():
            self.timefield_show_var.set('false')
            self.not_show_timefield()
    def reset_frefield_state(self):
        if self.frefield_show_var.get():
            self.frefield_show_var.set('false')
            self.not_show_frefield()
            
##########heatmap creation#####################################################################    

    def start_time_day_changed(self,event):
        self.set_start_time()

    def start_time_month_changed(self,event):
        self.set_start_time()

    def start_time_year_changed(self,event):
        self.set_start_time()

    def end_time_day_changed(self,event):
        self.set_end_time()

    def end_time_month_changed(self,event):
        self.set_end_time()

    def end_time_year_changed(self,event):
        self.set_end_time()

        
    def set_start_time(self):
        start_day = self.start_time_day.get()
        start_month = self.start_time_month.get()
        start_year = self.start_time_year.get()
        self.init_setting['start_time'] = start_year + start_month + start_day
        print(self.init_setting['start_time'])
        
        self.reset_heatmap_state()
        self.reset_hist_state()
        self.reset_timefield_state()
        self.reset_frefield_state()

            
    def get_start_time(self):
        return self.init_setting['start_time']
    
    def set_end_time(self):
        end_day = self.end_time_day.get()
        end_month = self.end_time_month.get()
        end_year = self.end_time_year.get()
        self.init_setting['end_time'] = end_year + end_month + end_day
        print(self.init_setting['end_time'])
        
        self.reset_heatmap_state()
        self.reset_hist_state()
        self.reset_timefield_state()
        self.reset_frefield_state()
            
    def get_end_time(self):
        return self.init_setting['end_time']
        
#    def loc_method_changed(self, event):
#        if self.location_method.get() == LOC_METHODS[0]:
#            return
#        else:
#        #self.location_method.get()
#            return self.location_method.get()
            
    def set_loc_method(self, event = None):
        self.init_setting['loc_method'] = self.location_method.get()
        print(self.init_setting['loc_method'])
        
        self.reset_heatmap_state()
        self.reset_hist_state()
        self.reset_timefield_state()
        self.reset_frefield_state()
            
    def get_loc_method(self):
        return self.init_setting['loc_method']        
    
    def heatmap_show(self):
        if self.heatmap_show_var.get():
            if self.is_time_correct():
                if self.is_loc_method():
                    self.create_heatmap()
                else:
                    self.setting_loc_info()
                    self.heatmap_show_var.set('false')
            else:
                self.setting_time_info()
                self.heatmap_show_var.set('false')
        else:
            self.not_show_heatmap()
                
#    def set_heatmap_show_var(self):
#        self.init_setting['heatmap'] = self.heatmap_show_var.get()
#        print(self.init_setting['heatmap']) 
#        
#    def get_heatmap_show_var(self):
#        return self.init_setting['heatmap']
    
    def is_time_correct(self):
        a = self.get_start_time()
        b = self.get_end_time()
        if int(a[:4]) == int(b[:4]):
             if int(a[4:6]) == int(b[4:6]):
                  if int(a[6:]) <= int(b[6:]):
                       return True
                  else:
                       return False
             elif int(a[4:6]) < int(b[4:6]):
                  return True
             else:
                  return False
        elif int(a[:4]) < int(b[:4]):
             return True
        else:
             return False

                 
    def setting_time_info(self, event = None):
        messagebox.showinfo('setting time', 'start time is greater than end time')        
    
    def create_heatmap(self):
        self.create_heatmap_figure()
        self.embedd_heatmap_figure()
        
    def create_heatmap_figure(self):
        start_time = self.get_start_time()
        end_time = self.get_end_time()
        loc_method = self.get_loc_method()
 
        loc = self.get_loc_data(start_time, end_time, loc_method)
        loc_x = loc[0][:]
        loc_y = loc[1][:]
        loc_x = loc_x[~np.isnan(loc_x)].tolist()
        loc_y = loc_y[~np.isnan(loc_y)].tolist()
        
#        self.af0 = Figure(figsize=(7.4, 3.8), dpi=100)
#        ax = self.af0.add_subplot(111)   
        self.af0, ax = plt.subplots(figsize = (7.4, 3.8), dpi = 100)
        h = ScatterPlot(start_time, loc_x, loc_y)
        h.plot_heatmap(self.af0, ax)
#        h.get_data_direct(start_time, loc_x, loc_x) 
##        h.length_data()
#        count = h.blockcount()
#        my_xticklabels = h.get_xticklabels()
#        my_yticklabels = h.get_yticklabels()
#        masktemp = h.get_mask()
##        
##        self.af0, ax = plt.subplots(figsize = (7.4, 3.8), dpi = 100)
###        ax = self.af0.add_subplot(111)
#        self.af0 = Figure(figsize=(7.4, 3.8), dpi=100)
#        ax = self.af0.add_subplot(111)        
#                           
#        g = sns.heatmap(count, vmin = 1, vmax = 100, annot = True, fmt = 'g', 
#                        ax = ax, xticklabels = my_xticklabels, yticklabels = my_yticklabels, 
#                        cmap = "jet", mask = masktemp, annot_kws={"size":7})        
#        h.figure_set(g)
#        plt.grid(True)
#        plt.close(self.af0)
#        g.set_xlabel('Horizontal (mm)')   
#        g.set_ylabel('Vertical (mm)') 
#        g.set_title('Heatmap of event {}'.format(self.filename))
#        agx = [3.6, 20.2, 25,25.5,20.2,3.8,3.6]
#        agy = [4.5, 4.5, 5.1,19.1,20,20,4.5]
#        arx = [6, 29, 29 ,6,6]
#        ary = [7, 7, 17.9, 17.9,7]
#        g.plot(agx,agy,color='g',linestyle = '--')
#        g.plot(arx,ary, color='r',linestyle = ':')

#        h.heatmap(a)
#        h.heatmap(False)

#        from PIL import ImageTk, Image
#        
#        start_time = self.get_start_time()
#        end_time = self.get_end_time()
#        loc_method = self.get_loc_method()
# 
#
#        loc = self.get_loc_data(start_time, end_time, loc_method)
#        loc_x = loc[0][:]
#        loc_y = loc[1][:]
#        loc_x = loc_x[~np.isnan(loc_x)]
#        loc_y = loc_y[~np.isnan(loc_y)]
#        h = ScatterPlot()
#        h.get_data_direct(start_time, loc_x, loc_x) 
#        h.heatmap(False)
#
#        
#        h.g.figure.savefig('h.png')
#        
#        self.img = ImageTk.PhotoImage(Image.open('h.png'))
        
        
#        self.f = Figure(figsize=(10, 7.4), dpi=100)
#        a = f.add_subplot(111)        
#        t = np.arange(-1.0, 1.0, 0.001)
#        s = t * np.sin(1 / t)
#        a.plot(t, s)
    def get_loc_data(self, start_time, end_time, loc_method):
        self.open_h5_file()
        start_time = 't'+ start_time
        end_time = 't'+ end_time
        self.table_emerge(start_time, end_time)
        num_row = self.new_table.nrows
        if num_row:
            x = self.new_table.cols._f_col('{}/x'.format(loc_method))
            y = self.new_table.cols._f_col('{}/y'.format(loc_method))
        else:
            print('there is not location data selected')
            self.show_table_info()
            
        return [x,y]
        self.close_h5_file()
            #x = table.cols.loc_seq4s.x[:]
#            y = table.cols.loc_seq4s.y[:]
#            self.x = x[~np.isnan(x)]
#            self.y = y[~np.isnan(y)]

        
    def table_emerge(self, a, b):
        self.create_new_table()
        table_list = [t.name for t in self.h5file.walk_nodes('/', 'Table')]
        if a in table_list:
            if b in table_list:
                start = table_list.index(a)
                end = table_list.index(b)

                self.do_table_emerge(start, end)
            
            else:
                print('table named {} is not existed'.format(b))
                start_b = table_list.index(a)
                temp_list_1 = sorted(table_list + [b])
                end_b = temp_list_1.index(b) - 1
                
                self.do_table_emerge(start_b, end_b)
                
        else:
            print('table named {} is not existed'.format(a))            
            if b in table_list:
                end_a = table_list.index(b)
                temp_list_2 = sorted(table_list + [a])
                start_a = temp_list_2.index(a)
                
                self.do_table_emerge(start_a, end_a)
                
            else:
                print('table named {} and {} are neither existed'.format(a, b))
                temp_list_3 = sorted(table_list + [a] + [b])
                start_ab = temp_list_3.index(a)
                end_ab = temp_list_3.index(b) - 2
                self.do_table_emerge(start_ab, end_ab)
                

        
                    
    def do_table_emerge(self, start_index, end_index): 
        if start_index > end_index:
            self.error_info_time()
            print('start time is larger than end time')
        else: 
            for i, t in enumerate(self.h5file.walk_nodes('/', 'Table')):
                if ((i >= start_index) & (i <= end_index)):
                    t.append_where(dstTable = self.new_table)
                else:
                    pass
                    
                
    def open_h5_file(self):
        self.h5file = tb.open_file('IKTS.h5', 'a')
        
    def close_h5_file(self):
        self.h5file.close()
        
    def create_new_table(self):
        if '/new_table' in self.h5file: 
            a = self.h5file.root.new_table
            a.remove()
            
        self.new_table = self.h5file.create_table('/', 'new_table', Resultnested)

        
    def show_table_info(self, event = None):
        messagebox.showinfo('show_table_info', 'there is not location data selected')
    def error_info_time(self, event = None):
        messagebox.showerror('Error', 'start time is larger than end time')
#    def error_info_0(self, event = None):
#        messagebox.showerror('Error', 'named table is not existed')
        
    def embedd_heatmap_figure(self):
        self.heatmap_canvas_frame = tk.Frame(self.heatmap_frame)
        self.heatmap_canvas_frame.pack(side=tk.TOP,fill=tk.BOTH, expand=1)
        canvas = FigureCanvasTkAgg(self.af0, master=self.heatmap_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.heatmap_toolbar_frame = tk.Frame(self.heatmap_frame)
        self.heatmap_toolbar_frame.pack(fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, self.heatmap_toolbar_frame)
        toolbar.update()    
#        self.heatmap_canvas_frame = tk.Frame(self.heatmap_frame)
#        self.heatmap_canvas_frame.pack(side=tk.TOP,fill=tk.BOTH, expand=1)
#        self.vis = tk.Label(self.heatmap_canvas_frame, image = self.img)
#        self.vis.image = self.img
#        self.vis.pack(side=tk.TOP,fill=tk.BOTH, expand=1)         

    def not_show_heatmap(self):
        self.heatmap_canvas_frame.destroy()
        self.heatmap_toolbar_frame.destroy()
############time histogram#############################################################        
        
    def is_loc_method(self):
        if self.get_loc_method()!= LOC_METHODS[0]:
            return True
        else:
            return False
        
    def setting_loc_info(self, event = None):
        messagebox.showinfo('setting loc method', 'please choose loc method')

        
    def x1_changed(self,event=None):    
        try:
            cx1 = int(self.x1.get())
        except:
            print('please enter integer number')
            self.error_info_1()
        if cx1 > 1200 or cx1 < -2000:
            self.error_info_2()
        else: return cx1
        
        
            
    def x2_changed(self,event=None):  
        try:
            cx2 = int(self.x2.get())
        except:
            print('please enter integer number')
            self.error_info_1()
        if cx2 > 1200 or cx2 < -2000:
            self.error_info_2()
        else: return cx2
        
        
    def y1_changed(self,event=None):     
        try:
            cy1 = int(self.y1.get())
        except:
            print('please enter integer number')
            self.error_info_1()
        if cy1 > 2000 or cy1 < -400:
            self.error_info_3()
        else: return cy1 
        
        
        
    def y2_changed(self,event=None):
        try:
            cy2 = int(self.y2.get())
        except:
            print('please enter integer number')
            self.error_info_1()
        if cy2 > 2000 or cy2 < -400:
            self.error_info_3()
        else: return cy2

        
    def set_bottom_loc(self):
        x1 = self.x1_changed()
        y1 = self.y1_changed()
        self.init_setting['bottom_loc'] = [x1,y1]
        print(self.init_setting['bottom_loc'])
    def get_bottom_loc(self):
        return self.init_setting['bottom_loc']
        
    def set_top_loc(self):
        x2 = self.x2_changed()
        y2 = self.y2_changed()
        self.init_setting['top_loc'] = [x2,y2]     
        print(self.init_setting['top_loc'])
    def get_top_loc(self):
        return self.init_setting['top_loc']
    
    def error_info_1(self, event = None):
        messagebox.showerror('Error', 'please enter number')
        
    def error_info_2(self, event = None):
        messagebox.showerror('Error', 'value is not in the range [-2000, 1200]')

    def error_info_3(self, event = None):
        messagebox.showerror('Error', 'value is not in the range [-400, 2000]')
        
    def location_range_selected(self):
        self.set_bottom_loc()
        self.set_top_loc()
        top_loc = self.get_top_loc()
        bottom_loc = self.get_bottom_loc()
        if top_loc[0] - bottom_loc[0] < 10:
            self.error_info_4()
        elif top_loc[1] - bottom_loc[1] < 10 :
            self.error_info_5()
            
        self.reset_hist_state()
        self.reset_timefield_state()
        self.reset_frefield_state()
    
    def error_info_4(self, event = None):
        messagebox.showerror('Error', 'x2 - x1 is less than 10')
        
    def error_info_5(self, event = None):
        messagebox.showerror('Error', 'y2 - y1 is less than 10')
        
    def get_location_range(self):
        self.get_top_loc()
        self.get_bottom_loc()
        

    
    def hist_show(self):     
        if self.hist_show_var.get():
            if self.is_location_range_selected():
                if self.is_time_interval_selected():
                    
                    self.create_hist()
            else:
                self.hist_show_var.set(False)
        else:
            self.not_show_hist()

                
    def is_location_range_selected(self):             
        top_loc_1 = self.get_top_loc()
        bottom_loc_1 = self.get_bottom_loc()
        if top_loc_1[0] != None:
            if top_loc_1[1]!= None:
                if bottom_loc_1[0]!= None:
                    if bottom_loc_1[1]!= None:
                        return True
                    else:
                        self.show_loc_range_info()
                        return False
                else:
                    self.show_loc_range_info()
                    return False
            else:
                self.show_loc_range_info()
                return False

        else:
            self.show_loc_range_info()
            return False
                    
    def show_loc_range_info(self, event = None):
        messagebox.showinfo('select location range', 'please select the location range of interest')
    def is_time_interval_selected(self):
        time_interval_1 = self.time_interval_var.get()
        if time_interval_1 != TIME_INTERVAL[0]:
            return True
        else:
            self.show_time_interval_info()
            self.hist_show_var.set(False)
            return False
            
    def create_hist(self):
        self.create_hist_figure()
        self.embedd_hist_figure()  
              
    def create_hist_figure(self):
        hist_data = self.hist_figure_data()
        self.af = Figure(figsize=(7.4, 3.6), dpi=100)
        ax = self.af.add_subplot(111)
        hist_data['count'].plot(kind='bar', title ="Histogram: count vs. time", 
               legend=False, fontsize=12, ax = ax, rot = 10)
        ax.set_xlabel("Time", fontsize = 10)
        ax.set_ylabel('Count', fontsize = 10)





    def hist_figure_data(self):
        row_index = self.get_row_index_meet_condition()
        if len(row_index) == 0:
            self.show_meet_condition_info()
            self.hist_show_var.set(False)
        else:   
            measure_time = self.get_measure_time_data()
            count = [1 if x in row_index else 0 for x in range(len(measure_time))]
            measT = [datetime.datetime.strptime(x,'%d.%m.%Y %H:%M:%S') for x in measure_time]
            time_interval_2 = self.get_time_interval()
            
            f = pd.DataFrame()
            f['time'] = measT
            f['count'] = count
            f.index = f['time']
            k = f.resample('{}'.format(time_interval_2)).sum()
            k['time'] = k.index
            
            return k

            
            
    def set_time_interval(self, event = None):
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
        self.init_setting['time_interval'] = dt
        
        self.reset_hist_state()

            
    def get_time_interval(self):
        return self.init_setting['time_interval']

    def get_measure_time_data(self):
        self.open_h5_file()
        
        if '/new_table' in self.h5file: 
            a = self.h5file.root.new_table
            num_row = a.nrows
            if num_row: 
                measT = []
                measD = a.cols.meastimeD[:]
                measH = a.cols.meastimeH[:]
                for i in range(num_row):
                    temp = measD[i].decode('UTF-8') + ' ' + measH[i].decode('UTF-8').replace('.',':')
                    measT.append(temp)
                return measT
            
            else:
                self.show_new_table_time_info()
                print('there is no data in table')
        else:
            self.show_new_table_info()
            print('there is no related data created')
        
        self.close_h5_file()
    def show_time_interval_info(self):
        messagebox.showinfo('show_time_interval_info', 'the time interval is not selected')
    def show_meet_condition_info(self):
        messagebox.showinfo('show_meet_condition_info', 'there is no event in the selected location range')
       
    def show_new_table_info(self):
        messagebox.showinfo('show_table_info', 'there is no related data created')
    def show_new_table_time_info(self):
        messagebox.showinfo('show_table_time_info', 'there is no data in table')
            
    def get_row_index_meet_condition(self):
        top_loc_2 = self.get_top_loc()
        bottom_loc_2 = self.get_bottom_loc()
        
        start_time = self.get_start_time()
        end_time = self.get_end_time()
        loc_method = self.get_loc_method()

        loc_data = self.get_loc_data(start_time, end_time, loc_method)
        x = loc_data[0][:]
        y = loc_data[1][:]
        
        return list(np.where((x >= bottom_loc_2[0]) & (x <= top_loc_2[0]) & (y >= bottom_loc_2[1]) & (y <= top_loc_2[1]))[0])
        
        
    def embedd_hist_figure(self):
        self.hist_canvas_frame = tk.Frame(self.hist_frame)
        self.hist_canvas_frame.pack(side=tk.TOP,fill=tk.BOTH, expand=1)
        canvas = FigureCanvasTkAgg(self.af, master=self.hist_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.hist_toolbar_frame = tk.Frame(self.hist_frame)
        self.hist_toolbar_frame.pack(fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, self.hist_toolbar_frame)
        toolbar.update()              
    
    def not_show_hist(self):
        self.hist_canvas_frame.destroy()
        self.hist_toolbar_frame.destroy()

##########timefield figure#######################################################        

    def set_channel(self, event = None):
        self.init_setting['channel'] = self.channel.get()
        print(self.init_setting['channel'])
        
        self.reset_timefield_state()
        self.reset_frefield_state()
        
    def get_channel(self):
        return self.init_setting['channel']
    
    def set_timefield(self, event = None):
        self.init_setting['timefield'] = self.timefield_var.get()
        print(self.timefield_var.get())
        
        self.reset_timefield_state()

            
    def get_timefield(self):
        return self.init_setting['timefield']
    
    def timefield_show(self):
        if self.timefield_show_var.get():
            if self.is_location_range_selected():
                if self.is_channel_selected():
                    if self.is_timefield_selected():
                        self.create_timefield_hist()
            else:
                self.timefield_show_var.set(False)
        else:
            self.not_show_timefield()

        
        
    def is_channel_selected(self):
        channel_1 = self.get_channel()
        if channel_1 != CH[0]:
            return True
        else:
            self.show_channel_info()
            self.timefield_show_var.set(False)
            self.frefield_show_var.set(False)
            return False

    def is_timefield_selected(self):
        timefield_1 = self.get_timefield()
        if timefield_1 != TIMEFIELD_PRAMETERS[0]:
            return True
        else: 
            self.show_timefield_info()
            self.timefield_show_var.set(False)
            return False
    def show_timefield_info(self):
        messagebox.showinfo('show_timefield_info', 'timefield parameter is not selected')
    def show_channel_info(self):
        messagebox.showinfo('show_channel_info', 'channel is not selected')

    def create_timefield_hist(self):
        self.create_timefield_hist_figure()
        self.embedd_timefield_hist_figure() 
        
    def create_timefield_hist_figure(self):
        timefield_hist_data = self.get_timefield_hist_data()
        self.af1 = Figure(figsize=(7.4, 3.6), dpi=100)
        a = self.af1.add_subplot(111)
        a.plot(timefield_hist_data)
        a.set_title('Time field figure: {}'.format(self.get_timefield()), fontsize = 12)
        a.set_xlabel('Count',fontsize = 10)
        a.set_ylabel('{}'.format(self.get_timefield()), fontsize = 10)
        
    def get_timefield_hist_data(self):
        row_index = self.get_row_index_meet_condition()
        if len(row_index) == 0:
            self.show_meet_condition_info()
            self.timefield_show_var.set(False)
        else: 
            timefield_data = self.get_timefield_data()
            k = np.asarray(timefield_data)[row_index]            
            return k
        
    def get_timefield_data(self):
        self.open_h5_file()
        
        if '/new_table' in self.h5file: 
            a = self.h5file.root.new_table
            channel = self.get_channel()
            timefield_parameter = self.get_timefield()
            num_row = a.nrows
            if num_row:
                timefield_data = a.cols._f_col('{}/timefield/{}'.format(channel, timefield_parameter))
                return timefield_data
            
            else:
                self.show_new_table_time_info()
                print('there is no data in table')
        else:
            self.show_new_table_info()
            print('there is no related data created')
        
        self.close_h5_file()
    
    def embedd_timefield_hist_figure(self):
        self.timefield_canvas_frame = tk.Frame(self.timefield_frame)
        self.timefield_canvas_frame.pack(side=tk.TOP,fill=tk.BOTH, expand=1)
        canvas = FigureCanvasTkAgg(self.af1, master=self.timefield_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.timefield_toolbar_frame = tk.Frame(self.timefield_frame)
        self.timefield_toolbar_frame.pack(fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, self.timefield_toolbar_frame)
        toolbar.update()              
    
    def not_show_timefield(self):
        self.timefield_canvas_frame.destroy()
        self.timefield_toolbar_frame.destroy()
        
##########frefield figure####################################################################

    def set_frefield(self, event = None):
        self.init_setting['frefield'] = self.frefield_var.get()
        print(self.frefield_var.get())
        
        self.reset_frefield_state()
            
            
    def get_frefield(self):
        return self.init_setting['frefield']
    
    def frefield_show(self):
        if self.frefield_show_var.get():
            if self.is_location_range_selected():
                if self.is_channel_selected():
                    if self.is_frefield_selected():
                        self.create_frefield_hist()
            else:
                self.frefield_show_var.set(False)
        else:
            self.not_show_frefield()
        
        
    def is_frefield_selected(self):
        frefield_1 = self.get_frefield()
        if frefield_1 != FREFIELD_PRAMETERS[0]:
            return True
        else: 
            self.show_frefield_info()
            self.frefield_show_var.set(False)
            return False
            
    def show_frefield_info(self):
        messagebox.showinfo('show_frefield_info', 'frefield parameter is not selected')

    def create_frefield_hist(self):
        self.create_frefield_hist_figure()
        self.embedd_frefield_hist_figure() 
        
    def create_frefield_hist_figure(self):
        frefield_hist_data = self.get_frefield_hist_data()
        self.af2 = Figure(figsize=(7.4, 3.6), dpi=100)
        a = self.af2.add_subplot(111)
        a.plot(frefield_hist_data)
        a.set_title('Freq field figure: {}'.format(self.get_frefield()), fontsize = 12)
        a.set_xlabel('Count', fontsize = 10)
        a.set_ylabel('{}'.format(self.get_frefield()), fontsize = 10)
        
    def get_frefield_hist_data(self):
        row_index = self.get_row_index_meet_condition()
        if len(row_index) == 0:
            self.show_meet_condition_info()
            self.frefield_show_var.set(False)
        else: 
            frefield_data = self.get_frefield_data()
            k = np.asarray(frefield_data)[row_index]            
            return k
        
    def get_frefield_data(self):
        self.open_h5_file()
        
        if '/new_table' in self.h5file: 
            a = self.h5file.root.new_table
            channel = self.get_channel()
            frefield_parameter = self.get_frefield()
            num_row = a.nrows
            if num_row:
                frefield_data = a.cols._f_col('{}/frefield/{}'.format(channel, frefield_parameter))
                return frefield_data
            
            else:
                self.show_new_table_time_info()
                print('there is no data in table')
        else:
            self.show_new_table_info()
            print('there is no related data created')
        
        self.close_h5_file()
    
    def embedd_frefield_hist_figure(self):
        self.frefield_canvas_frame = tk.Frame(self.frefield_frame)
        self.frefield_canvas_frame.pack(side=tk.TOP,fill=tk.BOTH, expand=1)
        canvas = FigureCanvasTkAgg(self.af2, master=self.frefield_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.frefield_toolbar_frame = tk.Frame(self.frefield_frame)
        self.frefield_toolbar_frame.pack(fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, self.frefield_toolbar_frame)
        toolbar.update()              
    
    def not_show_frefield(self):
        self.frefield_canvas_frame.destroy()
        self.frefield_toolbar_frame.destroy()
    
    
if __name__ == '__main__':       
    root = tk.Tk()
    t = graphpanel(root)

#variable = tk.StringVar(root)
#choice = [ "one", "two", "three"]
#variable.set(choice[0]) # default value
#
#def options():
#    print('the chosed value is: ', variable.get())
#
#w = ttk.OptionMenu(root, variable, *choice)
#w.pack()
#
#b = tk.Button(root, text = 'option', command = options)
#b.pack()



    tk.mainloop()
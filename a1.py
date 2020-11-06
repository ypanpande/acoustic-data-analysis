

import tkinter as tk
from tkinter import ttk, messagebox
#from Calender import Calendar
import tables as tb
#import datetime 
#import pytable_form as ptf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
#import matplotlib.pyplot as plt
import pandas as pd
from pandastable import Table

from t1 import TimeField

def main():
    path = 'D://Pywork//Pytest_1//Test files//IKTS.h5'
    root = tk.Tk()
    FirstCh(root, path, 'oda')
    root.mainloop()


class AccField(TimeField):
    def __init__(self, root, h5path, field, title = 'All', isrange = None, index = None):
        self.root = root
        self.path = h5path
        self.field = field
        self.title = title
        self.isrange = isrange
        self.index = index
        self.root.geometry('1550x1000+30+30')
        self.set_root_title()
        self.init_para()
        self.init_gui()
    def set_root_title(self):
        self.root.title('Acceleration Characters: {}'.format(self.title))
    def init_para(self):
        self.init_para_data()
        self.init_para_fig()
    def init_para_data(self):
        self.theta_var = tk.IntVar()
        self.rot_var = tk.IntVar()
        self.az0_var = tk.IntVar()
        self.ax_var = tk.IntVar()
        self.ay_var = tk.IntVar()
        self.az_var = tk.IntVar()
        
        self.timef = {'theta': self.theta_var, 'rot':self.rot_var,'az0':self.az0_var, 'ax':self.ax_var,
                      'ay':self.ay_var,'az':self.az_var}

    def init_gui_bar1(self):
        self.bar1 = ttk.LabelFrame(self.root, text = 'Set Parameters Panel', width = 1005, height = 155, relief = 'ridge', borderwidth = 1)
        self.bar1.place(x = 5, y = 5 , width = 1005, height = 145)
        
#        ttk.Label(self.bar1, text = 'Choose Channels:').place(x = 5, y = 5 , width = 100, height = 25)
#        for i, k in enumerate(self.CH.keys()):
#            ttk.Checkbutton(self.bar1, text = k, variable = self.CH[k], onvalue = 1, offvalue = 0, state = 'unchecked').place(x = 115 + 100*i, y = 5, width = 95, height = 25)
        
        bchannel = ttk.Button(self.bar1, text = 'confirm', command = self.show_figure_number)
        bchannel.place(x = 815, y = 15 , width = 60, height = 25)
        
        
        ttk.Label(self.bar1, text = 'Choose Parameters:').place(x = 5, y = 15 , width = 100, height = 25)        
        for m, n in enumerate(sorted(self.timef.keys())):
            ttk.Checkbutton(self.bar1, text = n, variable = self.timef[n], onvalue = 1, offvalue = 0,  state = 'unchecked').place(x = 115 + 100*m, y = 15, width = 95, height = 25)

        ttk.Label(self.bar1, text = 'Choose Function:').place(x = 5, y = 70 , width = 100, height = 25)        
        self.comfunc = ttk.Combobox(self.bar1, textvariable = self.cfunction, value = self.Function, width = 150, state = 'randonly')
        self.comfunc.place(x = 115, y = 70 , width = 130, height = 25)
        self.comfunc.current(0)
        self.comfunc.bind('<<ComboboxSelected>>', self.get_function)
        
        self.bshow = ttk.Button(self.bar1, text = 'Show Figures', command = self.show_figures, state = 'disabled')
        self.bshow.place(x = 260, y = 70 , width = 100, height = 25)

        ttk.Label(self.bar1, text = 'Data Table:').place(x = 470, y = 70 , width = 80, height = 25)        
        self.comtable = ttk.Combobox(self.bar1, textvariable = self.ctable, value = self.cTable, width = 150, state = 'randonly')
        self.comtable.place(x = 550, y = 70 , width = 120, height = 25)
        self.comtable.current(0)
        self.comtable.bind('<<ComboboxSelected>>', self.get_table)
        
        self.bshowT = ttk.Button(self.bar1, text = 'Show Table', command = self.show_table, state = 'disabled')
        self.bshowT.place(x = 690, y = 70 , width = 100, height = 25)


    def figure_number(self):
#        cp = self.get_chose_para(self.CH)
        pp = self.get_chose_para(self.timef)
        return {'num':len(pp), 'num_para':len(pp), 'para':pp}

    def create_figures(self):
        chose_data = self.get_chose_data()
        num = self.figure_number()['num']
        self.af = Figure(figsize=(16, 8.5), dpi=90)
        self.af.suptitle('Figures of function: {}'.format(self.cfunction.get()), fontsize = 12)
        i = 0
        for k2 in self.figure_number()['para']:
            d = chose_data[k2]
            if self.isrange:
                d = d[self.index]
                
            if num < 3:
                aa = self.af.add_subplot(1,num, i+1)
            else:
                aa = self.af.add_subplot(2,round(num/2), i+1)
            if self.cfunction.get() == self.Function[1]:
                aa.set_yscale(self.pscale.get())
                aa.plot(d, '{}{}'.format(self.pcolor.get()[0], self.plines.get()), linewidth = float(self.plinew.get()))
                aa.set_title('{}'.format(k2))
                aa.set_xlabel('count', fontsize = 10)
                aa.set_ylabel('{}'.format(k2), fontsize = 10)
                aa.grid(True)
            elif self.cfunction.get() == self.Function[2]:
                aa.hist(d, bins = self.hbins.get(), color = self.hcolor.get()[0], rwidth = float(self.hrwidth.get()))
                aa.set_title('{}'.format(k2))
                aa.set_xlabel('{} value'.format(k2), fontsize = 10)
                aa.set_ylabel('count', fontsize = 10)  
            elif self.cfunction.get() == self.Function[3]:
                aa.boxplot(d, showmeans = self.bmeans.get(), meanline = self.bmeans.get(), showfliers = self.bfliers.get())
                aa.set_title('{}'.format(k2))
#                        aa.set_xlabel('{} value'.format(k2), fontsize = 10)
                aa.set_ylabel('{} value'.format(k2), fontsize = 10) 
                        
            i += 1
            
            
    def show_table(self):
        dtawin = tk.Toplevel(self.root)
        dtawin.geometry('600x400+200+100')
        dtawin.title('Table: {}'.format(self.ctable.get()))
        f = ttk.Frame(dtawin)
        f.pack(fill=tk.BOTH,expand=1)
        chose_data = self.get_chose_data()
        
        df = pd.DataFrame()

        for k2 in self.figure_number()['para']:
            d = chose_data[k2]
            if self.isrange:
                d = d[self.index]
            df['{}'.format(k2)] = list(d)
        if self.ctable.get() == self.cTable[1]:
            pt = Table(f, dataframe=df, showtoolbar=False, showstatusbar=True)
            pt.show()
        elif self.ctable.get() == self.cTable[2]:
            dd = df.describe()
            
            dd['func'] = dd.index.tolist()
            cols = dd.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            pt = Table(f, dataframe=dd[cols], showtoolbar=False, showstatusbar=True)
            pt.show()

    def get_chose_data(self):
        try:
            with tb.open_file(self.path, mode = 'r') as h5file:
                if '/wnew_table' in h5file:
                    nt = h5file.root.wnew_table
                    if nt.nrows:
                        chose_data = {k2: nt.cols._f_col('{}/{}'.format(self.field, k2))[:] for k2 in self.get_chose_para(self.timef)}
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
         

class FirstCh(AccField):
    def set_root_title(self):
        self.root.title('First Channel Info: {}'.format(self.title))
        

    def init_para_data(self):
        self.firstch_var = tk.IntVar()
        self.firstt_var = tk.IntVar()
        
        self.timef = {'shorttime_Ch': self.firstch_var, 'shorttime_t':self.firstt_var}
        

    def get_chose_data(self):
        try:
            with tb.open_file(self.path, mode = 'r') as h5file:
                if '/wnew_table' in h5file:
                    nt = h5file.root.wnew_table
                    if nt.nrows:
                        chose_data = {k2: nt.cols._f_col('{}'.format(k2))[:] for k2 in self.get_chose_para(self.timef)}
#                        if 'shorttime_Ch' in chose_data.keys():
#                            chose_data['shorttime_Ch'] = chose_data['shorttime_Ch'][:,0]
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

if __name__ == '__main__': main()      
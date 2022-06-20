
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


def main():
    path = 'D://Pywork//Pytest_1//Test files//IKTS.h5'
    root = tk.Tk()
    TimeField(root, path, 'timefield')
    root.mainloop()


class TimeField:
    def __init__(self, root, h5path, field, title='All', isrange=False, index=None):
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
        self.root.title('Time Field Characters: {}'.format(self.title))

    def init_para(self):
        self.init_para_ch()
        self.init_para_data()
        self.init_para_fig()
# =============================================================================
#  init_para         start
# =============================================================================

    def init_para_ch(self):
        self.ch0_var = tk.IntVar()
        self.ch1_var = tk.IntVar()
        self.ch2_var = tk.IntVar()
        self.ch3_var = tk.IntVar()
        self.ch4_var = tk.IntVar()
        self.ch5_var = tk.IntVar()
#        self.chall_var = tk.IntVar()
        self.CH = {'ch0': self.ch0_var, 'ch1': self.ch1_var, 'ch2': self.ch2_var, 'ch3': self.ch3_var,
                   'ch4': self.ch4_var, 'ch5': self.ch5_var}

        self.timef = {'maxAmp_t': self.mA_var, 'time_peak': self.tp_var, 'Energy': self.en_var, 'Energy25': self.en25_var,
                      'ZeroCrossf': self.zcf_var, 'rise_time': self.rt_var, 'RA': self.ra_var}

    def init_para_fig(self):
        self.cfunction = tk.StringVar()
        self.Function = ['--choose function--', 'show value',
                         'value histogram', 'statistic boxplot']
        self.ctable = tk.StringVar()
        self.cTable = ['--choose data--', 'data table', 'statistic describe']

    def init_para_data(self):
        self.mA_var = tk.IntVar()
        self.tp_var = tk.IntVar()
        self.en_var = tk.IntVar()
        self.en25_var = tk.IntVar()
        self.zcf_var = tk.IntVar()
        self.rt_var = tk.IntVar()
        self.ra_var = tk.IntVar()
        self.pcolor = tk.StringVar()
        self.plines = tk.StringVar()
        self.plinew = tk.StringVar()
        self.pscale = tk.StringVar()
        self.color = ['blue', 'green', 'red',
                      'cyan', 'magenta', 'yellow', 'k-black']
        self.linestyle = ['-', '--', '-.', ':', 'o', 'v', '^',
                          '<', '>', '*', 's', 'p', 'h', 'H', '+', 'x', 'D', 'd']
        self.linewidth = ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4']
        self.axisscale = ['linear', 'log', 'symlog']

        self.hbins = tk.IntVar()
        self.hcolor = tk.StringVar()
        self.hrwidth = tk.StringVar()
        self.bins = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
#        self.density = [False, True]
        self.rwidth = ['1', '0.1', '0.2', '0.3',
                       '0.4', '0.5', '0.6', '0.7', '0.8', '0.9']

        self.bmeans = tk.BooleanVar()
        self.bfliers = tk.BooleanVar()
        self.means = [True, False]
        self.fliers = [True, False]

# =============================================================================
#       init_para     end
# =============================================================================
    def init_gui(self):
        self.init_gui_bar1()
        self.init_gui_bar2()
        self.init_gui_bar3()
# =============================================================================
#       init_gui  bar1
# =============================================================================

    def init_gui_bar1(self):
        self.bar1 = ttk.LabelFrame(self.root, text='Set Parameters Panel',
                                   width=1005, height=155, relief='ridge', borderwidth=1)
        self.bar1.place(x=5, y=5, width=1005, height=145)

        ttk.Label(self.bar1, text='Choose Channels:').place(
            x=5, y=5, width=100, height=25)
        for i, k in enumerate(sorted(self.CH.keys())):
            ttk.Checkbutton(self.bar1, text=k, variable=self.CH[k], onvalue=1, offvalue=0, state='unchecked').place(
                x=115 + 100*i, y=5, width=95, height=25)

        bchannel = ttk.Button(self.bar1, text='confirm',
                              command=self.show_figure_number)
        bchannel.place(x=815, y=15, width=60, height=25)

        ttk.Label(self.bar1, text='Choose Parameters:').place(
            x=5, y=40, width=100, height=25)
        for m, n in enumerate(sorted(self.timef.keys())):
            ttk.Checkbutton(self.bar1, text=n, variable=self.timef[n], onvalue=1, offvalue=0,  state='unchecked').place(
                x=115 + 100*m, y=40, width=95, height=25)

#        ttk.Separator(self.bar1, orient = "horizontal").place(x = 5, y = 70 , width = 900, height = 5)

        ttk.Label(self.bar1, text='Choose Function:').place(
            x=5, y=85, width=100, height=25)
        self.comfunc = ttk.Combobox(
            self.bar1, textvariable=self.cfunction, value=self.Function, width=150, state='randonly')
        self.comfunc.place(x=115, y=85, width=130, height=25)
        self.comfunc.current(0)
        self.comfunc.bind('<<ComboboxSelected>>', self.get_function)

        self.bshow = ttk.Button(
            self.bar1, text='Show Figures', command=self.show_figures, state='disabled')
        self.bshow.place(x=265, y=85, width=100, height=25)

        ttk.Label(self.bar1, text='Data Table:').place(
            x=470, y=85, width=80, height=25)
        self.comtable = ttk.Combobox(
            self.bar1, textvariable=self.ctable, value=self.cTable, width=150, state='randonly')
        self.comtable.place(x=550, y=85, width=120, height=25)
        self.comtable.current(0)
        self.comtable.bind('<<ComboboxSelected>>', self.get_table)

        self.bshowT = ttk.Button(
            self.bar1, text='Show Table', command=self.show_table, state='disabled')
        self.bshowT.place(x=690, y=85, width=100, height=25)
# =============================================================================
#        init_gui  bar3
# =============================================================================

    def init_gui_bar3(self):
        self.bar3 = ttk.LabelFrame(
            self.root, text='Set Plot Style', width=520, height=155, relief='ridge', borderwidth=1)
        self.bar3.place(x=1020, y=5, width=520, height=145)
        ttk.Label(self.bar3, text='Color:').place(
            x=5, y=5, width=65, height=23)
        self.cplotcolor = ttk.Combobox(
            self.bar3, textvariable=self.pcolor, value=self.color, width=100, state='randonly')
        self.cplotcolor.place(x=75, y=5, width=70, height=23)
        self.cplotcolor.current(6)
        self.cplotcolor.bind('<<ComboboxSelected>>', self.state_update)

        ttk.Label(self.bar3, text='Style:').place(
            x=5, y=35, width=65, height=23)
        self.cplotstyle = ttk.Combobox(
            self.bar3, textvariable=self.plines, value=self.linestyle, width=100, state='randonly')
        self.cplotstyle.place(x=75, y=35, width=70, height=23)
        self.cplotstyle.current(0)
        self.cplotstyle.bind('<<ComboboxSelected>>', self.state_update)

        ttk.Label(self.bar3, text='Linewidth:').place(
            x=5, y=65, width=65, height=23)
        self.cplotwidth = ttk.Combobox(
            self.bar3, textvariable=self.plinew, value=self.linewidth, width=100, state='randonly')
        self.cplotwidth.place(x=75, y=65, width=70, height=23)
        self.cplotwidth.current(1)
        self.cplotwidth.bind('<<ComboboxSelected>>', self.state_update)

        ttk.Label(self.bar3, text='Scale:').place(
            x=5, y=95, width=65, height=23)
        self.cplotscale = ttk.Combobox(
            self.bar3, textvariable=self.pscale, value=self.axisscale, width=100, state='randonly')
        self.cplotscale.place(x=75, y=95, width=70, height=23)
        self.cplotscale.current(0)
        self.cplotscale.bind('<<ComboboxSelected>>', self.state_update)

        ttk.Label(self.bar3, text='Bins:').place(
            x=160, y=5, width=55, height=23)
        self.chbins = ttk.Combobox(
            self.bar3, textvariable=self.hbins, value=self.bins, width=100, state='randonly')
        self.chbins.place(x=220, y=5, width=70, height=23)
        self.chbins.current(1)
        self.chbins.bind('<<ComboboxSelected>>', self.state_update)

        ttk.Label(self.bar3, text='Color:').place(
            x=160, y=35, width=55, height=23)
        self.chcolor = ttk.Combobox(
            self.bar3, textvariable=self.hcolor, value=self.color, width=100, state='randonly')
        self.chcolor.place(x=220, y=35, width=70, height=23)
        self.chcolor.current(0)
        self.chcolor.bind('<<ComboboxSelected>>', self.state_update)

        ttk.Label(self.bar3, text='Rwidth:').place(
            x=160, y=65, width=55, height=23)
        self.chrwidth = ttk.Combobox(
            self.bar3, textvariable=self.hrwidth, value=self.rwidth, width=100, state='randonly')
        self.chrwidth.place(x=220, y=65, width=70, height=23)
        self.chrwidth.current(0)
        self.chrwidth.bind('<<ComboboxSelected>>', self.state_update)

        ttk.Label(self.bar3, text='Showmean:').place(
            x=310, y=5, width=65, height=23)
        self.chbins = ttk.Combobox(
            self.bar3, textvariable=self.bmeans, value=self.means, width=100, state='randonly')
        self.chbins.place(x=380, y=5, width=70, height=23)
        self.chbins.current(1)
        self.chbins.bind('<<ComboboxSelected>>', self.state_update)

        ttk.Label(self.bar3, text='Showfliers:').place(
            x=310, y=35, width=65, height=23)
        self.chcolor = ttk.Combobox(
            self.bar3, textvariable=self.bfliers, value=self.fliers, width=100, state='randonly')
        self.chcolor.place(x=380, y=35, width=70, height=23)
        self.chcolor.current(0)
        self.chcolor.bind('<<ComboboxSelected>>', self.state_update)

        self.bupdate = ttk.Button(
            self.bar3, text='Update Figures', command=self.update_figures, state='disabled')
        self.bupdate.place(x=315, y=65, width=100, height=25)


# =============================================================================
#        init_gui  bar2
# =============================================================================

    def init_gui_bar2(self):
        self.bar2 = ttk.LabelFrame(
            self.root, text='Figures Panel', width=1540, height=840, relief='sunken', borderwidth=1)
        self.bar2.place(x=5, y=160, width=1540, height=830)

    def show_figure_number(self):
        n = self.figure_number()['num']
        text = 'Number of figures is: {: 4}'.format(n)
        ttk.Label(self.bar1, text=text).place(
            x=815, y=45, width=170, height=25)

    def figure_number(self):
        cp = self.get_chose_para(self.CH)
        pp = self.get_chose_para(self.timef)
        return {'num': len(cp)*len(pp), 'num_ch': len(cp), 'num_para': len(pp), 'channel': cp, 'para': pp}

    def get_chose_para(self, a):
        return [k for k, v in a.items() if v.get()]

    def get_function(self, event=None):
        if not self.figure_number()['num_para']:
            messagebox.showerror(title='para error',
                                 message='parameter is not choosed')
            self.cfunction.set('--choose function--')
            self.comfunc.current(0)
        elif not self.figure_number()['num']:
            messagebox.showerror(title='channel error',
                                 message='channel is not choosed')
            self.cfunction.set('--choose function--')
            self.comfunc.current(0)
        elif self.figure_number()['num'] > 8:
            messagebox.showerror(title='figure number error',
                                 message='figure number exceeds 8')
            self.cfunction.set('--choose function--')
            self.comfunc.current(0)
        else:
            self.bshow.config(state='!disabled')

    def show_figures(self):
        self.is_frame_free()
        self.create_figures()
        self.embed_figures()

    def create_figures(self):
        chose_data = self.get_chose_data()
        num = self.figure_number()['num']
        self.af = Figure(figsize=(16, 8.5), dpi=90)
        self.af.suptitle('Figures of function: {}'.format(
            self.cfunction.get()), fontsize=12)
        i = 0
        if self.figure_number()['num_ch'] <= self.figure_number()['num_para']:
            for k1 in self.figure_number()['channel']:
                for k2 in self.figure_number()['para']:
                    d = chose_data[k1][k2]
                    if self.isrange:
                        d = d[self.index]

                    if num < 3:
                        aa = self.af.add_subplot(1, num, i+1)
                    else:
                        aa = self.af.add_subplot(2, round(num/2), i+1)
                    if self.cfunction.get() == self.Function[1]:
                        aa.set_yscale(self.pscale.get())
                        aa.plot(d, '{}{}'.format(self.pcolor.get()[
                                0], self.plines.get()), linewidth=float(self.plinew.get()))
#                        aa.plot(d, fmt = '{}{}'.format(color = self.pcolor.get(), linestyle = self.plines.get(), linewidth = float(self.plinew.get()))
                        aa.set_title('{} -- {}'.format(k1, k2))
                        aa.set_xlabel('count', fontsize=10)
                        aa.set_ylabel('{}'.format(k2), fontsize=10)
                        aa.grid(True)
                    elif self.cfunction.get() == self.Function[2]:
                        aa.hist(d, bins=self.hbins.get(), color=self.hcolor.get(
                        ), rwidth=float(self.hrwidth.get()))
                        aa.set_title('{} -- {}'.format(k1, k2))
                        aa.set_xlabel('{} value'.format(k2), fontsize=10)
                        aa.set_ylabel('count', fontsize=10)
                    elif self.cfunction.get() == self.Function[3]:
                        aa.boxplot(d, showmeans=self.bmeans.get(
                        ), meanline=self.bmeans.get(), showfliers=self.bfliers.get())
                        aa.set_title('{} -- {}'.format(k1, k2))
#                        aa.set_xlabel('{} value'.format(k2), fontsize = 10)
                        aa.set_ylabel('{} value'.format(k2), fontsize=10)
                    i += 1
        else:
            for k2 in self.figure_number()['para']:
                for k1 in self.figure_number()['channel']:
                    d = chose_data[k1][k2]
                    if self.isrange:
                        d = d[self.index]

                    if num < 3:
                        aa = self.af.add_subplot(1, num, i+1)
                    else:
                        aa = self.af.add_subplot(2, round(num/2), i+1)
                    if self.cfunction.get() == self.Function[1]:
                        aa.set_yscale(self.pscale.get())
                        aa.plot(d, '{}{}'.format(self.pcolor.get()[
                                0], self.plines.get()), linewidth=float(self.plinew.get()))
#                        aa.plot(d, color = self.pcolor.get(), linestyle = self.plines.get(), linewidth = float(self.plinew.get()))
                        aa.set_title('{} -- {}'.format(k1, k2))
                        aa.set_xlabel('count', fontsize=10)
                        aa.set_ylabel('{}'.format(k2), fontsize=10)
                        aa.grid(True)
                    elif self.cfunction.get() == self.Function[2]:
                        aa.hist(d, bins=self.hbins.get(), color=self.hcolor.get(
                        ), rwidth=float(self.hrwidth.get()))
                        aa.set_title('{} -- {}'.format(k1, k2))
                        aa.set_xlabel('{} value'.format(k2), fontsize=10)
                        aa.set_ylabel('count', fontsize=10)
                    elif self.cfunction.get() == self.Function[3]:
                        aa.boxplot(d, showmeans=self.bmeans.get(
                        ), meanline=self.bmeans.get(), showfliers=self.bfliers.get())
                        aa.set_title('{} -- {}'.format(k1, k2))
#                        aa.set_xlabel('{} value'.format(k2), fontsize = 10)
                        aa.set_ylabel('{} value'.format(k2), fontsize=10)

                    i += 1

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

    def get_chose_data(self):
        try:
            with tb.open_file(self.path, mode='r') as h5file:
                if '/wnew_table' in h5file:
                    nt = h5file.root.wnew_table
                    if nt.nrows:
                        chose_data = {k1: {k2: nt.cols._f_col('{}/{}/{}'.format(k1, self.field, k2))[
                            :] for k2 in self.get_chose_para(self.timef)} for k1 in self.get_chose_para(self.CH)}
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

    def is_frame_free(self):
        try:
            self.canvas_frame.destroy()
            self.toolbar_frame.destroy()
        except:
            pass

    def state_update(self, event=None):
        self.bupdate.config(state='!disabled')

    def update_figures(self):
        self.show_figures()

    def get_table(self, event=None):
        if not self.figure_number()['num_para']:
            messagebox.showerror(title='para error',
                                 message='parameter is not choosed')
            self.ctable.set('--choose data--')
            self.comtable.current(0)
        elif not self.figure_number()['num']:
            messagebox.showerror(title='channel error',
                                 message='channel is not choosed')
            self.ctable.set('--choose data--')
            self.comtable.current(0)
        else:
            self.bshowT.config(state='!disabled')

    def show_table(self):
        dtawin = tk.Toplevel(self.root)
        dtawin.geometry('600x400+200+100')
        dtawin.title('Table: {}'.format(self.ctable.get()))
        f = ttk.Frame(dtawin)
        f.pack(fill=tk.BOTH, expand=1)
        chose_data = self.get_chose_data()

        df = pd.DataFrame()

        for k1 in self.figure_number()['channel']:
            for k2 in self.figure_number()['para']:
                d = chose_data[k1][k2]
                if self.isrange:
                    d = d[self.index]
                df['{}-{}'.format(k1, k2)] = list(d)
        if self.ctable.get() == self.cTable[1]:
            pt = Table(f, dataframe=df, showtoolbar=False, showstatusbar=True)
            pt.show()
        elif self.ctable.get() == self.cTable[2]:
            dd = df.describe()

            dd['func'] = dd.index.tolist()
            cols = dd.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            pt = Table(f, dataframe=dd[cols],
                       showtoolbar=False, showstatusbar=True)
            pt.show()


class FreField(TimeField):
    def set_root_title(self):
        self.root.title('Frequency Field Characters: {}'.format(self.title))

    def init_para_data(self):
        self.mA_var = tk.IntVar()
        self.fp_var = tk.IntVar()
        self.fc_var = tk.IntVar()
        self.fw_var = tk.IntVar()
        self.pow_var = tk.IntVar()

        self.timef = {'maxAmp_f': self.mA_var, 'fre_peak': self.fp_var, 'fre_centroid': self.fc_var, 'fre_wpeak': self.fw_var,
                      'Power': self.pow_var}


if __name__ == '__main__':
    main()

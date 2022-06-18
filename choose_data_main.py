

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from Calender import Calendar
import tables as tb
import datetime
import pytable_form as ptf
from time_field_character import TimeField, FreField
from accelaration_character import AccField, FirstCh
from location_frame import LocAll
from frequency_field_character import LocField


def main():
    root = tk.Tk()
    FirstWin(root)
    root.mainloop()


class FirstWin:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x500+30+30")
        self.root.title('first window')
        self.default_source_file = 'D://resultfolder'
        self.tttlist = ['table name list']
        self.dayVar = tk.IntVar()
        self.beginDay = {}
        self.endDay = {}
        self.init_gui()

    def init_gui(self):
        menubar = tk.Menu(self.root)
        locmenu = tk.Menu(menubar, tearoff=0)
        locmenu.add_command(label='Sequential6s',
                            command=self.loc_sequential6s)
        locmenu.add_command(label='Geiger6s', command=self.loc_geiger6s)
        locmenu.add_separator()
        locmenu.add_command(label='Sequential4s',
                            command=self.loc_sequential4s)
        locmenu.add_command(label='Geiger4s', command=self.loc_geiger4s)
        locmenu.add_separator()
        locmenu.add_command(label='All Methods', command=self.loc_all_methods)
        menubar.add_cascade(label='Location', menu=locmenu)
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
        charmenu = tk.Menu(menubar, tearoff=0)
        charmenu.add_command(label='Time Field', command=self.time_field)
        charmenu.add_command(label='Freq Field', command=self.freq_field)
        menubar.add_cascade(label='Character', menu=charmenu)

        bsource = ttk.Button(self.root, text="h5 file",
                             command=self.choose_h5_file)
        bsource.place(x=100, y=100, width=90, height=30)

        self.lsource = ttk.Label(
            self.root, text=self.default_source_file, background="white")
        self.lsource.place(x=200, y=100, width=300, height=30)
        ttk.Label(self.root, text="date number:").place(
            x=100, y=220,  width=120, height=30)
        ttk.Radiobutton(self.root, text='one day', variable=self.dayVar, value=1,
                        command=self.choose_date).place(x=230, y=220,  width=100, height=30)
        ttk.Radiobutton(self.root, text='more days', variable=self.dayVar, value=2,
                        command=self.choose_date).place(x=340, y=220,  width=100, height=30)

        binfo = ttk.Button(self.root, text="h5 info",
                           command=self.h5_info_date)
        binfo.place(x=100, y=140, width=90, height=30)

        self.calchoose1 = ttk.Button(
            self.root, text='choose begin date', command=self.choose_first_date, state='disabled')
        self.calchoose1.place(x=100, y=260, width=120, height=30)
        self.calget1 = ttk.Button(
            self.root, text='show', command=self.get_first_date, state='disabled')
        self.calget1.place(x=230, y=260, width=50, height=30)

        self.cal1 = ttk.Label(self.root, text='year-month-day',
                              background="white", state='disabled')
        self.cal1.place(x=290, y=260, width=100, height=30)

        self.calchoose2 = ttk.Button(
            self.root, text='choose end date', command=self.choose_end_date, state='disabled')
        self.calchoose2.place(x=100, y=300, width=120, height=30)
        self.calget2 = ttk.Button(
            self.root, text='show', command=self.get_end_date, state='disabled')
        self.calget2.place(x=230, y=300, width=50, height=30)

        self.bdata = ttk.Button(
            self.root, text='get data', command=self.get_data, state='disabled')
        self.bdata.place(x=100, y=360, width=120, height=30)
        self.combo_list = ttk.Combobox(
            self.root, value=self.tttlist, width=100, state='disabled')
        self.combo_list.place(x=240, y=360, width=120, height=30)
        self.combo_list.current(0)
# =============================================================================
# first window functions
# =============================================================================

    def choose_h5_file(self):
        self.default_source_file = filedialog.askopenfilename(parent=self.root,
                                                              initialdir=self.default_source_file,
                                                              title='Select h5 file', filetypes=(('h5 file', '*.h5'), ('all files', '*.*')))
        self.lsource.config(text=self.default_source_file)

    def h5_info_date(self):
        h5infowin = tk.Toplevel(self.root)
        h5infowin.geometry('250x250+30+30')
        h5infowin.title('h5 file tables info')

        h5info = scrolledtext.ScrolledText(
            master=h5infowin, wrap=tk.WORD, font=("Helvetica", 10), state='disabled')
        h5info.pack()

        h5info.config(state='normal')
        h5info.delete(1.0, 'end')
        try:
            with tb.open_file(self.default_source_file, 'r') as h5file:
                for k, v in enumerate(h5file.walk_nodes('/', 'Table')):
                    h5info.insert('{}.0'.format(k+1), 'Name:  ' +
                                  v.name+'        '+'Rows:  ' + str(v.nrows) + '\n')
        except IOError:
            print('open h5 file error')
            messagebox.showerror(title='h5 file', message='open h5 file error')

        h5info.config(state='disabled')

    def get_table_list(self):
        self.table_list = []
        try:
            with tb.open_file(self.default_source_file, 'r') as h5file:
                for k, v in enumerate(h5file.walk_nodes('/', 'Table')):
                    self.table_list.append(v.name)
        except IOError:
            print('open h5 file error')
            messagebox.showerror(title='h5 file', message='open h5 file error')

    def choose_date(self):
        if self.dayVar.get() == 1:
            self.calchoose1.state(['!disabled'])
            self.calget1.state(['!disabled'])
            self.cal1.state(['!disabled'])
            self.calchoose2.state(['disabled'])
            self.calget2.state(['disabled'])
            self.cal2.state(['disabled'])
            self.calchoose1.state(['!disabled'])
            self.calget1.state(['!disabled'])
            self.cal1.state(['!disabled'])
            self.calchoose2.state(['!disabled'])
            self.calget2.state(['!disabled'])
            self.cal2.state(['!disabled'])
            self.bdata.state(['!disabled'])
            self.combo_list.state(['!disabled'])

    def choose_end_date(self):
        self.bdata.state(['disabled'])
        self.combo_list.state(['disabled'])

        datewin = tk.Toplevel(self.root)
        datewin.title('choose the end date')
        Calendar(datewin, self.endDay)

    def get_first_date(self):
        self.first_date = '{}-{:02}-{:02}'.format(
            self.beginDay['year_selected'], self.beginDay['month_selected'], self.beginDay['day_selected'])
        self.cal1.config(text=self.first_date)
        self.get_table_list()
        if self.dayVar.get() == 1:
            self.bdata.state(['!disabled'])
            self.combo_list.state(['!disabled'])

    def table_index(self, tt, r=1):
        if tt in self.table_list:
            tt_idx = self.table_list.index(tt)
        else:
            if r:
                tt_idx = sorted(self.table_list + [tt]).index(tt)
            else:
                tt_idx = sorted(self.table_list + [tt]).index(tt) - 1

        return tt_idx

    def get_emerge_table(self, a, b):
        with tb.open_file(self.default_source_file, 'a') as ff:
            if '/wnew_table' in ff:
                aa = ff.root.wnew_table
                aa.remove()

        elif self.dayVar.get() == 2:
            t1 = 't{}{:02}{:02}'.format(
                self.beginDay['year_selected'], self.beginDay['month_selected'], self.beginDay['day_selected'])
            t2 = 't{}{:02}{:02}'.format(
                self.endDay['year_selected'], self.endDay['month_selected'], self.endDay['day_selected'])
            t1_idx = self.table_index(t1)
            t2_idx = self.table_index(t2, 0)
            if t1_idx >= (len(self.table_list) - 1):
                print('Selected date is out of date range in the data file')
                messagebox.showerror(
                    title='data info', message='Selected date is out of date range in the data file')


# =============================================================================
# menu functions
# =============================================================================


    def loc_geiger6s(self):
        lg6 = tk.Toplevel(self.root)
        date = '{}-{:02}-{:02}'.format(self.beginDay['year_selected'],
                                       self.beginDay['month_selected'], self.beginDay['day_selected'])
        LocField(lg6, self.default_source_file, 'loc_geiger6s', date)

    def loc_sequential6s(self):
        ls6 = tk.Toplevel(self.root)
        date = '{}-{:02}-{:02}'.format(self.beginDay['year_selected'],
                                       self.beginDay['month_selected'], self.beginDay['day_selected'])
        LocField(ls6, self.default_source_file, 'loc_seq6s', date)

    def loc_geiger4s(self):
        lg4 = tk.Toplevel(self.root)
        date = '{}-{:02}-{:02}'.format(self.beginDay['year_selected'],
                                       self.beginDay['month_selected'], self.beginDay['day_selected'])
        LocField(lg4, self.default_source_file, 'loc_geiger4s', date)

    def loc_sequential4s(self):
        ls4 = tk.Toplevel(self.root)
        date = '{}-{:02}-{:02}'.format(self.beginDay['year_selected'],
                                       self.beginDay['month_selected'], self.beginDay['day_selected'])
        LocField(ls4, self.default_source_file, 'loc_seq4s', date)

    def loc_all_methods(self):
        lam = tk.Toplevel(self.root)
        date = '{}-{:02}-{:02}'.format(self.beginDay['year_selected'],
                                       self.beginDay['month_selected'], self.beginDay['day_selected'])
        LocAll(lam, self.default_source_file, date)

    def acceleration(self):
        af = tk.Toplevel(self.root)
        AccField(af, self.default_source_file, 'oda')

    def firstchannel(self):
        cf = tk.Toplevel(self.root)
        FirstCh(cf, self.default_source_file, 'oda')

    def help_box(self):
        pass

    def about(self):
        pass


if __name__ == '__main__':
    main()

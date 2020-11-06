

import tkinter as tk
from tkinter import ttk

import calendar
import datetime
#import sys

 
class Calendar:
    def __init__(self, parent, values = {}):
        self.values = values
        self.parent = parent
        self.cal = calendar.TextCalendar(calendar.SUNDAY)
        self.year = datetime.date.today().year
        self.month = datetime.date.today().month
        day = datetime.date.today().day
        self.wid = []
        self.day_selected = day
        self.month_selected = self.month
        self.year_selected = self.year
        self.day_name = ''
         
        self.setup(self.year, self.month)
         
    def clear(self):
        for w in self.wid[:]:
            w.grid_forget()
            #w.destroy()
            self.wid.remove(w)
     
    def go_prev(self):
        if self.month > 1:
            self.month -= 1
        else:
            self.month = 12
            self.year -= 1
        #self.selected = (self.month, self.year)
        self.clear()
        self.setup(self.year, self.month)
 
    def go_next(self):
        if self.month < 12:
            self.month += 1
        else:
            self.month = 1
            self.year += 1
         
        #self.selected = (self.month, self.year)
        self.clear()
        self.setup(self.year, self.month)
         
    def selection(self, day, name):
        self.day_selected = day
        self.month_selected = self.month
        self.year_selected = self.year
        self.day_name = name
         
        #data
        self.values['day_selected'] = day
        self.values['month_selected'] = self.month
        self.values['year_selected'] = self.year
        self.values['day_name'] = name
        self.values['month_name'] = calendar.month_name[self.month_selected]
         
        self.clear()
        self.setup(self.year, self.month)
         
    def setup(self, y, m):
        left = ttk.Button(self.parent, text='<', width=5, command=self.go_prev)
        self.wid.append(left)
        left.grid(row=0, column=1)
         
        header = ttk.Label(self.parent,  text='{}   {}'.format(calendar.month_abbr[m], str(y)), width=15)
        self.wid.append(header)
        header.grid(row=0, column=2, columnspan=3)
         
        right = ttk.Button(self.parent, text='>', width=5, command=self.go_next)
        self.wid.append(right)
        right.grid(row=0, column=5)
         
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        for num, name in enumerate(days):
            t = ttk.Label(self.parent, width=5, text=name[:3])
            self.wid.append(t)
            t.grid(row=1, column=num)
         
        for w, week in enumerate(self.cal.monthdayscalendar(y, m), 2):
            for d, day in enumerate(week):
                if day:
                    #print(calendar.day_name[day])
                    b = ttk.Button(self.parent, width=5, text=day, command=lambda day=day:self.selection(day, calendar.day_name[(day-1) % 7]))
                    self.wid.append(b)
                    b.grid(row=w, column=d)
                     
        sel = ttk.Label(self.parent, text='{} {} {} {}'.format(
            self.day_name, calendar.month_name[self.month_selected], self.day_selected, self.year_selected))
        self.wid.append(sel)
        sel.grid(row=8, column=0, columnspan=7)
         
        ok = ttk.Button(self.parent, width=5, text='OK', command=self.kill_and_save)
        self.wid.append(ok)
        ok.grid(row=9, column=2, columnspan=3, pady=10)
         
    def kill_and_save(self):
        self.parent.destroy()
 
 
if __name__ == '__main__':
 
    class Control:
        def __init__(self, parent):
            self.parent = parent
            self.choose_btn = tk.Button(self.parent, text='Choose',command=self.popup)
            self.show_btn = tk.Button(self.parent, text='Show Selected',command=self.print_selected_date)
            self.choose_btn.grid()
            self.show_btn.grid()
            self.data = {}
             
        def popup(self):
            child = tk.Toplevel()
            cal = Calendar(child, self.data)
             
        def print_selected_date(self):
            print(self.data)    
 
    root = tk.Tk()
    app = Control(root)
    root.mainloop()
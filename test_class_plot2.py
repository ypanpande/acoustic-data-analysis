

import matplotlib.pyplot as plt
#from matplotlib.figure import Figure

import numpy as np
import pandas as pd
import seaborn as sns
#import os
import tkinter as tk
from tkinter import filedialog

class ScatterPlot:
    def __init__(self, filename, x, y, z = [0], ca = None, areatop = [-2000,2000], areabottom = [1200,-400], block = 100):
        self.sx2=[-1650,5,505,550,0,-1650,-1650]
        self.sy2=[1552.5,1555,1482.5,82.5,0,-2.5,1552.5]
        
        self.rx2 = [-1410,5,890,900,0,-1410,-1410]
        self.ry2 = [1312.5,1305,1282.5,252.5,240,247.5,1312.5]
        
        self.filename = filename
        self.locx = x
        self.locy = y
        if not z[0]:
            self.z = [0]*len(x)
        else:
            self.z = z
        self.ca = ca
        
        self.areatop = areatop
        self.areabottom = areabottom
        self.block = block
        
    def showfigure(self):
        plt.figure()
        plt.title('Location of event {}'.format(self.filename))
        plt.xlabel('Horizontal (mm)')
        plt.ylabel('Vertical (mm)')
        plt.grid(True)
        plt.xlim(-2000, 1200)
        plt.ylim(-400, 2000)
                
    def get_data(self):
        root = tk.Tk()
        root.withdraw()
        self.filename = filedialog.askopenfilename()
        self.data = pd.read_excel(self.filename)
        self.locx = self.data['x0 (mm)']
        self.locy = self.data['y0 (mm)']

        return len(self.locx)
    def plotdata(self):
        plt.scatter(self.locx, self.locy,color='b', marker='o', alpha=.4)
    
    def plotsensor(self):
        plt.plot(self.sx2, self.sy2, color='g',linestyle = '--')
        
    def plotfield(self):
        plt.plot(self.rx2, self.ry2, color='r',linestyle = ':')
        


    def scatter_plot(self):
        self.showfigure()
        self.plotsensor()
        self.plotfield()
        self.plotdata()
        
        
    def blockcount(self):
        hornum = int(np.round((self.areabottom[0] - self.areatop[0])/self.block))
        vernum = int(np.round((self.areatop[1] - self.areabottom[1])/self.block))
        self.mapcoordx = np.arange(self.areatop[0],self.areabottom[0]+self.block,self.block)
        self.mapcoordy = np.arange(self.areatop[1],self.areabottom[1]-self.block,-self.block)
        
        self.count = np.zeros((hornum,vernum))
        for mapx in range(hornum):
            for mapy in range(vernum):
                x = [self.mapcoordx[mapx], self.mapcoordx[mapx+1]]
                y = [self.mapcoordy[mapy+1], self.mapcoordy[mapy]]
                for dataloop in range(self.length_data()):
                    if x[0] <= self.locx[dataloop] < x[1]:
                        if y[0] <= self.locy[dataloop] < y[1]:
                            self.count[mapx][mapy] +=1
        
        return self.count.T
    
    def blockcount2(self):
        hornum = int(np.round((self.areabottom[0] - self.areatop[0])/self.block))
        vernum = int(np.round((self.areatop[1] - self.areabottom[1])/self.block))
        self.mapcoordx = np.arange(self.areatop[0],self.areabottom[0]+self.block,self.block)
        self.mapcoordy = np.arange(self.areatop[1],self.areabottom[1]-self.block,-self.block)
        
        self.count = np.zeros((hornum,vernum))
        zsum = np.zeros((hornum,vernum))
        for mapx in range(hornum):
            for mapy in range(vernum):
                x = [self.mapcoordx[mapx], self.mapcoordx[mapx+1]]
                y = [self.mapcoordy[mapy+1], self.mapcoordy[mapy]]
                for dataloop in range(self.length_data()):
                    if x[0] <= self.locx[dataloop] < x[1]:
                        if y[0] <= self.locy[dataloop] < y[1]:
                            self.count[mapx][mapy] +=1
                            zsum[mapx][mapy] += self.z[dataloop]
        if self.ca == 'az':
            zmean = np.around(np.divide(zsum, self.count),2)
        else:
            zmean = np.around(np.divide(zsum, self.count))
        zmean[np.isnan(zmean)] = 0  
            
        return {'count':self.count.T, 'sum': zsum.T, 'mean': zmean.T}
    def get_xticklabels(self):
        return np.array(self.mapcoordx[:-1])+int(self.block/2)
    def get_yticklabels(self):
        return np.array(self.mapcoordy[:-1])-int(self.block/2)
    def get_mask(self):
        masktemp = self.blockcount().copy()
        masktemp[masktemp >=1] = 2
        masktemp[masktemp ==0] = 1
        masktemp[masktemp ==2] = 0
        
        return masktemp
#    def figure_plot(self, self.blockcount(),ax = None, self.get_xticklabels, self.get_yticklabels, self.get_mask):
#        
#        g = sns.heatmap(self.count.T, vmin = 1, vmax = 100, annot = True, fmt = 'g', ax = ax, xticklabels = my_xticklabels, yticklabels = my_yticklabels, cmap = "jet", mask = masktemp)        

    def figure_set(self, g):
        g.set_xlabel('Horizontal (mm)')   
        g.set_ylabel('Vertical (mm)') 
        g.set_title('Heatmap of event {}'.format(self.filename))
        agx = [3.6, 20.2, 25,25.5,20.2,3.8,3.6]
        agy = [4.5, 4.5, 5.1,19.1,20,20,4.5]
        arx = [6, 29, 29 ,6,6]
        ary = [7, 7, 17.9, 17.9,7]
        g.plot(agx,agy,color='g',linestyle = '--')
        g.plot(arx,ary, color='r',linestyle = ':')

    def plot_heatmap(self, f,ax, method = 'Loc', vmin = 0, vmax = 100, cmap = 'jet', 
                     linewidths = 0, sensor = True, cha = 'loc', aspect = 'count'):
        
#        self.length_data()
#        plt.figure()
        
#        ax = f.add_subplot(111)
        a = self.blockcount2()        
        
        my_xticklabels = self.get_xticklabels()
        my_yticklabels = self.get_yticklabels()
        masktemp = self.get_mask()
        #sns.palplot(sns.color_palette("jet", n_colors=256))  
#        my_xticklabels = np.array(self.mapcoordx[:-1])+int(self.block/2)
#        my_yticklabels = np.array(self.mapcoordy[:-1])-int(self.block/2)
#        masktemp = self.count.T.copy()
#        masktemp[masktemp >=1] = 2
#        masktemp[masktemp ==0] = 1
#        masktemp[masktemp ==2] = 0
                    
        self.g = sns.heatmap(a[aspect], vmin = vmin, vmax = vmax, annot = True, fmt = 'g', annot_kws={"size":8},
                             ax = ax, xticklabels = my_xticklabels, yticklabels = my_yticklabels,
                             cmap = cmap, mask = masktemp, linewidths = linewidths)        
        #g.invert_yaxis()
        self.g.set_xlabel('Horizontal (mm)')   
        self.g.set_ylabel('Vertical (mm)') 
        self.g.set_title('Heatmap of {} on {}-{}:{}'.format(method, self.filename, cha, aspect))
        if sensor:
            agx = [3.6, 20.2, 25,25.5,20.2,3.8,3.6]
            agy = [4.5, 4.5, 5.1,19.1,20,20,4.5]
            arx = [6, 29, 29 ,6,6]
            ary = [7, 7, 17.9, 17.9,7]
            self.g.plot(agx,agy,color='g',linestyle = '--')
            self.g.plot(arx,ary, color='r',linestyle = ':')
            self.g.text(2.9, 3.8, 'CH:4', fontsize = 8, bbox = dict(facecolor = 'red', alpha = 0.2))
            self.g.text(19.5, 3.8, 'CH:0', fontsize = 8, bbox = dict(facecolor = 'red', alpha = 0.2))
            self.g.text(24.3, 4, 'CH:2', fontsize = 8, bbox = dict(facecolor = 'red', alpha = 0.2))
            self.g.text(24.8, 20, 'CH:3', fontsize = 8, bbox = dict(facecolor = 'red', alpha = 0.2))
            self.g.text(19.5, 21, 'CH:1', fontsize = 8, bbox = dict(facecolor = 'red', alpha = 0.2))
            self.g.text(3.1, 21, 'CH:5', fontsize = 8, bbox = dict(facecolor = 'red', alpha = 0.2))
        ax.grid(True) 
        plt.close(f)
#        if not show:
#            plt.close(a)
            
if __name__ == '__main__':
    filename = 'nnnew_Seq4s_loc_20180814.xls'
    data = pd.read_excel(filename)
    locx = list(data['x0 (mm)'])
    locy = list(data['y0 (mm)'])
    print(type(locx))
    f, ax = plt.subplots(figsize = (7.4, 3.8), dpi = 100)
    p = ScatterPlot(filename, locx, locy)
#    p.get_data()
#    p.showfigure()
#    p.plotsensor()
#    p.plotfield()
#    p.plotdata()
#    p.length_data()
#    p.blockcount()
    p.scatter_plot()
    p.plot_heatmap(f, ax)
    
    
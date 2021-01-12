
import tables as tb

class CH_s(tb.IsDescription):
    _v_pos = 2
#    class picktimes(tb.IsDescription):  
    class timefield(tb.IsDescription):
        pickt = tb.FloatCol(pos = 0)
        maxAmp_t = tb.FloatCol(pos = 1)
        time_peak = tb.FloatCol(pos = 2)
        Energy = tb.FloatCol(pos = 3)
        Energy25 = tb.FloatCol(pos = 4)
        ZeroCrossf = tb.FloatCol(pos = 5)
        rise_time = tb.FloatCol(pos = 6)
        RA = tb.FloatCol(pos = 7)
    
    class frefield(tb.IsDescription):
        maxAmp_f = tb.FloatCol(pos = 0)
        fre_peak = tb.FloatCol(pos = 1)
        fre_centroid = tb.FloatCol(pos = 2)
        fre_wpeak = tb.FloatCol(pos = 3)
        Power = tb.FloatCol(pos = 4)
        PartialPower = tb.FloatCol(shape = (5),pos = 5)        
    
class loc_s(tb.IsDescription):
    _v_pos = 1
    x = tb.FloatCol(pos = 0)
    y = tb.FloatCol(pos = 1)
    t0 = tb.FloatCol(pos = 2)
    res = tb.FloatCol(pos = 3)
    aver_res = tb.FloatCol(pos = 4)
    
class acc_info(tb.IsDescription):
    _v_pos = 3
    theta = tb.FloatCol(pos = 0)
    rot = tb.FloatCol(pos = 1)
    time = tb.StringCol(32,pos = 2)
    az0 = tb.FloatCol(pos = 3)
    ax = tb.FloatCol(pos = 4)
    ay = tb.FloatCol(pos = 5)
    az = tb.FloatCol(pos = 6)
    
class Resultnested(tb.IsDescription):
    foldername = tb.StringCol(32, pos = 0)
    filename = tb.StringCol(32, pos = 1)
    meastimeD = tb.StringCol(32, pos = 2)
    meastimeH = tb.StringCol(32, pos = 3)
    meastimeT = tb.StringCol(32, pos = 4)
    picktimearray = tb.FloatCol(shape = (6), pos = 5)
    shorttime_Ch = tb.UInt16Col(pos = 6)
    shorttime_t = tb.FloatCol(pos = 7)
    loc_seq6s = loc_s()
    loc_geiger6s = loc_s()
    loc_seq4s = loc_s()
    loc_geiger4s = loc_s()
    ch0 = CH_s()
    ch1 = CH_s()
    ch2 = CH_s()
    ch3 = CH_s()
    ch4 = CH_s()
    ch5 = CH_s() 
    oda = acc_info()        
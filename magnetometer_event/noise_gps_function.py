import numpy as np
import matplotlib.pyplot as plt
import sys, time
sys.path.insert(0, "..")
from tqdm import tqdm
from extra.progressbar import progress_bar
from data_reader_NMEA.NMEA_data_reader import ReadNMEAData
from extra.error_calculation_NMA_standard import accuracy_NMEA_opt, filtering_outliers

def create_date(begin, end):
    date = []
    for i in range(begin,end+1):
        if len(str(i))==1:
            date.append("00"+str(i))
        elif len(str(i))==2:
            date.append("0"+str(i))
        else:
            date.append(str(i))
    return date


def run_filter_NMEA_data(nr_days, receiver):
    noise = np.zeros((nr_days,4))
    pieces_per_interval = 3
    noise_3_9 = np.zeros((nr_days,pieces_per_interval))*np.nan
    noise_21_3 = np.zeros((nr_days,pieces_per_interval))*np.nan
    counter_first = [1,1]
    year = "2018"
    date = create_date(1,nr_days)
    for i in tqdm(range(len(date)),desc= "RTIM data"):
        adress = "/run/media/michaelsb/HDD Linux/data/NMEA/"+year+"/"+date[i]+"/"+\
        "NMEA_M"+receiver +"_"+date[i]+"0.log"
        obj = ReadNMEAData()
        try:
            obj.read_textfile(adress,verbose=False)
            N,E,Z = obj.coordinates
            home_computer = 1
        except FileNotFoundError:
            try:
                adress = "/scratch/michaesb/data/NMEA/"+year+"/"+date[i]+"/NMEA_M"+ \
                receiver+"_"+date[i]+"0.log"
                obj = ReadNMEAData()
                obj.read_textfile(adress,verbose=False)
                N,E,Z = obj.coordinates
                Office_computer = 1
            except FileNotFoundError:
                tqdm.write("no "+receiver+" file here at day: " + str(i) +" year: "+year)
                tqdm.write(adress)
                noise[i,:] = np.nan
                continue

        if len(Z) < 60:
            noise[i,:] = np.nan
            continue

        sigma = accuracy_NMEA_opt(Z-np.mean(Z))
        index_3, index_9, index_15 ,index_21 = \
        int(len(sigma)/8.),int(len(sigma)*3/8.),int(len(sigma)*5/8.),int(len(sigma)*7/8.)
        if counter_first[0]==1:
            noise[i,0] = np.nan
            counter_first[0] = 0
        else:
            noise[i,0]=np.nanmedian(np.concatenate([noise_stored,sigma[:index_3],]))
        noise[i,1] = np.nanmedian(sigma[index_3:index_9])
        noise[i,2] = np.nanmedian(sigma[index_9:index_15])
        noise[i,3] = np.nanmedian(sigma[index_15:index_21])

        if counter_first[1]==1:
            counter_first[1]=0
            noise_stored = sigma[index_21:]
            continue
        for k in range(pieces_per_interval):
            index_k_21,index_k1_3 = int(-len(sigma)*(1- (21+k*2)/24.)), \
                                    int(-len(sigma)*(1- (21+(k+1)*2)/24.)),
            index_k2_3, index_k_9 = int(+len(sigma)*(3+k*2)/24.), \
                                    int(+len(sigma)*(3+(k+1)*2)/24.)
            if k<pieces_per_interval/2:
                noise_21_3[i, k] = np.nanmedian(noise_stored[\
                int(len(noise_stored)*2*k/3):int(len(noise_stored)*2*(k+1)/3)])

            elif k==pieces_per_interval/2 and pieces_per_interval==3:
                noise_21_3[i,k]=np.nanmedian(np.concatenate(\
                [noise_stored[int(len(noise_stored)*2*k/3):],sigma[:index_k1_3]]))
            else:
                noise_21_3[i,k] = np.nanmedian(sigma[index_k_21:index_k1_3])
            noise_3_9[i,k] = np.nanmedian(sigma[index_k2_3:index_k_9])
            # tqdm.write(str(2*k/3)+ ", 2*k/3")
            # tqdm.write(str(noise_21_3[i,:])+"21_3")
            # tqdm.write(str(noise_3_9[i,:])+"3_9")
        noise_stored = sigma[index_21:]
    return date,noise, noise_21_3, noise_3_9



def run_NMEA_data(nr_days, receiver):
        nr_datapoints = 50500
        noise = np.zeros((nr_days,nr_datapoints))*np.nan
        time_axis = np.zeros((nr_days,nr_datapoints))*np.nan
        year = "2018"
        date = create_date(1,nr_days)
        for i in tqdm(range(len(date)),desc= "RTIM data"):
            adress = "/run/media/michaelsb/HDD Linux/data/NMEA/"+year+"/"+date[i]+"/"+\
            "NMEA_M"+receiver +"_"+date[i]+"0.log"
            obj = ReadNMEAData()
            try:
                obj.read_textfile(adress,verbose=False)
                N,E,Z = obj.coordinates
                home_computer = 1
            except FileNotFoundError:
                try:
                    adress = "/scratch/michaesb/data/NMEA/"+year+"/"+date[i]+"/NMEA_M"+ \
                    receiver+"_"+date[i]+"0.log"
                    obj = ReadNMEAData()
                    obj.read_textfile(adress,verbose=False)
                    N,E,Z = obj.coordinates
                    Office_computer = 1
                except FileNotFoundError:
                    tqdm.write("no "+receiver+" file here at day: " + str(i) +" year: "+year)
                    tqdm.write(adress)
                    noise[i,:] = np.nan
                    continue
            if len(Z) < 60:
                noise[i,:] = np.nan
                time_axis[i,:] = np.nan
                continue
            # tqdm.write(str((len(accuracy_NMEA_opt(Z-np.mean(Z)))+120)/(60*60)))
            noise_temp = accuracy_NMEA_opt(Z-np.mean(Z))
            noise[i,:len(noise_temp)]  = noise_temp
            time_axis[i,:len(obj.time_4)] = obj.time_4
        return time_axis,noise
if __name__ == '__main__':
    t,gps =run_NMEA_data(100,"TRM")

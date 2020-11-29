import numpy as np
import matplotlib.pyplot as plt
import sys, time
sys.path.insert(0, "../") # to get access to adjecent packages in the repository
from extra.time_date_conversion import date_to_days
from magnetometer_event.filtering_events import filtering_to_Norway_night
from supermag_substorm_reader.magnetometer_reader import ReadMagnetomerData
from supermag_substorm_reader.substorm_event_reader import ReadSubstormEvent
from data_reader_OMNI.OMNI_data_reader import ReadOMNIData



try:
    laptop_path = "/scratch/michaesb"
    path_event = laptop_path+"substorm_event_list_2018.csv"
    path_mag = laptop_path+"20201025-17-57-supermag.csv"
    obj_event.read_csv(path_event,verbose = False)
    print("substorm event reader")
    obj_mag.read_csv(path_mag, verbose = False)
    print("magnetometer reader")

except FileNotFoundError:
    desktop_path = "/run/media/michaelsb/HDD Linux/data/"
    path_event = desktop_path+"/substorm_event_list_2018.csv"
    path_mag = desktop_path+"/20201025-17-57-supermag.csv"
    obj_event.read_csv(path_event,verbose = False)
    print("substorm event reader")
    obj_mag.read_csv(path_mag, verbose = False)
    print("magnetometer reader")


#magnetometer reader
dates_mag, time_UTC_mag,\
location_long,location_lat,\
geographic_north,geographic_east, geographic_z, \
magnetic_north,magnetic_east, magnetic_z = obj_mag.receiver_specific_data("TRO")

#then event reader
lat = obj_event.latitude
mag_time = obj_event.magnetic_time
time_UTC_event = obj_event.dates_time
dates_event, year = obj_event.day_of_year

Norway_time = time_UTC_event + 1
lat, time_of_event, Norway_time, dates_event = filtering_to_Norway_night(lat,mag_time,Norway_time,dates_event)

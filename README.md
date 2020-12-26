# master thesis CPOS System
A repository for the work done during Michael Bitneys master thesis in Space physics
This contains multiple datareaders, processing and plotting tools use to further
investigate substorms impact on GPS.

## Folders

### Data

The data is located elsewhere on the computer, as the dataset are quite large
and some is received from kartverket and can't be shared by me.

### Data readers

#### NMEA, RTIM, ROTI

data_reader_NMEA, data_reader_ROTI,data_reader_RTIM is datareaders for data
from Kartverket. NMEA data is location based data, RTIM is measurement of the
different scintillations and ROTI is map based that shows the forecasting of
the ROTI index of Norway

#### OMNI

data_reader_OMNI reads the OMNI data from NASA database of data, which contain
multiple parameters about the solar wind and more.

#### supermag_substorm

This contains datareader and other files for reading magnetometer data from Norway
and a reader for reading a substorm event list.

### Filters and processing


#### seasonal data

A place where we look at the changes for a year in NMEA data. Shows a clear
event happening in the middle of the year, but otherwise nothing conclusive
about seasonal changes

#### plasma stream event

Investigating an event happening in the middle of the year that causes big implications
on the noise levels. This appeared to be localized to certain receivers and was
not purely spacephysics phenomena, so it was not pursued.  

#### laptop specific

Files made for my laptop, so I can test stuff out without my higher performance
Desktop


#### magnetometer event

A look into the substorm event list and try to locate the events for the magnetometer


### extra
Various scripts like progressbar and such that doesn't fit in any particular folder

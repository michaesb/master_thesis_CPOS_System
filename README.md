# Master thesis CPOS System
A repository for the work done during Michael Bitneys master thesis in Space physics
This contains multiple datareaders, processing and plotting tools use to further
investigate substorms impact on GPS.
Mainly tested in Linux, but should in theory work with Windows.

## Folders

### Data

The data is located elsewhere on the computer, as the dataset are quite large
and some is received from kartverket and can't be shared by me.

### Data readers

Each datareader has a class structure, so can be used in objectoriented way in
other scripts. Each datareader has a test with the help of Unitest. They can be
run indiviually or you can run all by typing
´´´
pytest -v
´´´
in the master_thesis_CPOS_system folder. This will work without having the data
available as it is tested on a small file of the data in the folder.
All test should be good, as of 1. january 2021.

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
Various scripts like progressbar, noise calulation and such that doesn't fit in any particular folder.

## Dependencies

Here we make use of various packages som are, but not limited to:

* Scipy

* Pandas

* Unittest

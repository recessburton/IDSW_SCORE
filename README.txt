Copyright (C),2014-2016, YTC, BJFU, www.bjfulinux.cn, www.muheda.com
Created on 16/9/19 09:14

@author: Gaoxiang Yang, ytc, yanggaoxiang@dtbpoint.com
@version: 0.1

This README file can also be found in http://123.56.10.87:8090/x/UwAR.

This application targets to score the driving behavior.

With the driving behavior data from CSV files from disk, we utilize the specific and
concise formulation to yield the bounded score which, for example, would be 0-100.
The score rule or formulation can be found in http://123.56.10.87:8090/x/UwAR.

The result is stored on disk as .csv file following the format below:
filename:results-year-month.csv
e.g. results-2016-08.csv

File format:
id: denotes the IDSW device ID;
score: denotes driving behavior scores of drivers;
rank: denotes the rank among all the drivers;
defeat: denotes how much percentage of antagonists this driver has been vanquished;
advice: denotes the advices given to each driver
month: denotes the month the statistic taken place


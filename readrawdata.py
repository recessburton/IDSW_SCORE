#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C),2014-2016, YTC, BJFU, www.bjfulinux.cn, www.muheda.com
Created on 16/9/19 10:16

@author: Gaoxiang Yang, ytc, yanggaoxiang@dtbpoint.com
@version: 0.1
"""

import pandas as pd
from pandas import DataFrame as df

def inputRawCSV(dirpath):
    '''
    Read the given drive date CSV files on disk
    :param string:root dirpath,e.g. "/usr/local/data/staticsData/":
    :return DataFrame:
    '''
    #read WDDriveLength
    s = pd.read_csv(dirpath+"/WDDriveLength.csv", header=None)
    s.columns = ['id','s','date']

    #read WDDriveTime
    t = pd.read_csv(dirpath+"/WDDriveTime.csv", header=None)
    t.columns= ['id', 't', 'date']
    #combine s & t
    driveActionData = pd.merge(s, t, on=['id', 'date'], how='inner')

    #read WDDriveRainLength
    sr = pd.read_csv(dirpath+"/WDDriveRainLength.csv", header=None)
    sr.columns = ['id', 'sr', 'date']
    #combine driveActionData & sr, use LEFT connection, the 0-value is applicable as value NaN
    driveActionData = pd.merge(driveActionData, sr, on=['id', 'date'], how='left')

    #read WDDriveNightTimes
    fn = pd.read_csv(dirpath+"/WDDriveNightTimes.csv", header=None)
    fn.columns = ['id', 'fn', 'date']
    #combine driveActionData & fn, use LEFT connection, the 0-value is applicable as value NaN
    driveActionData = pd.merge(driveActionData, fn, on=['id', 'date'], how='left')

    #read WDDriveNightLength
    sn = pd.read_csv(dirpath+"/WDDriveNightLength.csv", header=None)
    sn.columns = ['id','sn','date']
    #combine driveActionData & sn, use LEFT connection, the 0-value is applicable as value NaN
    driveActionData = pd.merge(driveActionData, sn, on=['id', 'date'], how='left')

    #read WDSpeedUp
    fu = pd.read_csv(dirpath+"/WDSpeedUp.csv", header=None)
    fu.columns = ['id','fu','date']
    #combine driveActionData & fu, use LEFT connection, the 0-value is applicable as value NaN
    driveActionData = pd.merge(driveActionData, fu, on=['id', 'date'], how='left')

    #read WDSpeedDown
    fd = pd.read_csv(dirpath+"/WDSpeedDown.csv", header=None)
    fd.columns = ['id','fd','date']
    #combine driveActionData & fd, use LEFT connection, the 0-value is applicable as value NaN
    driveActionData = pd.merge(driveActionData, fd, on=['id', 'date'], how='left')

    #read WDALDW
    ca = pd.read_csv(dirpath+"/WDALDW.csv", header=None)
    ca.columns = ['id','ca','date']
    #combine driveActionData & ca, use LEFT connection, the 0-value is applicable as value NaN
    driveActionData = pd.merge(driveActionData, ca, on=['id', 'date'], how='left')

    #read WDULDW
    cu = pd.read_csv(dirpath+"/WDULDW.csv", header=None)
    cu.columns = ['id','cu','date']
    #combine driveActionData & cu, use LEFT connection, the 0-value is applicable as value NaN
    driveActionData = pd.merge(driveActionData, cu, on=['id', 'date'], how='left')

    #read WDFCW
    w = pd.read_csv(dirpath+"/WDFCW.csv", header=None)
    w.columns = ['id','w','date']
    #combine driveActionData & w, use LEFT connection, the 0-value is applicable as value NaN
    driveActionData = pd.merge(driveActionData, w, on=['id', 'date'], how='left')

    return driveActionData
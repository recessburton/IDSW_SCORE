#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C),2014-2016, YTC, BJFU, www.bjfulinux.cn, www.muheda.com
Created on 16/9/19 11:19

@author: Gaoxiang Yang, ytc, yanggaoxiang@dtbpoint.com
@version: 0.1
"""

import pandas as pd
from pandas import DataFrame
from pandas import Series

def driveActionDataClean(driveActionData):
    '''
    Clean and filter the drive action data
    :param DataFrame:driveActionData:
    :return DataFrame:
    '''
    driveActionData = driveActionData.fillna(0)
    driveActionData = driveActionData[driveActionData['s']<2800000]#filter max drive length(m) in a day at max speed 120km/h
    driveActionData['s'] = driveActionData['s']/1000 #from m to km
    driveActionData = driveActionData[driveActionData['t']<86400]#filter max drive time in a day(s)
    driveActionData['t'] = driveActionData['t']/3600 #from s to h
    driveActionData['v'] = driveActionData['s']/driveActionData['t'] #yield velocity
    driveActionData = driveActionData[driveActionData['sr'] < 2800000]  # filter max drive length(m) in a day at max speed 120km/h
    driveActionData['sr'] = driveActionData['sr']/1000  # from m to km
    driveActionData = driveActionData[driveActionData['fn'] < 100]  # filter max drive times at night, max 100 empirically
    driveActionData = driveActionData[driveActionData['sn'] < 1400000]  # filter max drive length(m) at night(12h) at max speed 120km/h
    driveActionData['sn'] = driveActionData['sn']/1000  # from m to km
    driveActionData = driveActionData[driveActionData['fu'] < 5000]  # filter max sharp accelerate times, empirically 5000
    driveActionData = driveActionData[driveActionData['fd'] < 5000]  # filter max sharp decelerate times, empirically 5000
    driveActionData = driveActionData[driveActionData['ca'] < 1000]  # filter max lane departure times, empirically 1000
    driveActionData = driveActionData[driveActionData['cu'] < 1000]  # filter max dangerous lane departure times, empirically 5000
    driveActionData = driveActionData[driveActionData['w'] < 20]  # filter max collision warning times, empirically 20
    return driveActionData

def monthlyGroupedData(driveActionData):
    '''
    Group drive action data a month by every driver
    :param DataFrame:driveActionData:
    :return DataFrameGroupBy Object:
    '''
    groupedDriverData = driveActionData.groupby('id')
    return groupedDriverData

def getMax(groupedDriverData, driveActionKey):
    '''
    Get the Maximum in groupedDriverData by the given driveActionKey, e.g. WDSeedUp.
    :param DataFrameGroupBy Object:groupedDriverData:
    :param string: driveActionKey:
    :return DataFrame:
    '''
    return groupedDriverData[driveActionKey].max()

def getMin(groupedDriverData, driveActionKey):
    '''
    Get the Minimum in groupedDriverData by the given driveActionKey, e.g. WDSeedUp.
    :param DataFrameGroupBy Object:groupedDriverData:
    :param string: driveActionKey:
    :return DataFrame:
    '''
    return groupedDriverData[driveActionKey].min()

def getAvg(groupedDriverData, driveActionKey):
    '''
    Get the average value in groupedDriverData by the given driveActionKey, e.g. WDSeedUp.
    :param DataFrameGroupBy Object:groupedDriverData:
    :param string: driveActionKey:
    :return DataFrame:
    '''
    return groupedDriverData[driveActionKey].mean()

def getSum(groupedDriverData, driveActionKey):
    '''
    Get the summation in groupedDriverData by the given driveActionKey, e.g. WDSeedUp.
    :param DataFrameGroupBy Object:groupedDriverData:
    :param string: driveActionKey:
    :return DataFrame:
    '''
    return groupedDriverData[driveActionKey].sum()

def getTotalAvg(driveActionData, driveActionKey):
    '''
    Get the average value of the total values of the specific key.
    :param DataFrame:driveActionData:
    :param string:driveActionKey:
    :return float:
    '''
    return driveActionData[driveActionKey].mean()


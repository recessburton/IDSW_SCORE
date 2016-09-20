#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C),2014-2016, YTC, BJFU, www.bjfulinux.cn, www.muheda.com
Created on 16/9/19 10:07

@author: Gaoxiang Yang, ytc, yanggaoxiang@dtbpoint.com
@version: 0.1
"""

import time
import os
import ConfigParser
import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas import Series
import readrawdata as readcsv
import dataconstruct

# the weights in the formula in rule doc.
weights = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
# the view window, here it is 30 days specifically.
N = 30
config = ConfigParser.ConfigParser()
config.readfp(open("./config.ini", "rb"))
rawdatapath = config.get("global", "rawdatapath")
resultdatapath = config.get("global", "resultdatapath")



def calculateScore():
    '''
    Calculate drive action score.
    :return DataFrames:
    '''
    driveActionData = readcsv.inputRawCSV(rawdatapath)
    driveActionData = dataconstruct.driveActionDataClean(driveActionData)
    groupedData = dataconstruct.monthlyGroupedData(driveActionData)

    fraction1 = weights[0]*np.tanh((dataconstruct.getTotalAvg(driveActionData,'v')\
                                        -dataconstruct.getSum(groupedData,'s')/dataconstruct.getSum(groupedData,'t'))\
                                        /(dataconstruct.getMax(groupedData,'v')-dataconstruct.getMax(groupedData,'v')))
    fraction2 = weights[1]*np.tanh((dataconstruct.getSum(groupedData,'sr')+dataconstruct.getSum(groupedData,'sn'))\
                                   /(1+dataconstruct.getSum(groupedData,'s')))
    fraction3 = weights[2]*np.tanh(dataconstruct.getSum(groupedData,'sn')\
                                   /(1+dataconstruct.getSum(groupedData,'fn')))
    fraction4 = weights[3]*np.tanh(dataconstruct.getSum(groupedData,'fu')/N)
    fraction5 = weights[4]*np.tanh(dataconstruct.getSum(groupedData,'fd')/N)
    fraction6 = weights[5]*np.tanh(dataconstruct.getSum(groupedData,'cu')\
                                   /(1+dataconstruct.getSum(groupedData,'ca')))
    fraction7 = weights[6]*np.tanh(dataconstruct.getSum(groupedData,'w')/N)
    driveActionScoresSeries = 50.0/7.0*(13.0+fraction1-fraction2-fraction3-fraction4-fraction5-fraction6-fraction7)
    driveActionScores = DataFrame({'id':driveActionScoresSeries.index.values,'score':driveActionScoresSeries.values},index=np.arange(driveActionScoresSeries.count()))
    return driveActionData,driveActionScores


def ranking(driveActionScores):
    '''
    Ranking the drive action scores and calculate how much percentage of
    antagonists this driver has been vanquished.
    :param DataFrame:driveActionScores:
    :return DataFrame:
    '''
    totaldrivers = driveActionScores['id'].count()
    driveActionScores['rank'] = driveActionScores['score'].rank(ascending=False)
    driveActionScores['defeat'] = 1 - driveActionScores['rank']/totaldrivers #the percentage the drivers has been defeat
    driveActionScores['score'] = Series([min(max(40.0,score),99.0) for score in driveActionScores['score']])#bound the score in 40 and 99
    driveActionScores['defeat'] = Series([min(max(0.01,defeat),0.98) for defeat in driveActionScores['defeat']])#bound the defeat in 0.01 and 0.98
    return driveActionScores


def advice(driveActionData, driveActionScores):
    """
    Give advices to each driver in every indicator when the driver has worse behavior
    than 75% of all drivers do.
    ref. Advice Strings (read from "Advices.txt").
    :param driveActionScores:
    :return:
    """
    valmap = {'s' :'WDDriveLength',
              't' :'WDDriveTime',
              'sr':'WDDriveRainLength',
              'v' :'DriveAvgSpeed',
              'fn':'WDDriveNightTimes',
              'sn':'WDDriveNightLength',
              'fu':'WDSpeedUp',
              'fd':'WDSpeedDown',
              'ca':'WDALDW',
              'cu':'WDULDW',
              'w' :'WDFCW'}
    adviceStringsRaw=pd.read_table("Advices.txt",sep=' ',encoding="utf-8",header=None)
    adviceStrings = dict(adviceStringsRaw.to_dict('split')['data'])
    groupedData = dataconstruct.monthlyGroupedData(driveActionData)
    # yield the DataFrame that indicates the worst value of each driver
    maxValue = DataFrame({'s' :groupedData['s'].max(),
                          't' :groupedData['t' ].max(),
                          'sr':groupedData['sr'].max(),
                          'v' :groupedData['v' ].max(),
                          'fn':groupedData['fn'].max(),
                          'sn':groupedData['sn'].max(),
                          'fu':groupedData['fu'].max(),
                          'fd':groupedData['fd'].max(),
                          'ca':groupedData['ca'].max(),
                          'cu':groupedData['cu'].max(),
                          'w' :groupedData['w' ].max()})
    maxValue['id'] = maxValue.index
    maxValue.index = np.arange(maxValue['s'].count())
    maxValue['advices'] = ""
    for key in valmap.keys():
        # find rows which has bad driving behavior(worse than 75% of all drivers in every indicator)
        advs = maxValue[maxValue[key]>driveActionData[key].quantile(0.75)]['advices']
        advs = advs.fillna(" ")
        # append driving advice according to Advices.txt file
        maxValue['advices'] = advs.map(lambda x : x+adviceStrings[valmap[key]])
    maxValue['advices'] = maxValue['advices'].fillna(adviceStrings['Default'])
    advices = DataFrame({'id':maxValue['id'],'advices':maxValue['advices']})
    driveActionScores = pd.merge(driveActionScores, advices, on='id', how='inner')
    day_now = time.localtime()
    lastMonth = '%d-%02d' % (day_now.tm_year, day_now.tm_mon-1)
    driveActionScores['month'] = lastMonth
    driveActionScores['score'] = driveActionScores['score'].astype(int)
    driveActionScores['defeat'] = driveActionScores['defeat']*100
    driveActionScores['defeat'] = driveActionScores['defeat'].astype(int)
    return driveActionScores

day_now = time.localtime()
lastMonth = '%d-%02d' % (day_now.tm_year, day_now.tm_mon-1)
print lastMonth+" Initializing..."
print "Start calculate driving action scores..."
actiondata, scores = calculateScore()
print "Score done. Ranking..."
scores = ranking(scores)
print "Rank done. Giving advice..."
scores = advice(actiondata, scores)
#存库
print "Advice given. Write to files 'results-"+lastMonth+".csv'..."
if not os.path.exists(resultdatapath):
    os.mkdir(resultdatapath)
scores.to_csv(resultdatapath+"/results-"+lastMonth+".csv", encoding='utf-8')
print "Done."



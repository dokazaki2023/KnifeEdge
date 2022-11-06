#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 21:44:02 2022

@author: okazakidaiki
"""

import numpy as np
from PyDAQmx import TaskHandle,int32,DAQmxCreateTask,byref, DAQmxCreateAIVoltageChan,DAQmxCfgSampClkTiming,DAQmxStartTask,DAQmxReadAnalogF64,DAQError,DAQmxStopTask,DAQmxClearTask,DAQmx_Val_GroupByChannel,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,DAQmx_Val_Cfg_Default,DAQmx_Val_Volts

def DataAcquision(N, samplingrate):
    taskHandle = TaskHandle()
    read = int32()
    N = int(N)
    data = np.zeros((N,), dtype=np.float64)
    try: # DAQmx Configure Code
        DAQmxCreateTask("",byref(taskHandle))
        DAQmxCreateAIVoltageChan(taskHandle,b"Dev1/ai6","",DAQmx_Val_Cfg_Default,-10.0,10.0,DAQmx_Val_Volts,None)
        DAQmxCfgSampClkTiming(taskHandle,"",float(samplingrate),DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,N)
        DAQmxStartTask(taskHandle)# DAQmx Start Code # DAQmx Read Code
        DAQmxReadAnalogF64(taskHandle,N,-1,DAQmx_Val_GroupByChannel,data,N,byref(read),None)
        # print ('測定が終了しました')
    except DAQError as err:
        print ("DAQmx Error: %s"%err)
    finally:
        if taskHandle:
            DAQmxStopTask(taskHandle)
            DAQmxClearTask(taskHandle)
            
    return data
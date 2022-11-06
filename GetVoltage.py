# -*- coding: utf-8 -*-
"""
Created on Tue May 18 18:29:02 2021

@author: Ashilab
"""

from PyDAQmx import TaskHandle,int32,DAQmxCreateTask,byref, DAQmxCreateAIVoltageChan,DAQmxCfgSampClkTiming,DAQmxStartTask,DAQmxReadAnalogF64,DAQError,DAQmxStopTask,DAQmxClearTask,DAQmx_Val_GroupByChannel,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,DAQmx_Val_Cfg_Default,DAQmx_Val_Volts
import numpy as np


class GetVoltage:
    def __init__(self, channel, sampleN_per_channel, samplingrate, time_out, taskHandle=TaskHandle()):
        self.channel = channel
        self.sampleN = sampleN_per_channel
        self.rate = samplingrate
        self.time_out = time_out
        self.taskHandle = taskHandle

    def Set(self):
        try: # DAQmx Configure Code
            DAQmxCreateTask("",byref(self.taskHandle))
            for chan in self.channel:
                DAQmxCreateAIVoltageChan(self.taskHandle,chan,"",DAQmx_Val_Cfg_Default,-10,10,DAQmx_Val_Volts,None)
            DAQmxCfgSampClkTiming(self.taskHandle,"",float(self.rate),DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,self.sampleN)
        except DAQError as err:
            print ("DAQmx Error: %s"%err)
            if self.taskHandle:
                DAQmxStopTask(self.taskHandle)
                DAQmxClearTask(self.taskHandle)
    
    def Start(self):
        try: # DAQmx Configure Code
            DAQmxStartTask(self.taskHandle)# DAQmx Start Code # DAQmx Read Code
        except DAQError as err:
            print ("DAQmx Error: %s"%err)
            if self.taskHandle:
                DAQmxStopTask(self.taskHandle)
                DAQmxClearTask(self.taskHandle)
        
        
    def Get(self):
        read = int32()
        allN = len(self.channel)*self.sampleN
        rawdata = np.zeros((allN), dtype=np.float64)
        
        try: # DAQmx Configure Code
            DAQmxReadAnalogF64(self.taskHandle,-1,int(self.time_out),DAQmx_Val_GroupByChannel,rawdata,allN,byref(read),None)
        except DAQError as err:
            print ("DAQmx Error: %s"%err)
        finally:
            if self.taskHandle:
                DAQmxStopTask(self.taskHandle)
                DAQmxClearTask(self.taskHandle)
              
        Data = rawdata.reshape(-1,self.sampleN)
        return Data
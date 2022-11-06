# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 16:37:35 2022

@author: owner
"""
from PyDAQmx import Task,DAQmx_Val_Volts

def Analog_Vol_out(value):
    task = Task()
    task.CreateAOVoltageChan(b"Dev1/ao0","",-10.0,10.0,DAQmx_Val_Volts,None)
    task.StartTask()
    task.WriteAnalogScalarF64(1,10.0,value,None)
    task.StopTask()
# -*- coding: utf-8 -*-
"""
Created on Sun May  1 09:30:55 2022

@author: owner
"""
import time
def check(inst):
    N = 0
    while N < 1:       
        if inst.query('AXIX:MOTION?') == '0\r':                 
            if inst.query('AXIY:MOTION?') == '0\r':                 
                if inst.query('AXIZ:MOTION?') == '0\r':                    
                    N = N+1                  
                else:
                    time.sleep(0.1)                    
            else:
                time.sleep(0.1)            
        else:
            time.sleep(0.1)
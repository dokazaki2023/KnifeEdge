#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 17:48:29 2020

@author: okazakidaiki
"""

def move(inst,str1,str2,strX,strY,strZ):
    import time  
    k = 0
    while k < 1:
        
        if inst.query('AXIX:MOTION?') == '0\r':                   
            if inst.query('AXIY:MOTION?') == '0\r':                
                if inst.query('AXIZ:MOTION?') == '0\r':                    
                    k = k+1                   
                else:
                    time.sleep(0.1)                    
            else:
                time.sleep(0.1)           
        else:
            time.sleep(0.1)
                       
    N = 0
    inst.write('AXIX' + str1 + str2 + strX)    
    while N <2:
        if inst.query('AXIX:MOTION?') == '0\r':       
            inst.write('AXIY' + str1 + str2 + strY)           
            while N < 1:
                if inst.query('AXIY:MOTION?') == '0\r':            
                    inst.write('AXIZ' + str1 + str2 + strZ)
                    N = N+1                
                else:
                    time.sleep(0.1)
            N = N+1            
        else:
            time.sleep(0.1)


def move_XY(inst,str1,str2,strX,strY):
    import time  
    k = 0
    while k < 1:
        if inst.query('AXIX:MOTION?') == '0\r':                   
            if inst.query('AXIY:MOTION?') == '0\r':                
                if inst.query('AXIZ:MOTION?') == '0\r':                    
                    k = k+1                   
                else:
                    time.sleep(0.1)                    
            else:
                time.sleep(0.1)           
        else:
            time.sleep(0.1)
                       
    N = 0
    inst.write('AXIX' + str1 + str2 + strX)    
    while N < 1:
        if inst.query('AXIX:MOTION?') == '0\r':       
            inst.write('AXIY' + str1 + str2 + strY)           
            N = N+1            
        else:
            time.sleep(0.1)

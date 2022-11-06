#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 01:15:52 2020

@author: okazakidaiki
"""

def connect_D250():
    import pyvisa
    import time
    flag = 0
###############################################################################
#                               機器接続                                       #
#                       D/Aコンバータ、D250と接続する                               #
###############################################################################
###############################################################################
    rm = pyvisa.ResourceManager('visa32.dll') # visaのdllの取得
    print('接続可能なインターフェースは')
    print(rm.list_resources()) # 接続機器のリストアップ
    inst = rm.open_resource("GPIB0::10::INSTR")# 接続機器の選択
    inst.write("*rst; status:preset; *cls")
    print(inst.query("*IDN?")+'に接続しました')# 通信テスト　機器の名前を聞く
    # inst.values_format.use_ascii('x', '$', np.array)
###############################################################################
#                         ステージコントローラ（D250） 動作設定                       #                                                                            #
###############################################################################
###############################################################################   
    time.sleep(0.1)
    inst.write('AXIX:UNIT 0:SELSP 0:STANDARD 1:Rate0 1:DRDIV 0')#速度テーブル設定
    while flag < 1:
        if inst.query('DRDIV?') == '0\r':
            inst.write('AXIX:POS 0:HOMEP 0:CWSLE 0:CCWSLE 0')#時計回りソフトリミット設定
            flag = flag + 1
        else :
            time.sleep(0.1)

    while flag < 2:
        if inst.query('CCWSLE?') == '0\r':
            inst.write('AXIX:MEMSW0 7:MEMSW1 0:MEMSW2 0:MEMSW3 0:MEMSW4 0:MEMSW5 0:MEMSW6 0:MEMSW7 0')#機械リミットセンサ設定
            flag = flag + 1
        else :
            time.sleep(0.1)
            
    time.sleep(0.1)
    inst.write('AXIY:UNIT 0:SELSP 0:STANDARD 1:Rate0 1:DRDIV 0')#速度テーブル設定        
    while flag < 3:
        if inst.query('DRDIV?') == '0\r':
            inst.write('AXIY:POS 0:HOMEP 0:CWSLE 0:CCWSLE 0')#時計回りソフトリミット設定
            flag = flag + 1
        else :
            time.sleep(0.1)
            
    while flag < 4:
        if inst.query('CCWSLE?') == '0\r':
            inst.write('AXIY:MEMSW0 7:MEMSW1 0:MEMSW2 0:MEMSW3 0:MEMSW4 0:MEMSW5 0:MEMSW6 0:MEMSW7 0')#機械リミットセンサ設定
            flag = flag + 1
        else :
            time.sleep(0.1)  
       
    time.sleep(0.1)    
    inst.write('AXIZ:UNIT 0:SELSP 0:STANDARD 1:Rate0 1:DRDIV 0')#速度テーブル設定        
    while flag < 5:
        if inst.query('DRDIV?') == '0\r':
            inst.write('AXIZ:POS 0:HOMEP 0:CWSLE 0:CCWSLE 0')#時計回りソフトリミット設定
            flag = flag + 1
        else :
            time.sleep(0.1)

    while flag < 6:
        if inst.query('CCWSLE?') == '0\r':
            inst.write('AXIZ:MEMSW0 7:MEMSW1 0:MEMSW2 0:MEMSW3 0:MEMSW4 0:MEMSW5 0:MEMSW6 0:MEMSW7 0')#機械リミットセンサ設定
            flag = flag + 1
        else :
            time.sleep(0.1) 
    
    print('Initialize succeeded')
    return inst
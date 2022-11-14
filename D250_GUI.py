#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 10:02:53 2022

@author: okazakidaiki
"""

from PyQt5.QtWidgets import QFileDialog,QMainWindow,QApplication
from PyQt5 import  uic
from PyQt5.QtCore import Qt, QThreadPool
import sys
import os
import numpy as np
import pyqtgraph as pg
import datetime
from scipy.special import erfc
from scipy.optimize import curve_fit
import pyqtgraph.exporters # pg.exporters を呼ぶために必要
# import time

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.threadpool = QThreadPool()
        self.x = {}
        self.y = {}
        self.lines = {}
        
        global dlg1,times,Flag_direction
        times = 0
        dlg1 = uic.loadUi("D250.ui")  # 作成した page1.ui を読み出して, ダイアログ1を作成
        Flag_direction = 0

        ## Default ##
        dlg1.LineEdit_Folders.setText("C:\\Users\\owner\\Desktop\\")
        dlg1.LineEdit_Data_Number.setText('0')
        dlg1.LineEdit_Stage_LSpeed.setText('2000')
        dlg1.LineEdit_Stage_FSpeed.setText('2000')
        dlg1.LineEdit_Stage_MicroStep.setText('1')
        dlg1.LineEdit_StageX.setText('0')
        dlg1.LineEdit_StageY.setText('0')
        dlg1.LineEdit_StageZ.setText('0')
        dlg1.LineEdit_Speed.setText('500')
        dlg1.LineEdit_Response.setText('1')
        dlg1.LineEdit_Accuracy.setText('0.2')
        dlg1.LineEdit_Knife_XFrom.setText('0')
        dlg1.LineEdit_Knife_YFrom.setText('0')
        dlg1.LineEdit_Knife_ZFrom.setText('0')
        dlg1.LineEdit_Knife_XTo.setText('2000')
        dlg1.LineEdit_Knife_YTo.setText('2000')
        dlg1.LineEdit_Knife_ZTo.setText('2000')
        dlg1.LineEdit_Knife_Xpitch.setText('10')
        dlg1.LineEdit_Knife_Ypitch.setText('10')
        dlg1.LineEdit_Knife_Zpitch.setText('500')
        dlg1.LineEdit_Knife_XTime.setText('10')
        dlg1.LineEdit_Knife_YTime.setText('10')
        dlg1.LineEdit_Knife_ZTime.setText('100')
        dlg1.LineEdit_Diameter_Estimate.setText('200')
        dlg1.LineEdit_ZSCAN_From.setText('0')
        dlg1.LineEdit_ZSCAN_To.setText('2000')
        dlg1.LineEdit_ZSCAN_pitch.setText('10')
        dlg1.LineEdit_Scan_Number.setText('1')
        
        ## Text Box ##
        dlg1.LineEdit_Knife_XFrom.textChanged.connect(self.Calc)
        dlg1.LineEdit_Knife_YFrom.textChanged.connect(self.Calc)
        dlg1.LineEdit_Knife_ZFrom.textChanged.connect(self.Calc)
        dlg1.LineEdit_Knife_XTo.textChanged.connect(self.Calc)
        dlg1.LineEdit_Knife_YTo.textChanged.connect(self.Calc)
        dlg1.LineEdit_Knife_ZTo.textChanged.connect(self.Calc)
        dlg1.LineEdit_Knife_Xpitch.textChanged.connect(self.Calc)
        dlg1.LineEdit_Knife_Ypitch.textChanged.connect(self.Calc)
        dlg1.LineEdit_Knife_Zpitch.textChanged.connect(self.Calc)
        dlg1.LineEdit_Speed.textChanged.connect(self.Calc)
        dlg1.LineEdit_Response.textChanged.connect(self.Calc)

        ## Combo ##
        dlg1.ComboBox_Direction.activated[str].connect(self.Direction)
        
        ## Push Button ##
        dlg1.Button_Close.clicked.connect(self.close_application)
        dlg1.Button_Folder.clicked.connect(self.Folder)
        dlg1.Button_MOVE.clicked.connect(self.Move)
        dlg1.Button_GoORIGIN.clicked.connect(self.GoOrigin)
        dlg1.Button_SetORIGIN.clicked.connect(self.Define_Origin)
        dlg1.Button_Position.clicked.connect(self.Position)
        dlg1.Button_Knife_Measure.clicked.connect(self.Knife)
        dlg1.Button_ZSCAN_Measure.clicked.connect(self.ZSCAN)

        
        # dlg1.graphicsView1.setBackground("#FFFFFF00")# 3 背景色を設定する(#FFFFFF00 : Transparent)
        # fontCss = {'font-family': "Arial, Noto Sans Mono Regular", 'font-size': '24pt', 'color': 'white'}
        p1 = dlg1.graphicsView1.plotItem
        p1.setLabels(bottom = 'Position (um)', left='Power (mV)')
        p1.getAxis('bottom').setPen(pg.mkPen(color='w', width=1.5))
        p1.getAxis('left').setPen(pg.mkPen(color='w', width=1.5))
        
        p2 = dlg1.graphicsView2.plotItem
        p2.setLabels(bottom = 'Position (um)', left='Power (mV)')
        p2.getAxis('bottom').setPen(pg.mkPen(color='w', width=1.5))
        p2.getAxis('left').setPen(pg.mkPen(color='w', width=1.5))
        
        p3 = dlg1.graphicsView3.plotItem
        p3.setLabels(bottom = 'Position (um)', left='Radius (um)')
        p3.getAxis('bottom').setPen(pg.mkPen(color='w', width=1.5))
        p3.getAxis('left').setPen(pg.mkPen(color='w', width=1.5))
        
        dlg1.show()  # ダイアログ1を表示
        
    
    def keyPressEvent(self,e): # エスケープキーを押すと画面が閉じる
        if e.key() == Qt.Key_Escape:
            dlg1.close()
    
    def close_application(self):
        dlg1.close()  
            
    def Folder(self):
        global file_path
        file_path = QFileDialog.getExistingDirectory()
        if len(file_path) == 0:
            return
        file_path = file_path.replace('/',chr(92))+chr(92)
        dlg1.textEdit.append('Path: ' + file_path) 
        dlg1.LineEdit_Folders.setText(str(file_path))
        
    def Position(self):
        X = int(inst.query('AXIX:POS?'))
        Y = int(inst.query('AXIY:POS?'))
        Z = int(inst.query('AXIZ:POS?'))
        dlg1.textEdit.append('Pos: ' + str([X,Y,Z]))
        dlg1.textEdit.show()
        print('Current Position: ' + str([X,Y,Z]))
        
    def Direction(self, text):
        global Flag_direction
        if text == 'CW':
            Flag_direction = 0
        if text == 'CCW':
            Flag_direction = 1

    def Move(self):
        import D250_move 
        X = int(dlg1.LineEdit_StageX.text())
        Y = int(dlg1.LineEdit_StageY.text())
        Z = int(dlg1.LineEdit_StageZ.text())
        Vl = int(dlg1.LineEdit_Stage_LSpeed.text())
        Vf = int(dlg1.LineEdit_Stage_FSpeed.text())
        str1_abs = ':LSPEED0'+' '+str(Vl)
        str2_abs = ':FSPEED0'+' '+str(Vf)
        strX_abs = ':GOABS'+' '+str(X)
        strY_abs = ':GOABS'+' '+str(Y)
        strZ_abs = ':GOABS'+' '+str(Z)
        D250_move.move(inst,str1_abs,str2_abs,strX_abs,strY_abs,strZ_abs)
        dlg1.textEdit.append('Pos: ' + str([X,Y,Z])) 
        dlg1.textEdit.show()
        print('Stage has been moved')
        
    def GoOrigin(self):
        import D250_move 
        Vl = int(dlg1.LineEdit_Stage_LSpeed.text())
        Vf = int(dlg1.LineEdit_Stage_FSpeed.text())
        str1_abs = ':LSPEED0'+' '+str(Vl)
        str2_abs = ':FSPEED0'+' '+str(Vf)
        strX0 = ':GOABS 0'
        strY0 = ':GOABS 0'
        strZ0 = ':GOABS 0'
        D250_move.move(inst,str1_abs,str2_abs,strX0,strY0,strZ0)
        print('Stage is at origin')
        dlg1.textEdit.append('Pos: ' + str([0,0,0])) 
        dlg1.textEdit.show()       
        
    def Define_Origin(self):
        import time
        flag = 0
        time.sleep(0.1)
        inst.write('AXIX:HOMEP 0:POS 0')#速度テーブル設定
        while flag < 1:
            if inst.query('AXIX:POS?') == '0\r':
                inst.write('AXIY:HOMEP 0:POS 0')#時計回りソフトリミット設定
                flag = flag + 1
            else :
                time.sleep(0.1)
        while flag < 2:
            if inst.query('AXIY:POS?') == '0\r':
                inst.write('AXIZ:HOMEP 0:POS 0')#時計回りソフトリミット設定
                flag = flag + 1
            else :
                time.sleep(0.1)

    def Calc(self):
        global positionx, positiony, positionz, strx, strxx, stry, stryy, strz, samplingratex, samplingratey, \
            times, folder, strL, strF, strX, strY, strZ, Nx, Ny, Nz, Flag_direction

        Vl = int(dlg1.LineEdit_Stage_LSpeed.text())
        Vf = int(dlg1.LineEdit_Stage_FSpeed.text())
        speed = int(dlg1.LineEdit_Speed.text())
        response = int(dlg1.LineEdit_Response.text()) 
        accuracy = int(speed*response)*1e-3

        try:
            scan_rangex = int(dlg1.LineEdit_Knife_XTo.text()) - int(dlg1.LineEdit_Knife_XFrom.text())      
            scan_divx = int(dlg1.LineEdit_Knife_Xpitch.text())
            Nx = int(scan_rangex/scan_divx)       
            scan_timex = int(scan_rangex/speed)
            samplingratex = int(Nx/scan_timex)
            
            scan_rangey = int(dlg1.LineEdit_Knife_YTo.text()) - int(dlg1.LineEdit_Knife_YFrom.text())
            scan_divy = int(dlg1.LineEdit_Knife_Ypitch.text())
            Ny = int(scan_rangey/scan_divy)        
            scan_timey = int(scan_rangey/speed)
            samplingratey = int(Ny/scan_timey)

            scan_rangez = int(dlg1.LineEdit_Knife_ZTo.text()) - int(dlg1.LineEdit_Knife_ZFrom.text())
            scan_divz = int(dlg1.LineEdit_Knife_Zpitch.text())
            Nz = int(scan_rangez/scan_divz)        
            scan_timez = (scan_timex + scan_timey)*2*Nz

                                
            str1 = ':LSPEED0'+' '+str(speed/10)#ステージ駆動速度　命令
            str2 = ':FSPEED0'+' '+str(speed)#ステージ起動速度　命令
            str3 = ':PULS'+' '+str(scan_rangex)#ステージ駆動範囲　命令
            str4 = ':PULS'+' '+str(scan_rangey)#ステージ駆動範囲　命令
    
            str5 = ':LSPEED0'+' '+str(2000/10)#ステージ駆動速度　命令
            str6 = ':FSPEED0'+' '+str(2000)#ステージ起動速度　命令    
            str7 = ':PULS'+' '+str(scan_divz)#ステージ駆動範囲　

            if Flag_direction == 0:
                strx = 'AXIX' + str1 + str2 + str3 + ':GO CW'
                strxx = 'AXIX:' + str5 + str6 + str3 + ':GO CCW'
            else:
                strx = 'AXIX' + str1 + str2 + str3 + ':GO CCW'
                strxx = 'AXIX:' + str5 + str6 + str3 + ':GO CW'
            stry = 'AXIY' + str1 + str2 + str4 + ':GO CW'
            stryy = 'AXIY:' + str5 + str6 + str4 + ':GO CCW'
            strz = 'AXIZ' + str5 + str6 + str7 + ':GO CW'        
        except:
            return
        
        strL = ':LSPEED0'+' '+str(Vl)
        strF = ':FSPEED0'+' '+str(Vf)
        strX = ':GOABS'+' '+str(int(dlg1.LineEdit_Knife_XFrom.text()))
        strY = ':GOABS'+' '+str(int(dlg1.LineEdit_Knife_YFrom.text()))
        strZ = ':GOABS'+' '+str(int(dlg1.LineEdit_Knife_ZFrom.text()))
        
        dlg1.LineEdit_Knife_XTime.setText(str(scan_timex)) 
        dlg1.LineEdit_Knife_YTime.setText(str(scan_timey)) 
        dlg1.LineEdit_Knife_ZTime.setText(str(scan_timez)) 
        dlg1.LineEdit_Accuracy.setText(str(accuracy)) 
        
        positionx = np.linspace(int(dlg1.LineEdit_Knife_XFrom.text()),int(dlg1.LineEdit_Knife_XTo.text()),Nx)                       
        positiony = np.linspace(int(dlg1.LineEdit_Knife_YFrom.text()),int(dlg1.LineEdit_Knife_YTo.text()),Ny)
        positionz = np.linspace(int(dlg1.LineEdit_Knife_ZFrom.text()),int(dlg1.LineEdit_Knife_ZTo.text()),Nz+1)
        
        folder = str(dlg1.LineEdit_Folders.text())
        times = int(dlg1.LineEdit_Data_Number.text())


    def Knife(self):
        import D250_move, D250_check, AD_Convert_Ch6 
        global times, filename0, filename1, filename2, z_start, z_end, z_div
        
        def KnifeEdge_fit(x,a,b,c):
            f = a*erfc(np.sqrt(2)*((x-c)/b))
            return f 

        legend = "dammy,position"
        power_x = np.zeros((Nz+3,Nx), dtype=np.float64)
        power_y = np.zeros((Nz+3,Ny), dtype=np.float64)
        power_z =  np.zeros((6,Nz+1), dtype=np.float64)
        rawdata_x = np.zeros((Nx,), dtype=np.float64)
        rawdata_y = np.zeros((Ny,), dtype=np.float64)
        dammy_x = np.zeros((Nx,), dtype=np.float64)
        dammy_y = np.zeros((Ny,), dtype=np.float64)
        dammy_z = np.zeros((Nz+1,), dtype=np.float64)
        r_x = np.zeros(Nz+1)
        r_y = np.zeros(Nz+1)
        z_x = np.zeros(Nz+1)
        z_y = np.zeros(Nz+1)
    
        power_x[0] = dammy_x
        power_x[1] = positionx
        power_y[0] = dammy_y
        power_y[1] = positiony
        power_z[0] = dammy_z
        power_z[1] = positionz
        
        j = 0

        D250_move.move(inst,strL,strF,strX,strY,strZ)
        p1 = dlg1.graphicsView1
        p2 = dlg1.graphicsView2
        p3 = dlg1.graphicsView3
        
        rawdata_x = AD_Convert_Ch6.DataAcquision(Nx,samplingratex)
        p1.clear()
        p2.clear()
        
        t = 3*np.pi/2
        diameter = float(dlg1.LineEdit_Diameter_Estimate.text())

        for i in range(Nz+1):
            print('z_position = ' + str(positionz[i]) + ' um')
            t = t + 5*np.pi*(i/(Nz+2))/3
            Red = int(127*np.sqrt(((np.cos(t))**2 + (np.sin(t) - 1)**2)))
            Green = int(127*np.sqrt(((np.cos(t)+np.sqrt(3)/2)**2 + (np.sin(t) + 1/2)**2)))
            Blue = int(127*np.sqrt(((np.cos(t)-np.sqrt(3)/2)**2 + (np.sin(t) + 1/2)**2)))
            
            D250_check.check(inst)                                   
            inst.write(strx)
            rawdata_x = AD_Convert_Ch6.DataAcquision(Nx,samplingratex)            
            D250_check.check(inst)
            D250_move.move_XY(inst,strL,strF,strX,strY)
            power_x[j+2] = rawdata_x.T
            p1.plot(x=positionx, y=rawdata_x*1e3, symbol='o', pen=None, symbolBrush=(Red,Green,Blue), symbolSize=10)
            pg.QtGui.QApplication.processEvents()      
            initialValue = np.array([np.max(rawdata_x), diameter/2, (np.max(positionx)+np.min(positionx))/2])
            try:
                param, cov = curve_fit(KnifeEdge_fit,positionx,rawdata_x,initialValue,maxfev=1000)
                diameter = np.abs(np.round(2*param[1],6))
                r_x[i] = diameter/2
                z_x[i] = param[2]
            except:
                r_x[i] = np.nan
                z_x[i] = np.nan
                
            D250_check.check(inst)      
            inst.write(stry)
            rawdata_y = AD_Convert_Ch6.DataAcquision(Ny,samplingratey)                  
            D250_check.check(inst)
            D250_move.move_XY(inst,strL,strF,strX,strY)
            power_y[j+2] = rawdata_y.T
            p2.plot(x=positiony, y=rawdata_y*1e3, symbol='t', pen=None, symbolBrush=(Red,Green,Blue), symbolSize=10)
            pg.QtGui.QApplication.processEvents()
            try:
                initialValue = np.array([np.max(rawdata_y), diameter/2, (np.max(positiony)+np.min(positiony))/2])
                param, cov = curve_fit(KnifeEdge_fit,positiony,rawdata_y,initialValue,maxfev=1000)
                diameter = np.abs(np.round(2*param[1],6))
                r_y[i] = diameter/2
                z_y[i] = param[2]
            except:
                r_y[i] = np.nan
                z_y[i] = np.nan

            D250_check.check(inst)        
            legend = legend + ",Measurement" + str(i)
            inst.write(strz)
            
            p3.clear()
            p3.plot(x=positionz, y=r_x, symbol='o', pen=None, symbolBrush='r', symbolSize=10)
            p3.plot(x=positionz, y=r_y, symbol='t', pen=None, symbolBrush='b', symbolSize=10)
            pg.QtGui.QApplication.processEvents()  
            j = j+1

        D250_check.check(inst)
        D250_move.move(inst,strL,strF,strX,strY,strZ) 
        
        dlg1.textEdit.append(str(datetime.datetime.now()) + ' : Measurement No.'+str(int(dlg1.LineEdit_Data_Number.text()))+ ' is finished')
        dlg1.LineEdit_Data_Number.setText(str(times))
        print('KnifeEdge Finished')
        
        # ## save datas
        folder = str(dlg1.LineEdit_Folders.text())
        power_z[2] = r_x.T
        power_z[3] = r_y.T
        power_z[4] = z_x.T
        power_z[5] = z_y.T
        
        folder = str(dlg1.LineEdit_Folders.text())
        directory = folder + str(datetime.date.today())

        def duplicate_rename_x(filename):
            new_name = filename
            global times
            if os.path.exists(filename):
                name, ext = os.path.splitext(filename)
                while True:
                    new_name = "{}{}({}){}".format(directory, '_KnifeEdge_x', times, ext)
                    if not os.path.exists(new_name):
                        return new_name
                    times += 1
                    dlg1.LineEdit_Data_Number.setText(str(times))
            else:
                return new_name
        
        
        def duplicate_rename_y(filename):
            new_name = filename
            global times
            if os.path.exists(filename):
                name, ext = os.path.splitext(filename)
                while True:
                    new_name = "{}{}({}){}".format(directory, '_KnifeEdge_y', times, ext)
                    if not os.path.exists(new_name):
                        return new_name
                    times += 1
                    dlg1.LineEdit_Data_Number.setText(str(times))
            else:
                return new_name
        
        def duplicate_rename_z(filename):
            new_name = filename
            global times
            if os.path.exists(filename):
                name, ext = os.path.splitext(filename)
                while True:
                    new_name = "{}{}({}){}".format(directory, '_KnifeEdge_z', times, ext)
                    if not os.path.exists(new_name):
                        return new_name
                    times += 1
                    dlg1.LineEdit_Data_Number.setText(str(times))
            else:
                return new_name
        
        filename0 = "{}{}({}){}".format(directory, '_KnifeEdge_x', times, '.csv')                      
        filename0 = duplicate_rename_x(filename0)
        filename1 = "{}{}({}){}".format(directory, '_KnifeEdge_y', times, '.csv')
        filename1 = duplicate_rename_y(filename1)        
        filename2 = "{}{}({}){}".format(directory, '_KnifeEdge_z', times, '.csv')
        filename2 = duplicate_rename_z(filename2)
        filename3 = "{}{}({}){}".format(directory, '_KnifeEdge_x', times, '.png')                      
        filename3 = duplicate_rename_x(filename3)
        filename4 = "{}{}({}){}".format(directory, '_KnifeEdge_y', times, '.png')
        filename4 = duplicate_rename_y(filename4)        
        filename5 = "{}{}({}){}".format(directory, '_KnifeEdge_z', times, '.png')
        filename5 = duplicate_rename_z(filename5)
        filename6 = "{}{}({}){}".format(directory, '_KnifeEdge', times, '.txt')
        filename6 = duplicate_rename_z(filename6)
        
        try:
            np.savetxt(filename0, power_x.T, fmt="%.10f",delimiter=",", header=legend)# 保存する文字列。
            np.savetxt(filename1, power_y.T, fmt="%.10f",delimiter=",", header=legend)# 保存する文字列。
            np.savetxt(filename2, power_z.T, fmt="%.10f",delimiter=",", header="dammy,z,rx,ry,zx,zy")# 保存する文字列。
            exporter = pg.exporters.ImageExporter(dlg1.graphicsView1.scene()) # exportersの直前に pg.QtGui.QApplication.processEvents() を呼ぶ！
            exporter.parameters()['width'] = 1000
            exporter.export(filename3)
            exporter = pg.exporters.ImageExporter(dlg1.graphicsView2.scene()) # exportersの直前に pg.QtGui.QApplication.processEvents() を呼ぶ！
            exporter.parameters()['width'] = 1000
            exporter.export(filename4)
            exporter = pg.exporters.ImageExporter(dlg1.graphicsView3.scene()) # exportersの直前に pg.QtGui.QApplication.processEvents() を呼ぶ！
            exporter.parameters()['width'] = 1000
            exporter.export(filename5)
            
            dlg1.textEdit.append(str(datetime.datetime.now()) + ' : Measurement No.'+str(int(dlg1.LineEdit_Data_Number.text()))+ ' is finished')
            times = int(dlg1.LineEdit_Data_Number.text()) + 1 # measurement number
            dlg1.LineEdit_Data_Number.setText(str(times))
            
            text = str(dlg1.textEdit.toPlainText())
            with open(filename6, 'w') as f:
                f.write(text)
            print('ファイルは正常に保存されました。')
        except:
            print('ERROR:ファイルの保存に失敗しました。')

        
        # ## fit w0
        def gaussianbeam_fit(x,a,b,c):
            f = a*np.sqrt(1+((x-b)**2)/(c**2))
            return f
        
        try:
            initialValue = np.array([min(r_x), positionz[np.argmin(r_x)], 100])
            param, cov = curve_fit(gaussianbeam_fit,positionz,r_x,initialValue,maxfev=1000)
            # fit_x = gaussianbeam_fit(positionz,param[0],param[1],param[2])
            wsize = round(param[0],2)
            zpos = round(param[1],0)
            print('z_position_x = ' + str(zpos))
            print('rx_0 = ' + str(wsize))
            dlg1.textEdit.append('rx_0 = ' + str(wsize))
            
            initialValue = np.array([min(r_y), positionz[np.argmin(r_y)], 100])
            param, cov = curve_fit(gaussianbeam_fit,positionz,r_y,initialValue,maxfev=1000)
            # fit_x = gaussianbeam_fit(positionz,param[0],param[1],param[2])
            wsize = round(param[0],2)
            zpos = round(param[1],0)
            print('z_position_y = ' + str(zpos))
            print('ry_0 = ' + str(wsize))
            dlg1.textEdit.append('ry_0 = ' + str(wsize))

        except:
            return
        
        D250_check.check(inst)
        D250_move.move(inst,strL,strF,strX,strY,strZ) 
        
        
    def ZSCAN(self):
        import GetVoltage as ADC
        import D250_check

        BNC_PS = b"Dev1/ai3"
        BNC_OA = b"Dev1/ai4"
        BNC_CA = b"Dev1/ai5"

        scanN = int(dlg1.Scan_Number.text())
        speed_ZSCAN = int(dlg1.LineEdit_Speed.text())
        
        scan_range_ZSCAN = int(dlg1.LineEdit_ZSCAN_To.text()) - int(dlg1.LineEdit_ZSCAN_From.text())
        scan_div_ZSCAN = int(dlg1.LineEdit_ZSCAN_pitch.text())
        N_ZSCAN = int(scan_range_ZSCAN/scan_div_ZSCAN)
        scan_time_ZSCAN = int(scan_range_ZSCAN/speed_ZSCAN)
        samplingrate_ZSCAN = int(N_ZSCAN/scan_time_ZSCAN)
        
        dlg1.textEdit.append('1 Scan SampleN: {0}'.format(N_ZSCAN))
        dlg1.textEdit.append('Scan Time: {0} x {1} times'.format(scan_time_ZSCAN+1, scanN*2))
        print('1 Scan SampleN: {0}'.format(N_ZSCAN))
        print('Scan Time: {0} x {1} times'.format(scan_time_ZSCAN+1, scanN*2))

        position_ZSCAN = np.linspace(int(dlg1.LineEdit_Knife_ZFrom.text()),int(dlg1.LineEdit_Knife_ZTo.text()),N_ZSCAN)
        data_PS = np.zeros((scanN*2, N_ZSCAN), dtype=np.float64)
        data_OA = np.zeros((scanN*2, N_ZSCAN), dtype=np.float64)
        data_CA = np.zeros((scanN*2, N_ZSCAN), dtype=np.float64)
        print("Start")
        
        str_ZSCAN1 = ':LSPEED0'+' '+str(speed_ZSCAN/10)#ステージ駆動速度　命令
        str_ZSCAN2 = ':FSPEED0'+' '+str(speed_ZSCAN)#ステージ起動速度　命令    
        str_ZSCAN3 = ':PULS'+' '+str(scan_range_ZSCAN)#ステージ駆動範囲　                                   
        str_ZSCAN_CW = 'AXIZ' + str_ZSCAN1 + str_ZSCAN2 + str_ZSCAN3 + ':GO CW'
        str_ZSCAN_CCW = 'AXIZ' + str_ZSCAN1 + str_ZSCAN2 + str_ZSCAN3 + ':GO CCW'
        
        p1 = dlg1.graphicsView1
        p2 = dlg1.graphicsView2
        p3 = dlg1.graphicsView3
        p1.clear()
        p2.clear()
        p3.clear()
        
        t = 3*np.pi/2
        legend = "dammy,position"
        dammy_ZSCAN = np.zeros((N_ZSCAN,1), dtype=np.float64)

        for i in range(scanN):
            t = t + 5*np.pi*(i/(scanN+2))/3
            Red = int(127*np.sqrt(((np.cos(t))**2 + (np.sin(t) - 1)**2)))
            Green = int(127*np.sqrt(((np.cos(t)+np.sqrt(3)/2)**2 + (np.sin(t) + 1/2)**2)))
            Blue = int(127*np.sqrt(((np.cos(t)-np.sqrt(3)/2)**2 + (np.sin(t) + 1/2)**2)))
            
            print("   front {0}".format(i))           
            Task = ADC.GetVoltage([BNC_PS, BNC_OA, BNC_CA], N_ZSCAN, samplingrate_ZSCAN, 2*scan_time_ZSCAN)
            Task.Set()
            inst.write(str_ZSCAN_CW)            
            Task.Start()
            D250_check.check(inst)
            
            raw_data = Task.Get()
            data_PS[2*i] = raw_data[0]
            data_OA[2*i] = raw_data[1]
            data_CA[2*i] = raw_data[2]
            
            p1.plot(x=position_ZSCAN, y=raw_data[0], symbol='s', pen=None, symbolBrush=(Red,Green,Blue), symbolSize=10)
            p1.plot(x=position_ZSCAN, y=raw_data[1], symbol='o', pen=None, symbolBrush=(Red,Green,Blue), symbolSize=10)
            p1.plot(x=position_ZSCAN, y=raw_data[2], symbol='x', pen=None, symbolBrush=(Red,Green,Blue), symbolSize=10)
            pg.QtGui.QApplication.processEvents()
            legend = legend + ",MeasurementCW" + str(i)
                    
            print("   back {0}".format(i))           
            Task = ADC.GetVoltage([BNC_PS, BNC_OA, BNC_CA], N_ZSCAN, samplingrate_ZSCAN, 2*scan_time_ZSCAN)
            Task.Set()
            inst.write(str_ZSCAN_CCW)  
            Task.Start()
            D250_check.check(inst)
            
            raw_data = Task.Get()
            data_PS[2*i+1] = np.flipud(raw_data[0])
            data_OA[2*i+1] = np.flipud(raw_data[1])
            data_CA[2*i+1] = np.flipud(raw_data[2])
            
            p2.plot(x=position_ZSCAN, y=raw_data[0], symbol='s', pen=None, symbolBrush=(Red,Green,Blue), symbolSize=10)
            p2.plot(x=position_ZSCAN, y=raw_data[1], symbol='o', pen=None, symbolBrush=(Red,Green,Blue), symbolSize=10)
            p2.plot(x=position_ZSCAN, y=raw_data[2], symbol='x', pen=None, symbolBrush=(Red,Green,Blue), symbolSize=10)
            pg.QtGui.QApplication.processEvents()
            legend = legend + ",MeasurementCCW" + str(i)

        print("Finish")
        dlg1.textEdit.append(str(datetime.datetime.now()) + ' : Measurement No.'+str(int(dlg1.LineEdit_Data_Number.text()))+ ' is finished')
        times = int(dlg1.LineEdit_Data_Number.text()) + 1 # measurement number
        dlg1.LineEdit_Data_Number.setText(str(times))
        
        PS = np.mean(data_PS, axis=0)
        OA = np.mean(data_OA, axis=0)
        CA = np.mean(data_CA, axis=0)
        p3.plot(x=position_ZSCAN, y=PS, symbol='s', pen=None, symbolBrush=(Red,Green,Blue), symbolSize=10)
        p3.plot(x=position_ZSCAN, y=OA, symbol='o', pen=None, symbolBrush=(Red,Green,Blue), symbolSize=10)
        p3.plot(x=position_ZSCAN, y=CA, symbol='x', pen=None, symbolBrush=(Red,Green,Blue), symbolSize=10)
            
        savedata_PS = np.block([dammy_ZSCAN, position_ZSCAN.reshape(-1,1), data_PS.T])
        savedata_OA = np.block([dammy_ZSCAN, position_ZSCAN.reshape(-1,1), data_OA.T])
        savedata_CA = np.block([dammy_ZSCAN, position_ZSCAN.reshape(-1,1), data_CA.T])
        folder = str(dlg1.LineEdit_Folders.text())
        directory = folder + str(datetime.date.today())

        def duplicate_rename(filename):
            new_name = filename
            global times
            if os.path.exists(filename):
                name, ext = os.path.splitext(filename)
                while True:
                    new_name = "{}{}({}){}".format(directory, '_FRAC', times, ext)
                    if not os.path.exists(new_name):
                        return new_name
                    times += 1
                    dlg1.LineEdit_Data_Number.setText(str(times))
            else:
                return new_name
            
        filename0 = "{}{}({}){}".format(directory, '_ZSCAN_PS', times, '.csv')                      
        filename0 = duplicate_rename(filename0)
        filename1 = "{}{}({}){}".format(directory, '_ZSCAN_OA', times, '.csv')
        filename1 = duplicate_rename(filename1)        
        filename2 = "{}{}({}){}".format(directory, '_ZSCAN_CA', times, '.csv')
        filename2 = duplicate_rename(filename2)
        filename3 = "{}{}({}){}".format(directory, '_ZSCAN_CW', times, '.png')                      
        filename3 = duplicate_rename(filename3)
        filename4 = "{}{}({}){}".format(directory, '_ZSCAN_CCW', times, '.png')
        filename4 = duplicate_rename(filename4)        
        filename5 = "{}{}({}){}".format(directory, '_ZSCAN', times, '.txt')
        filename5 = duplicate_rename(filename5)
        
        try:
            np.savetxt(filename0, savedata_PS, fmt="%.10f",delimiter=",", header = legend)# 保存する文字列。 
            np.savetxt(filename1, savedata_OA, fmt="%.10f",delimiter=",", header = legend)# 保存する文字列。 
            np.savetxt(filename2, savedata_CA, fmt="%.10f",delimiter=",", header = legend)# 保存する文字列。 
            exporter = pg.exporters.ImageExporter(dlg1.graphicsView1.scene()) # exportersの直前に pg.QtGui.QApplication.processEvents() を呼ぶ！
            exporter.parameters()['width'] = 1000
            exporter.export(filename3) 
            exporter = pg.exporters.ImageExporter(dlg1.graphicsView2.scene()) # exportersの直前に pg.QtGui.QApplication.processEvents() を呼ぶ！
            exporter.parameters()['width'] = 1000
            exporter.export(filename4)   
            text = str(dlg1.textEdit.toPlainText())
            with open(filename5, 'w') as f:
                f.write(text)
            print('ファイルは正常に保存されました。')
        except:
            print('ERROR:ファイルの保存に失敗しました。')

if __name__ == "__main__":
    global inst
    import D250_connect_x
    inst = D250_connect_x.connect_D250()
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()

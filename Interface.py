#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.5 (standalone edition) on Wed Sep 17 14:20:34 2014

import wx
import TelnetController
import re
import os
import telnetlib
import logging
import Device
import Provision
import Setup
import threading
import thread
from multiprocessing.pool import ThreadPool
import Queue
import sys
import time
import random

# begin wxGlade: extracode
# end wxGlade

class FuncLog(logging.Handler):
    def __init__(self, ctrl):
        logging.Handler.__init__(self)
        self.ctrl = ctrl


    def emit(self, record):
        self.ctrl.AppendText(self.format(record) + "\n")




class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE ^ (wx.MAXIMIZE | wx.RESIZE_BORDER)
        wx.Frame.__init__(self, *args, **kwds)
        self.notebook_2 = wx.Notebook(self, -1, style=0)
        # pane1
        self.notebook_2_pane_1 = wx.Panel(self.notebook_2, -1, style=wx.TAB_TRAVERSAL | wx.FULL_REPAINT_ON_RESIZE)

        self.lblname = wx.StaticText(self.notebook_2_pane_1, label="Sector IP Address :", pos=(20, 30))
        self.sector = wx.TextCtrl(self.notebook_2_pane_1, value="10.107.40.1", pos=(150, 30), size=(140, -1),
                                  style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)

        self.lblname = wx.StaticText(self.notebook_2_pane_1, label="DL CIR :", pos=(20, 60))
        self.dlcir = wx.TextCtrl(self.notebook_2_pane_1, value="50000", pos=(150, 60), size=(140, -1),
                                 style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)

        self.lblname = wx.StaticText(self.notebook_2_pane_1, label="UL CIR :", pos=(20, 90))
        self.ulcir = wx.TextCtrl(self.notebook_2_pane_1, value="50000", pos=(150, 90), size=(140, -1),
                                 style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
        self.radio = wx.CheckBox(self.notebook_2_pane_1, label="Radio OFF-ON", pos=(350, 50))

        self.lblname = wx.StaticText(self.notebook_2_pane_1, label="DL PIR :", pos=(20, 120))
        self.dlpir = wx.TextCtrl(self.notebook_2_pane_1, value="50000", pos=(150, 120), size=(140, -1),
                                 style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)

        self.lblname = wx.StaticText(self.notebook_2_pane_1, label="UL PIR :", pos=(20, 150))
        self.ulpir = wx.TextCtrl(self.notebook_2_pane_1, value="50000", pos=(150, 150), size=(140, -1),
                                 style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)

        self.logger = wx.TextCtrl(self.notebook_2_pane_1, pos=(20, 620), size=(700, 200),
                                  style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)

        # A button
        self.button = wx.Button(self.notebook_2_pane_1, label="Save", pos=(20, 180))

        self.logr = logging.getLogger('')
        self.logr.setLevel(logging.DEBUG)
        hdlr = FuncLog(self.logger)
        # hdlr.setFormatter(logging.Formatter('%(levelname)s | %(name)s |%(message)s [@ %(asctime)s in %(filename)s:%(lineno)d]'))
        hdlr.setFormatter(logging.Formatter('%(levelname)s |%(message)s'))
        self.logr.addHandler(hdlr)

        #pan 2
        #self.notebook_2_pane_2 = wx.Panel(self.notebook_2, -1, style=wx.TAB_TRAVERSAL | wx.FULL_REPAINT_ON_RESIZE)




        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBoxRadio, self.radio)
        self.sector.Bind(wx.EVT_KEY_DOWN, self.onEnter)
        self.dlcir.Bind(wx.EVT_KEY_DOWN, self.onEnter)
        self.ulcir.Bind(wx.EVT_KEY_DOWN, self.onEnter)
        self.dlpir.Bind(wx.EVT_KEY_DOWN, self.onEnter)
        self.ulpir.Bind(wx.EVT_KEY_DOWN, self.onEnter)
        self.button.Bind(wx.EVT_KEY_DOWN, self.onEnter)

        self.notebook_2_pane_2 = wx.Panel(self.notebook_2, -1, style=wx.TAB_TRAVERSAL | wx.FULL_REPAINT_ON_RESIZE)
        self.setupList = ['S6 Craiova','S7 Craiova', '1+96(R4)', 'F2', 'F4', 'F7']
        self.combo_box_setup = wx.ComboBox(self.notebook_2_pane_2, -1, choices=self.setupList,
                                           style=wx.CB_DROPDOWN | wx.CB_DROPDOWN, size=(184, 20))
        self.devicelist = wx.TextCtrl(self.notebook_2_pane_2, pos=(-1, 30), size=(184, 256),
                                      style=wx.TE_MULTILINE | wx.HSCROLL)
        #self.logger = wx.TextCtrl(self.notebook_2_pane_1, pos=(20,220), size=(700,200), style=wx.TE_MULTILINE | wx.TE_READONLY|wx.HSCROLL)
        self.loggerprov = wx.TextCtrl(self.notebook_2_pane_2, pos=(2, 600), size=(900, 300),
                                      style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)

        self.logr = logging.getLogger('')
        self.logr.setLevel(logging.DEBUG)
        hdlr = FuncLog(self.loggerprov)
        #hdlr.setFormatter(logging.Formatter('%(levelname)s | %(name)s |%(message)s [@ %(asctime)s in %(filename)s:%(lineno)d]'))
        hdlr.setFormatter(logging.Formatter('%(levelname)s |%(message)s'))
        self.logr.addHandler(hdlr)

        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.combo_box_setup)
        #self.Bind(wx.EVT_TEXT, self.EvtText,self.combo_box_setup )





        #self.list_box_1.Bind(wx.EVT_LISTBOX, self.OnListBox1Listbox)

        self.lblname = wx.StaticText(self.notebook_2_pane_2, label="TFTP :", pos=(200, 30))
        self.tftp = wx.TextCtrl(self.notebook_2_pane_2, value="172.16.0.215", pos=(250, 30), size=(140, -1),
                                style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
        '''self.lblname = wx.StaticText(self.notebook_2_pane_2, label="Vlans :", pos=(400,30))
        self.groupvlan = wx.TextCtrl(self.notebook_2_pane_2, value="200,300", pos=(450, 30), size=(140,-1),style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)'''
        #self.lblname = wx.StaticText(self.notebook_2_pane_2, label="Services :", pos=(200,60))
        #self.service = wx.TextCtrl(self.notebook_2_pane_2, value="2", pos=(250, 60), size=(140,-1),style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
        self.lblname = wx.StaticText(self.notebook_2_pane_2, label="Vlans :", pos=(200, 60))
        self.servicevlan = wx.TextCtrl(self.notebook_2_pane_2, value="200,300", pos=(250, 60), size=(140, -1),
                                       style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)


        self.lblcommands=wx.StaticText(self.notebook_2_pane_2, label="Additional telnet commands :", pos=(650, 20))
        self.addtcommands = wx.TextCtrl(self.notebook_2_pane_2, pos=(640, 40), size=(200, 100),value="#set sysname RDL",
                              style=wx.TE_MULTILINE | wx.HSCROLL)




        #wx.ComboBox(self.notebook_2_pane_2, -1, choices=self.setupList, style=wx.CB_DROPDOWN | wx.CB_DROPDOWN,size=(184,20))
        self.labeldlubr = wx.StaticText(self.notebook_2_pane_2, label="DL UBR :", pos=(200, 180))
        self.valuedlubr = wx.TextCtrl(self.notebook_2_pane_2, value='23', pos=(250, 180), size=(140, -1),
                                      style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
        self.checkbox_dlubr = wx.CheckBox(self.notebook_2_pane_2, label="", pos=(400, 180))
        self.labelulubr = wx.StaticText(self.notebook_2_pane_2, label="UL UBR :", pos=(450, 180))
        self.valueulubr = wx.TextCtrl(self.notebook_2_pane_2, value='23', pos=(500, 180), size=(140, -1),
                                      style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
        self.checkbox_ulubr = wx.CheckBox(self.notebook_2_pane_2, label="", pos=(650, 180))
        #self.adapt= wx.CheckBox(self.notebook_2_pane_2, label="Adapt_Mod", pos=(200, 120))
        self.adapt = wx.RadioBox(self.notebook_2_pane_2, -1, ("Adaptive Modulation"), (200, 120),
                                 choices=[("ON"), ("OFF"), ("None")], majorDimension=3, style=wx.RA_SPECIFY_COLS)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBoxAdapt, self.adapt)
        #self.button_prov =wx.Button(self.notebook_2_pane_2, label="Create", pos=(200, 90))

        self.lblname = wx.StaticText(self.notebook_2_pane_2, label="DL/UL CIR :", pos=(200, 340))
        self.dlulcir = wx.TextCtrl(self.notebook_2_pane_2, value="50000", pos=(260, 335), size=(50, -1),
                                   style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
        self.checkbox_cir = wx.CheckBox(self.notebook_2_pane_2, label="", pos=(320, 340))

        self.lblname = wx.StaticText(self.notebook_2_pane_2, label="DL/UL PIR :", pos=(340, 340))
        self.dlulpir = wx.TextCtrl(self.notebook_2_pane_2, value="50000", pos=(400, 335), size=(50, -1),
                                   style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
        self.checkbox_pir = wx.CheckBox(self.notebook_2_pane_2, label="", pos=(460, 340))

        self.lblsyslog = wx.StaticText(self.notebook_2_pane_2, label="Syslog:", pos=(500, 340))
        self.text_syslog = wx.TextCtrl(self.notebook_2_pane_2, value="172.16.0.145", pos=(550, 335), size=(80, -1),
                                   style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
        self.checkbox_syslog = wx.CheckBox(self.notebook_2_pane_2, label="", pos=(640, 340))

        self.lblvlan = wx.StaticText(self.notebook_2_pane_2, label="VLAN Filter :", pos=(670, 340))
        self.text_vlan = wx.TextCtrl(self.notebook_2_pane_2, value="0", pos=(735, 335), size=(50, -1),
                                   style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
        self.checkbox_vlan = wx.CheckBox(self.notebook_2_pane_2, label="", pos=(790, 340))

        self.button_prov = wx.Button(self.notebook_2_pane_2, label="Create", pos=(200, 400))
        self.button_prov.Bind(wx.EVT_BUTTON, self.Clickbutton_prov)
        self.button_change = wx.Button(self.notebook_2_pane_2, label="Change", pos=(300, 400))
        self.button_change.Bind(wx.EVT_BUTTON, self.Clickbutton_change)

        self.button_report = wx.Button(self.notebook_2_pane_2, label="Report", pos=(400, 400))
        self.button_report.Bind(wx.EVT_BUTTON, self.Clickbutton_report)

        self.button_upgrade = wx.Button(self.notebook_2_pane_2, label="Upgrade", pos=(400, 450))
        self.button_upgrade.Bind(wx.EVT_BUTTON, self.Clickbutton_upgrade)
        self.text_upgrade = wx.TextCtrl(self.notebook_2_pane_2, value="RDL3KR4_0300_035.sbin", pos=(200, 450), size=(150, -1),
                           style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)

        self.button_chgver = wx.Button(self.notebook_2_pane_2, label="ChangeVersion", pos=(500, 450))
        self.button_chgver.Bind(wx.EVT_BUTTON, self.Clickbutton_chgver)



        self.radio_mode = wx.RadioBox(self.notebook_2_pane_2, -1, ("Radio Mode"), (200, 210),
                                      choices=[_("ON"), ("OFF"), ("None")], majorDimension=3, style=wx.RA_SPECIFY_COLS)
        self.cyclic_prefix = wx.RadioBox(self.notebook_2_pane_2, -1, ("Cyclic Prefix"), (400, 210),
                                         choices=[("1/4"), ("1/8"), ("None")], majorDimension=3,
                                         style=wx.RA_SPECIFY_COLS)
        self.chsize = wx.RadioBox(self.notebook_2_pane_2, -1, _("Channel Size"), (600, 210),
                                  choices=[("0.875"), ("1.25"), ("1.75"), ("2.5"), ("3.5"), ("5"), ("7"), ("10"),
                                           ("14"), ("20"), ("None")], majorDimension=3, style=wx.RA_SPECIFY_COLS)
        self.labelfreq = wx.StaticText(self.notebook_2_pane_2, label="Frequency :", pos=(200, 270))
        self.valuefreq = wx.TextCtrl(self.notebook_2_pane_2, value='3500', pos=(270, 270), size=(140, -1),
                                     style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
        self.checkbox_freq = wx.CheckBox(self.notebook_2_pane_2, label="", pos=(420, 270))

        self.labelsw = wx.StaticText(self.notebook_2_pane_2, label="sw version", pos=(500, 400))
        self.checkbox_sw = wx.CheckBox(self.notebook_2_pane_2, label="", pos=(560, 400))

        self.labelmac = wx.StaticText(self.notebook_2_pane_2, label="mac", pos=(580, 400))
        self.checkbox_mac = wx.CheckBox(self.notebook_2_pane_2, label="", pos=(610, 400))

        self.lblversion = wx.StaticText(self.notebook_2_pane_2, label="Version : 5.2", pos=(2, 580))



        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBoxFreq, self.checkbox_freq)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBoxDlUbr, self.checkbox_dlubr)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBoxULUBR, self.checkbox_ulubr)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBoxCir, self.checkbox_cir)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBoxPir, self.checkbox_pir)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBoxSw, self.checkbox_sw)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBoxMac, self.checkbox_mac)

        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBoxSyslog, self.checkbox_syslog)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBoxVlanFilter, self.checkbox_vlan)


        #self.radio_mode = wx.RadioButton(self.notebook_2_pane_2, -1, _("radio_mode"))
        self.radio_mode.Bind(wx.EVT_BUTTON, self.Clickbutton_change)
        self.cyclic_prefix.Bind(wx.EVT_BUTTON, self.Clickbutton_change)
        self.chsize.Bind(wx.EVT_BUTTON, self.Clickbutton_change)

        self.__set_properties()
        self.__do_layout()
        self.threads=[]
        file = open('Logger_Telnet.txt', "w")
        file.close()

        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle(("Lab Tool"))
        self.SetSize((900, 900))
        self.SetForegroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DDKSHADOW))
        self.radio.SetFocus()
        self.radio.SetValue(1)
        # self.adapt.SetFocus()
        # self.adapt.SetValue(1)
        self.adapt.SetSelection(2)
        self.radio_mode.SetSelection(2)
        self.cyclic_prefix.SetSelection(2)
        self.chsize.SetSelection(10)
        self.valuedlubr
        self.valuedlubr.Disable()
        self.valueulubr.Disable()
        self.valuefreq.Disable()
        self.dlulcir.Disable()
        self.dlulpir.Disable()
        self.text_vlan.Disable()
        self.text_syslog.Disable()



        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1 = wx.GridSizer(4, 3, 0, 0)
        self.notebook_2_pane_1.SetSizer(grid_sizer_1)
        self.notebook_2.AddPage(self.notebook_2_pane_1, ("Services"))
        self.notebook_2.AddPage(self.notebook_2_pane_2, ("Provisioning"))
        sizer_1.Add(self.notebook_2, 1, wx.EXPAND, 0)
        #self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def OnClick(self, event):
        # self.logger.AppendText(" Click on object with Id %d\n" %event.GetId())
        status_radio = ''
        if self.radio.IsChecked():
            status_radio = 'on'
        self.logr.info('Starting to apply values....')
        obj_device=Device.Device.SaveServiceValue(str(self.sector.GetValue()), str(self.dlcir.GetValue()), str(self.ulcir.GetValue()), self.radio.IsChecked(),
            str(self.dlpir.GetValue()), str(self.ulpir.GetValue()))
        self.logr.info('Finish process')

    def getvalues(self):
        self.logr.info('Starting to apply values....')
        items = str(self.devicelist.GetValue())
        list = items.split('\n')
        sc = ''.join(list[0])
        freq = ''
        dlubr = ''
        ulubr = ''
        cp = ''
        chsize = ''
        radio_mode = ''
        adapt = ''
        cir = ''
        pir = ''
        syslog=''
        upgrade_value=''
        vlanfilter=''
        if self.dlulcir.IsEnabled():
            cir = str(self.dlulcir.GetValue())
            self.logr.info('Set CIR')
        if self.dlulpir.IsEnabled():
            pir = str(self.dlulpir.GetValue())
            self.logr.info('Set PIR')
        if self.valuefreq.IsEnabled():
            freq = str(self.valuefreq.GetValue())
            freq = 'set rffreq ' + freq
            self.logr.info('Set Frequency')
        if self.valuedlubr.IsEnabled():
            dlubr = str(self.valuedlubr.GetValue())
            self.logr.info('Set DL UBR')
        if self.valueulubr.IsEnabled():
            ulubr = str(self.valueulubr.GetValue())
            self.logr.info('Set UL UBR')
        if self.cyclic_prefix.GetSelection() != 2:
            if self.cyclic_prefix.GetSelection() == 0:
                cp = 'set cp 0'
            else:
                cp = 'set cp 1'
            self.logr.info('Change cycle prefix')
        if self.radio_mode.GetSelection() != 2:
            if self.radio_mode.GetSelection() == 0:
                radio_mode = 'set radio on'
            else:
                radio_mode = 'set radio off'
            self.logr.info('Set radio mode')
        if self.chsize.GetSelection() != 10:
            if self.chsize.GetSelection() == 0:
                chsize = 'set chwidth 0.875'
            elif self.chsize.GetSelection() == 1:
                chsize = 'set chwidth 1.25'
            elif self.chsize.GetSelection() == 2:
                chsize = 'set chwidth 1.75'
            elif self.chsize.GetSelection() == 3:
                chsize = 'set chwidth 2.5'
            elif self.chsize.GetSelection() == 4:
                chsize = 'set chwidth 3.5'
            elif self.chsize.GetSelection() == 5:
                chsize = 'set chwidth 5'
            elif self.chsize.GetSelection() == 6:
                chsize = 'set chwidth 7'
            elif self.chsize.GetSelection() == 7:
                chsize = 'set chwidth 10'
            elif self.chsize.GetSelection() == 8:
                chsize = 'set chwidth 14'
            elif self.chsize.GetSelection() == 9:
                chsize = 'set chwidth 20'
            self.logr.info('Change channel size')
        if self.text_vlan.IsEnabled():
            vlanfilter = str(self.text_vlan.GetValue())
            vlanfilter = 'set vlanfilter on '+'\n'+'set allowedvlans ' + vlanfilter
            self.logr.info('Set Vlan Filter')
        else:
            vlanfilter = 'set vlanfilter off '+'\n'
            self.logr.info('Set Vlan Filter')
        if self.text_syslog.IsEnabled():
            syslog = str(self.text_syslog.GetValue())
            syslog = 'set syslogip ' + syslog
            self.logr.info('Set Syslog ip address:')

        if self.adapt.GetSelection() != 2:
            if self.adapt.GetSelection() == 0:
                adapt = 'on '
            else:
                adapt = 'off '
            self.logr.info('Set modulation type')
        items = str(self.addtcommands.GetValue())
        listcommands = items.split('\n')


        device = Device.Device(sc, freq, dlubr, ulubr, cp, chsize, radio_mode, adapt, cir, pir, vlanfilter, syslog,listcommands)
        return device

    def Clickbutton_change(self, event):
        items = str(self.devicelist.GetValue())
        list = items.split('\n')
        sc = ''.join(list[0])
        device = self.getvalues()
        #apply only SC
        if self.adapt.GetStringSelection()!="None" or self.checkbox_cir.GetValue() or self.checkbox_pir.GetValue() or self.checkbox_dlubr.GetValue() or self.checkbox_ulubr.GetValue():
            if Device.Device.pingdevice(sc) is not False:
                self.threadradio = threading.Thread(target=device.ChangeLinksValue, args=(device,))
                self.threads.append(self.threadradio)
                self.threadradio.start()
                self.logr.info('Change Links values')
            list.pop(0)
            for ip in list:
                #apply all device
                self.threadradio = threading.Thread(target=device.ChangeDeviceValue, args=(ip, device))
                self.logr.info('Change Device values' + ip)
                self.threads.append(self.threadradio)
                self.threadradio.start()
                #self.threadradio.join()
        else:
            for ip in list:
                #apply all device
                self.threadradio = threading.Thread(target=device.ChangeDeviceValue, args=(ip, device))
                self.logr.info('Change Device values' + ip)
                self.threads.append(self.threadradio)
                self.threadradio.start()
                #self.threadradio.join()



    def Clickbutton_report(self, event):
        #self.threadradio
        
        # result=Device.Device().SaveServiceValue()
        self.logr.info('Creating reports....')
        items = str(self.devicelist.GetValue())
        list = items.split('\n')
        listip = []
        queue = Queue.Queue()

        device = self.getvalues()
        file = open('Report.txt', "w")
        file.close()
        dict_mac = {}
        dict_sw = {}
        for ip in list:
            if self.checkbox_mac.GetValue() is True:
                self.logr.info('Get subscriber mac address for ip '     + ''.join(ip))
                thread1 = threading.Thread(target=Device.Device.getmacss, args=(ip, queue))
                self.threads.append(thread1)
                thread1.start()
                #dict_mac.update({ip:queue.get()})

            if self.checkbox_sw.GetValue() is True:
                self.logr.info('Get subscriber software version for ip '     + ''.join(ip))
                thread2 = threading.Thread(target=Device.Device.getswversion, args=(ip,queue))
                self.threads.append(thread2)
                thread2.start()
        while True:
            item=queue.get(block=True,timeout=10)
            file=open('Report.txt',"a")
            file.write(item+'\n')
            file.close()
            if item is None:
                break



        #dict_sw.update({ip:queue.get()})
        #dict_sw.update({queue.get()})
        #file=open('Report.txt',"a")
        #file.write(queue)
        '''if len(dict_mac)!=0:
            for k,v in dict_mac.items():
                file.write(k+','+v)
        if len(dict_sw)!=0:
            for k,v in dict_sw.items():
                file.write(k+','+v+'\n')'''

    def Clickbutton_upgrade(self, event):
        self.logr.info('Upgrading devices....')
        items = str(self.devicelist.GetValue())

        list = items.split('\n')
        count = 0
        queue = Queue.Queue()
        for ip in list:
            self.logr.info('Upgrade device with ip '     + ''.join(ip))
            thread1 = threading.Thread(target=Device.Device.upgrade, args=(ip,str(self.tftp.GetValue()),str(self.text_upgrade.GetValue())))
            self.threads.append(thread1)
            thread1.start()

    def Clickbutton_chgver(self, event):
        self.logr.info('Change software version................................')
        items = str(self.devicelist.GetValue())
        list = items.split('\n')
        count = 0
        queue = Queue.Queue()

        for ip in list:
            self.logr.info('Change software version for device with ip '     + ''.join(ip))
            thread1 = threading.Thread(target=Device.Device.changeversion, args=(ip,))
            self.threads.append(thread1)
            thread1.start()




    def EvtCheckBoxRadio(self, event):
        if self.radio.GetValue() is False:
            self.radio.SetValue(0)
            event.GetEvent()
            self.logr.info('Radio mode is disabled')
        else:
            self.radio.SetValue(1)
            self.logr.info('Radio mode is enabled')

    def EvtCheckBoxAdapt(self, event):
        if self.adapt.GetValue() is False:
            self.adapt.SetValue(0)
            self.logr.info('Adaptive modulation will be disabled')
        else:
            self.adapt.SetValue(1)
            self.logr.info('Adaptive modulation will be enabled')

    def EvtCheckBoxFreq(self, event):
        if self.checkbox_freq.GetValue() is False:
            self.valuefreq.Disable()
        else:
            self.valuefreq.Enable()
            self.logr.info('Modify frequency value')

    def EvtCheckBoxSyslog(self, event):
        if self.checkbox_syslog.GetValue() is False:
            self.text_syslog.Disable()
        else:
            self.text_syslog.Enable()
            self.logr.info('Modify syslog')

    def EvtCheckBoxVlanFilter(self, event):
        if self.checkbox_vlan.GetValue() is False:
            self.text_vlan.Disable()
        else:
            self.text_vlan.Enable()
            self.logr.info('Modify vlan')


    def EvtCheckBoxDlUbr(self, event):
        if self.checkbox_dlubr.GetValue() is False:
            self.valuedlubr.Disable()
        else:
            self.valuedlubr.Enable()
            self.logr.info('Modify DL UBR')

    def EvtCheckBoxULUBR(self, event):
        if self.checkbox_ulubr.GetValue() is False:
            self.valueulubr.Disable()
        else:
            self.valueulubr.Enable()
            self.logr.info('Modify UL UBR')

    def EvtCheckBoxCir(self, event):
        if self.checkbox_cir.GetValue() is False:
            self.dlulcir.Disable()
        else:
            self.dlulcir.Enable()
            self.logr.info('Modify cir value')

    def EvtCheckBoxPir(self, event):
        if self.checkbox_pir.GetValue() is False:
            self.dlulpir.Disable()
        else:
            self.dlulpir.Enable()
            self.logr.info('Modify pir value')
    def EvtCheckBoxSw(self, event):
        pass
    def EvtCheckBoxMac(self, event):
        pass

    def onEnter(self, event):
        """"""
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER:
            if self.sector.IsModified() is True:
                self.dlcir.SetFocus()
                self.sector.SetModified(False)
            elif self.dlcir.IsModified() is True:
                self.ulcir.SetFocus()
                self.dlcir.SetModified(False)
            elif self.ulcir.IsModified() is True:
                self.dlpir.SetFocus()
                self.ulcir.SetModified(False)
            elif self.dlpir.IsModified() is True:
                self.ulpir.SetFocus()
                self.dlpir.SetModified(False)
            elif self.ulpir.IsModified() is True:
                self.button.SetFocus()
                self.ulpir.SetModified(False)
            else:
                self.button.SetFocus()
                self.OnClick(event)

        event.Skip()

    def EvtComboBox(self, event):
        self.devicelist.Clear()
        self.devicelist.AppendText(Setup.Setup().GetSetupName(self.combo_box_setup.GetStringSelection()))

    def writelog(self, text):
        self.logr.info(text)

    def Clickbutton_prov(self, event):
        self.logr.info('Starting to apply values....')
        listmac = []
        items = str(self.devicelist.GetValue())
        list = items.split('\n')
        listipss = []
        ipup=[]
        count = 0
        queue = Queue.Queue()

        device = self.getvalues()

        for ip in list:
            if count == 0:
                if Device.Device.pingdevice(ip) is not False:
                    st = device.clearid(ip)
                    if st == False:
                        self.logr.info('Telnet session can not be opened ' + ip)
                        break
                    sc = ip
                    count += 1
                    self.logr.info('Recognition of sector controller')
                    continue
            else:
                count += 1
                thread1 = threading.Thread(target=Device.Device.getmac, args=(ip, queue))
                self.threads.append(thread1)
                thread1.start()
                ipup.append(ip)
                self.logr.info('Get subscriber mac address for ip ' + ''.join(ip))
                #thread1.join()
        for x in self.threads:
            x.join()
        list.pop(0)
        sizeq=queue.qsize()
        for ip in range(0, sizeq+1, 1):
            if queue.empty() is False:
                macip = queue.get()
                if macip == '':
                    self.logr.info('Telnet session on device  ' + list[ip] + ' is slow. Maybe device needs a reboot.')
                else:
                    macip = macip.replace('\n', '')
                    if len(macip) > 18:
                        mac = macip[0:17]
                        ip = macip[17:len(macip)]

                        listmac.append(mac)
                        listipss.append(ip)

        self.logr.info('Create elements...')
        # dict = {'Name': 'Zara', 'Age': 7, 'Class': 'First'};
        dict_frame = {'groupvlan': str(self.servicevlan.GetValue()),
                      'servicevlan': str(self.servicevlan.GetValue()),
                      'tftp': str(self.tftp.GetValue()),
                      'dlubr': str(device.dlubr),
                      'ulubr': str(device.ulubr),
                      'modulation': str(device.adapt),
                      'radio': str(device.radio_mode),
                      'cp': str(device.cp),
                      'channel': str(device.chsize),
                      'frequency': str(device.freq),
                      'cir': str(device.cir),
                      'pir': str(device.pir),
                      'vlanfilter':str(device.vlanfilter),
                      'syslog':str(device.syslog)}

        prov = Provision.Provision

        self.logr.info('Create provision ')

        try:
            prov_ok = prov.createProv(sc, len(listmac), listmac, listipss, dict_frame)
            if prov_ok == True:
                #device.ChangeLinksValue(device)
                for ip in reversed(ipup):
                    t = threading.Thread(target=device.ChangeDeviceValue, args=(ip, device))
                    self.threads.append(t)
                    t.start()
                    #self.threads.join()
                self.logr.debug('Finish')
        except:
            self.logr.error('The provision can not be created')


# end of class MyFrame
class MyApp(wx.App):
    def OnInit(self):
        frame_1 = MyFrame(None, -1, "Lab Tool", (-1, -1), (900, 900))
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return 1

# end of class MyApp

if __name__ == "__main__":
    import gettext

    gettext.install("app")  # replace with the appropriate catalog name

    app = MyApp(0)
    app.MainLoop()

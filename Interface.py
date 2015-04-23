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

# begin wxGlade: extracode
# end wxGlade

class FuncLog(logging.Handler):
    def __init__(self, ctrl):
       logging.Handler.__init__(self)
       self.ctrl = ctrl


    def emit(self, record):
       self.ctrl.AppendText(self.format(record)+"\n")


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE ^ (wx.MAXIMIZE | wx.RESIZE_BORDER)
        wx.Frame.__init__(self, *args, **kwds)
        self.notebook_2 = wx.Notebook(self, -1, style=0)
        #pane1
        self.notebook_2_pane_1 = wx.Panel(self.notebook_2, -1, style=wx.TAB_TRAVERSAL | wx.FULL_REPAINT_ON_RESIZE)
          
        self.lblname = wx.StaticText(self.notebook_2_pane_1, label="Sector IP Address :", pos=(20,30))
        self.sector = wx.TextCtrl(self.notebook_2_pane_1, value="10.107.40.1", pos=(150, 30), size=(140,-1),style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)

        self.lblname = wx.StaticText(self.notebook_2_pane_1, label="DL CIR :", pos=(20,60))
        self.dlcir = wx.TextCtrl(self.notebook_2_pane_1, value="50000", pos=(150, 60), size=(140,-1),style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)

        self.lblname = wx.StaticText(self.notebook_2_pane_1, label="UL CIR :", pos=(20,90))
        self.ulcir = wx.TextCtrl(self.notebook_2_pane_1, value="50000", pos=(150, 90), size=(140,-1),style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
        self.radio= wx.CheckBox(self.notebook_2_pane_1, label="Radio OFF-ON", pos=(350, 50))

        self.lblname = wx.StaticText(self.notebook_2_pane_1, label="DL PIR :", pos=(20,120))
        self.dlpir = wx.TextCtrl(self.notebook_2_pane_1, value="50000", pos=(150, 120), size=(140,-1),style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)

        self.lblname = wx.StaticText(self.notebook_2_pane_1, label="UL PIR :", pos=(20,150))
        self.ulpir = wx.TextCtrl(self.notebook_2_pane_1, value="50000", pos=(150, 150), size=(140,-1),style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)


        
        self.logger = wx.TextCtrl(self.notebook_2_pane_1, pos=(20,620), size=(700,200), style=wx.TE_MULTILINE | wx.TE_READONLY|wx.HSCROLL)

        # A button
        self.button =wx.Button(self.notebook_2_pane_1, label="Save", pos=(20, 180))
        
        self.logr = logging.getLogger('')
        self.logr.setLevel(logging.DEBUG)
        hdlr = FuncLog(self.logger)
        #hdlr.setFormatter(logging.Formatter('%(levelname)s | %(name)s |%(message)s [@ %(asctime)s in %(filename)s:%(lineno)d]'))
        hdlr.setFormatter(logging.Formatter('%(levelname)s |%(message)s'))
        self.logr.addHandler(hdlr)
        
        #pan 2
        #self.notebook_2_pane_2 = wx.Panel(self.notebook_2, -1, style=wx.TAB_TRAVERSAL | wx.FULL_REPAINT_ON_RESIZE)
        


        
        self.Bind(wx.EVT_BUTTON, self.OnClick,self.button)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBoxRadio, self.radio)
        self.sector.Bind(wx.EVT_KEY_DOWN, self.onEnter)
        self.dlcir.Bind(wx.EVT_KEY_DOWN, self.onEnter)
        self.ulcir.Bind(wx.EVT_KEY_DOWN, self.onEnter)
        self.dlpir.Bind(wx.EVT_KEY_DOWN, self.onEnter)
        self.ulpir.Bind(wx.EVT_KEY_DOWN, self.onEnter)
        self.button.Bind(wx.EVT_KEY_DOWN, self.onEnter)




        self.notebook_2_pane_2 = wx.Panel(self.notebook_2, -1)
        self.setupList = ['S1 Craiova','S2 Craiova','S3 Craiova','S4 Craiova','S5 Craiova','S6 Craiova','S7 Craiova', '1+80(R4)', '1+80(Mixed)','1+28','F1','F2','F3','F4','F7']
        self.combo_box_setup = wx.ComboBox(self.notebook_2_pane_2, -1, choices=self.setupList, style=wx.CB_DROPDOWN | wx.CB_DROPDOWN,size=(184,20))
        self.devicelist = wx.TextCtrl(self.notebook_2_pane_2, pos=(-1,30), size=(184, 256), style=wx.TE_MULTILINE | wx.HSCROLL)
        #self.logger = wx.TextCtrl(self.notebook_2_pane_1, pos=(20,220), size=(700,200), style=wx.TE_MULTILINE | wx.TE_READONLY|wx.HSCROLL)
        self.loggerprov = wx.TextCtrl(self.notebook_2_pane_2, pos=(2,600), size=(900,300), style=wx.TE_MULTILINE | wx.TE_READONLY|wx.HSCROLL)
        
        self.logr = logging.getLogger('')
        self.logr.setLevel(logging.DEBUG)
        hdlr = FuncLog(self.loggerprov)
        #hdlr.setFormatter(logging.Formatter('%(levelname)s | %(name)s |%(message)s [@ %(asctime)s in %(filename)s:%(lineno)d]'))
        hdlr.setFormatter(logging.Formatter('%(levelname)s |%(message)s'))
        self.logr.addHandler(hdlr)



        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.combo_box_setup )
        #self.Bind(wx.EVT_TEXT, self.EvtText,self.combo_box_setup )
        


        
        
        #self.list_box_1.Bind(wx.EVT_LISTBOX, self.OnListBox1Listbox)

        self.lblname = wx.StaticText(self.notebook_2_pane_2, label="TFTP :", pos=(200,30))
        self.tftp = wx.TextCtrl(self.notebook_2_pane_2, value="172.16.0.215", pos=(250, 30), size=(140,-1),style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
        '''self.lblname = wx.StaticText(self.notebook_2_pane_2, label="Vlans :", pos=(400,30))
        self.groupvlan = wx.TextCtrl(self.notebook_2_pane_2, value="200,300", pos=(450, 30), size=(140,-1),style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)'''
        self.lblname = wx.StaticText(self.notebook_2_pane_2, label="Services :", pos=(200,60))
        self.service = wx.TextCtrl(self.notebook_2_pane_2, value="2", pos=(250, 60), size=(140,-1),style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
        self.lblname = wx.StaticText(self.notebook_2_pane_2, label="Vlans :", pos=(400,60))
        self.servicevlan = wx.TextCtrl(self.notebook_2_pane_2, value="200,300", pos=(450, 60), size=(140,-1),style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)

        #wx.ComboBox(self.notebook_2_pane_2, -1, choices=self.setupList, style=wx.CB_DROPDOWN | wx.CB_DROPDOWN,size=(184,20))
        self.labeldlubr = wx.StaticText(self.notebook_2_pane_2, label="DL UBR :", pos=(200,180))
        self.valuedlubr = wx.TextCtrl(self.notebook_2_pane_2,value='15', pos=(250, 180),size=(140,-1),style= wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
        self.checkbox_dlubr= wx.CheckBox(self.notebook_2_pane_2, label="", pos=(400, 180))
        self.labelulubr = wx.StaticText(self.notebook_2_pane_2, label="UL UBR :", pos=(450,180))
        self.valueulubr = wx.TextCtrl(self.notebook_2_pane_2, value='15', pos=(500, 180), size=(140,-1),style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
        self.checkbox_ulubr= wx.CheckBox(self.notebook_2_pane_2, label="", pos=(650, 180))
        #self.adapt= wx.CheckBox(self.notebook_2_pane_2, label="Adapt_Mod", pos=(200, 120))
        self.adapt = wx.RadioBox(self.notebook_2_pane_2,-1, _("Modulation Type"),(200,120), choices=[_("ON"), _("OFF"), _("None")], majorDimension=3, style=wx.RA_SPECIFY_COLS)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBoxAdapt, self.adapt)
        self.button_prov =wx.Button(self.notebook_2_pane_2, label="Create", pos=(200, 90))
        self.button_prov.Bind(wx.EVT_BUTTON, self.Clickbutton_prov)
        self.button_change =wx.Button(self.notebook_2_pane_2, label="Change", pos=(200, 340))
        self.button_change.Bind(wx.EVT_BUTTON, self.Clickbutton_change)
               
        self.radio_mode = wx.RadioBox(self.notebook_2_pane_2,-1, _("Radio Mode"),(200,210), choices=[_("ON"), _("OFF"), _("None")], majorDimension=3, style=wx.RA_SPECIFY_COLS)
        self.cyclic_prefix = wx.RadioBox(self.notebook_2_pane_2,-1, _("Cyclic Prefix"),(400,210), choices=[_("1/4"), _("1/8"), _("None")], majorDimension=3, style=wx.RA_SPECIFY_COLS)
        self.chsize = wx.RadioBox(self.notebook_2_pane_2,-1, _("Channel Size"),(600,210), choices=[_("0.875"), _("1.25"), _("1.75"), _("2.5"), _("3.5"), _("5"), _("7"), _("10"), _("14"), _("20"), _("None")], majorDimension=3, style=wx.RA_SPECIFY_COLS)
        self.labelfreq = wx.StaticText(self.notebook_2_pane_2, label="Frequency :", pos=(200,270))
        self.valuefreq = wx.TextCtrl(self.notebook_2_pane_2,value='3500', pos=(270, 270),size=(140,-1),style= wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
        self.checkbox_freq= wx.CheckBox(self.notebook_2_pane_2, label="", pos=(420, 270))

        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBoxFreq, self.checkbox_freq)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBoxDlUbr, self.checkbox_dlubr)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBoxULUBR, self.checkbox_ulubr)


        #self.radio_mode = wx.RadioButton(self.notebook_2_pane_2, -1, _("radio_mode"))
        self.radio_mode.Bind(wx.EVT_BUTTON, self.Clickbutton_change)
        self.cyclic_prefix.Bind(wx.EVT_BUTTON, self.Clickbutton_change)
        self.chsize.Bind(wx.EVT_BUTTON, self.Clickbutton_change)

        



        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle(_("Lab Tool"))
        self.SetSize((900, 900))
        self.SetForegroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DDKSHADOW))
        self.radio.SetFocus()
        self.radio.SetValue(1)
        #self.adapt.SetFocus()
        #self.adapt.SetValue(1)
        self.adapt.SetSelection(2)
        self.radio_mode.SetSelection(2)
        self.cyclic_prefix.SetSelection(2)
        self.chsize.SetSelection(10)
        self.valuedlubr
        self.valuedlubr.Disable()
        self.valueulubr.Disable()
        self.valuefreq.Disable()


        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1 = wx.GridSizer(4, 3, 0, 0)
        self.notebook_2_pane_1.SetSizer(grid_sizer_1)
        self.notebook_2.AddPage(self.notebook_2_pane_1, _("Services"))
        self.notebook_2.AddPage(self.notebook_2_pane_2, _("Provisioning"))
        sizer_1.Add(self.notebook_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade
    def OnClick(self,event):
        #self.logger.AppendText(" Click on object with Id %d\n" %event.GetId())
        status_radio=''
        if self.radio.IsChecked(): 
            status_radio='on'
        self.logr.info('Starting to apply values....')
        self.thread = threading.Thread(target=Device.Device().SaveServiceValue, args=(str(self.sector.GetValue()),str(self.dlcir.GetValue()),str(self.ulcir.GetValue()),self.radio.IsChecked(),str(self.dlpir.GetValue()),str(self.ulpir.GetValue())))
        self.thread.start()
        #result=Device.Device().SaveServiceValue()
        self.logr.info('Finish process')
        
    def Clickbutton_change(self,event):
        adapt_status=''
        self.logr.info('Starting to apply values....')
        items=str(self.devicelist.GetValue())
        list=items.split('\n')
        sc=''.join(list[0])
        freq=''
        dlubr=''
        ulubr=''
        cp=''
        chsize=''
        radio_mode=''
        adapt=''
        if self.valuefreq.IsEnabled():
            freq=str(self.valuefreq.GetValue())
            freq='set rffreq '+freq
            self.logr.info('Change Frequency')
        if self.valuedlubr.IsEnabled():
            dlubr=str(self.valuedlubr.GetValue())
            self.logr.info('Change DL UBR')
        if self.valueulubr.IsEnabled():
            ulubr=str(self.valueulubr.GetValue())
            self.logr.info('Change UL UBR')
        if self.cyclic_prefix.GetSelection()!=2:
            if self.cyclic_prefix.GetSelection()==0:
                cp='set cp 0'
            else:
                cp='set cp 1'
            self.logr.info('Change cycle prefix')
        if self.chsize.GetSelection()!=10:
            if self.chsize.GetSelection()==0:
                chsize='set chwidth 0.875'
            elif self.chsize.GetSelection()==1:
                chsize='set chwidth 1.25'
            elif self.chsize.GetSelection()==2:
                chsize='set chwidth 1.75'
            elif self.chsize.GetSelection()==3:
                chsize='set chwidth 2.5'
            elif self.chsize.GetSelection()==4:
                chsize='set chwidth 3.5'
            elif self.chsize.GetSelection()==5:
                chsize='set chwidth 5'
            elif self.chsize.GetSelection()==6:
                chsize='set chwidth 7'
            elif self.chsize.GetSelection()==7:
                chsize='set chwidth 10'
            elif self.chsize.GetSelection()==8:
                chsize='set chwidth 14'
            elif self.chsize.GetSelection()==9:
                chsize='set chwidth 20'
            self.logr.info('Change channel size')

            
        if self.adapt.GetSelection()!=2:
            if self.adapt.GetSelection()==0:
                adapt='on '
            else:
                adapt='off '
            self.logr.info('Modify modulation type')

        Device.Device().ChangeLinksValue(sc,dlubr,ulubr,adapt)
        count=0
        if self.radio_mode.GetSelection()!=2:
            if self.radio_mode.GetSelection()==0:
                radio_mode='on'
            else:
                radio_mode='off'

        for ip in reversed(list):
            self.threadradio = threading.Thread(target=Device.Device().ChangeDeviceValue, args=(ip, radio_mode,freq,cp,chsize))
            self.threadradio.start()


        #result=Device.Device().SaveServiceValue()
        self.logr.info('Finish process')

        
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

    def writelog(self,text):
        self.logr.info(text)
    
    def Clickbutton_prov(self,event):
        self.logr.info('Starting to apply values....')
        threads = []
        listmac = []
        items=str(self.devicelist.GetValue())
        list=items.split('\n')
        listipss=[]
        count=0
        queue = Queue.Queue()

            

        for ip in list:
            if count==0:
                #swver=Device.Device().getswversion(ip)
                st=Device.Device().clearid(ip)
                sc=ip
                count+=1
                self.logr.info('Recognition of sector controller')
                continue
            else:

                count+=1
                self.logr.info('Get subscriber mac address for ip '+''.join(ip))

                thread1 = threading.Thread(target=Device.Device().getmac, args=(ip, queue))
                threads.append(thread1)
                #thread1.setDaemon(True)
                thread1.start()
                #thread1.join()
                #thread2 = threading.Thread(target=Device.Device().getip, args=(ip, queue_ip))
                #thread2.start()

        for ip in range(1,len(list),1):
                macip = queue.get()
                if macip=='':
                    self.logr.info('Device  is not up '+list[ip]+'. The ip has been ignored')
                else:
                    macip=macip.replace('\n','')
                    if len(macip)>18:
                        mac=macip[0:17]
                        ip=macip[17:len(macip)]
                        
                        listmac.append(mac)  
                        listipss.append(ip)  

                #thread2 = threading.Thread(target=Device.Device().getip, args=(ip, my_queue))
                #threads.append(thread2)
                #thread2.setDaemon(True)
                #thread2.start()
                #thread2.join()
                #ipss = my_queue.get()
                #listipss.append(ipss) 
        self.logr.info('Create elements...')
        dict = {'Name': 'Zara', 'Age': 7, 'Class': 'First'};
        dict_frame={'group':int(self.service.GetValue()),
                    'service':int(self.service.GetValue()),
                    'groupvlan':str(self.servicevlan.GetValue()),
                    'servicevlan':str(self.servicevlan.GetValue()),
                    'tftp':str(self.tftp.GetValue()),
                    'dlubr':str(self.valuedlubr.GetValue()),
                    'ulubr':str(self.valueulubr.GetValue())}
        #MyFrame(None, -1, "Lab Tool", (-1,-1), (600,600))
        #thread_prov = threading.Thread(target=Provision.Provision().createProv, args=(sc,len(listmac), listmac,listipss,int(self.service.GetValue()),int(self.service.GetValue()),str(self.servicevlan.GetValue()),str(self.servicevlan.GetValue()),str(self.tftp.GetValue())))
        thread_prov = threading.Thread(target=Provision.Provision().createProv, args=(sc,len(listmac),listmac,listipss,dict_frame))
        thread_prov.start()
        #Provision.Provision().createProv(sc,len(listmac), listmac,listipss,int(self.service.GetValue()),int(self.service.GetValue()),str(self.servicevlan.GetValue()),str(self.servicevlan.GetValue()),str(self.tftp.GetValue()))
        self.logr.info('Finish') 

        



# end of class MyFrame
class MyApp(wx.App):
    def OnInit(self):
        frame_1 = MyFrame(None, -1, "Lab Tool", (-1,-1), (900,900))
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return 1

# end of class MyApp

if __name__ == "__main__":
    import gettext
    gettext.install("app") # replace with the appropriate catalog name

    app = MyApp(0)
    app.MainLoop()
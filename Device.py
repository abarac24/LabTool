import wx
import TelnetController
import re
import os
import telnetlib
import logging
import Interface
import Queue
import time
import time
import sys
from threading import Thread


class Device:
    
        
    def SaveServiceValue(self,sector,dlcir,ulcir,statusradio,dlpir,ulpir):
        
        
        
        num=sector
        response = os.system("ping " +num.rstrip()+ " -n 1")
        if response != 0:
            return False


        telnet = TelnetController.TelnetController(host_name = num.rstrip(), user_name = 'admin', password = 'admin', prompt = '#')
        telnet.login()
        cmd=''
        list_id=[]
        while len(list_id)<5:
            list_id=telnet.run_command('show idtable',1).splitlines()
        
        services=self.getserviceid(list_id)
        if statusradio is True:
            cmd='set radio off'+'\n'+'save config'+'\n'
        telnet.run_command(cmd,0)
        cmd=''
        for i in services:
            cmd= cmd+'set dlcir '+''.join(i)+' '+dlcir+'\n'+'set ulcir '+''.join(i)+' '+ulcir+'\n'+'set dlpir '+''.join(i)+' '+dlpir+'\n'+'set ulpir '+''.join(i)+' '+ulpir+'\n'
        telnet.run_command(cmd,0)
        cmd=''
        if statusradio is True:
            cmd='set radio on'+'\n'+'save config'+'\n'
        telnet.run_command(cmd,0)
        telnet.logout()
        
        return True
    
    def getserviceid(self,listid):
        list_service=[]
        for element in listid:
            st=''.join(element)
            if st.find('Service')!=-1:
                st = re.findall('[\s][\s]\d{3}', st)
                list_service.append(st)
        return list_service

    def getlinkid(self,listid):
        list_service=[]
        for element in listid:
            st=''.join(element)
            if st.find('Link')!=-1:
                st = re.findall('[\s]\d{1,3}[\s]', st)
                list_service.append(st)
        return list_service
    
    def getswversion(self,num):
        telnet = TelnetController.TelnetController(host_name = num.rstrip(), user_name = 'admin', password = 'admin', prompt = '#')
        telnet.login()
        sw=''
        while len(sw)==0:
            sw=telnet.run_command('get swver',1).splitlines()
        startindex=''.join(sw).rfind('=')
        sw = ''.join(sw)[startindex+1:startindex+4]
        telnet.logout()
        return sw
    def getmac(self,num,out_queue):
        response = os.system("ping " +num.rstrip()+ " -n 2")
        if response != 0:
            print('Error: Device is not up  '+num+'\n')
            out_queue.put('')
            return
        
        telnet = TelnetController.TelnetController(host_name = num.rstrip(), user_name = 'admin', password = 'admin', prompt = '#')
        telnet.login()
        maclist=''
        while(len(maclist)<11):
            maclist=telnet.run_command('get mac',1)

        #time.sleep(1)
        startindex=''.join(maclist).rfind('=')
        endindex=len(''.join(maclist))
        mac = ''.join(maclist)[startindex+1:endindex]
        telnet.logout()
        out_queue.put(mac.replace(' ', '')+num.rstrip())
        #return mac
            
    def clearid(self,num):
        telnet = TelnetController.TelnetController(host_name = num.rstrip(), user_name = 'admin', password = 'admin', prompt = '#')
        status_login=telnet.login()
        if status_login==False:
            print('Error: Unable to start a telnet session on device  '+num+'\n')
            return False

        telnet.run_command('clear idtable',0)
        telnet.run_command('save config',0)

        
        telnet.logout()
        return True
    #ChangeValue, args=(self.radio.IsChecked(),str(self.valuedlubr.GetValue()),str(self.valueulubr.GetValue())
                       
    def ChangeLinksValue(self,sector,dlubr,ulubr,statusadapt):
        
        
        num=sector
        response = os.system("ping " +num.rstrip()+ " -n 1")
        if response != 0:
            return False


        telnet = TelnetController.TelnetController(host_name = num.rstrip(), user_name = 'admin', password = 'admin', prompt = '#')
        telnet.login()
        cmd=''
        list_id=[]
        while len(list_id)<5:
            list_id=telnet.run_command('show idtable',1).splitlines()
        
        links=self.getlinkid(list_id)
        for i in links:
            if statusadapt!='':
                cmd=cmd+'set adaptmod '+''.join(i)+' '+statusadapt+'\n'
            #telnet.run_command(cmd,0)
            if dlubr!='':    
                cmd= cmd+'set dlrate '+''.join(i)+' '+dlubr+'\n'
            if ulubr!='':    
                cmd= cmd+'set ulrate '+''.join(i)+' '+ulubr+'\n'
        if statusadapt!='' or dlubr!='' or ulubr!='':
            telnet.run_command(cmd+'save config'+'\n',0)
        telnet.logout()
        return True

    def ChangeDeviceValue(self,ip,radio_status,freq,cp,chsize):
        telnet = TelnetController.TelnetController(host_name = ip.rstrip(), user_name = 'admin', password = 'admin', prompt = '#')
        telnet.login()
        cmd=''
        if radio_status!= '':
            cmd=cmd+'set radio '+radio_status+'\r\n'
        if freq!='':
            cmd=cmd+' '+freq+'\r\n'
        if cp!='':
            cmd=cmd+' '+cp+'\r\n'
        if chsize!='':
            cmd=cmd+' '+chsize+'\r\n'
        if radio_status!='' or cp=='' or chsize=='':
            telnet.run_command(cmd+'save config'+'\r\n',0)

        
    def getip(self,num,out_queue):
        telnet = TelnetController.TelnetController(host_name = num.rstrip(), user_name = 'admin', password = 'admin', prompt = '#')
        telnet.login()
        iplist=telnet.run_command('set ipaddr',1).splitlines()
        startindex=''.join(iplist).rfind('=')
        endindex=len(''.join(iplist))
        ip = ''.join(iplist)[startindex+1:endindex]
        telnet.logout()
        out_queue.put(ip)
        return ip   
    

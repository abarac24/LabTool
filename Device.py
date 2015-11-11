import re
import os
import logging

import TelnetController


class Device(object):
    def __init__(self, sc, freq, dlubr, ulubr, cp, chsize, radio_mode, adapt,cir,pir,vlanfilter,syslog):
        self.sc = sc
        self.freq = freq
        self.dlubr = dlubr
        self.ulubr = ulubr
        self.cp = cp
        self.chsize = chsize
        self.radio_mode = radio_mode
        self.adapt = adapt
        self.cir=cir
        self.pir=pir
        self.vlanfilter=vlanfilter
        self.syslog=syslog
    @classmethod
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

        services=Device.getserviceid(list_id)
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
    @classmethod
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
            if st.find('Link') != -1 or st.find('L_Template') != -1 or st.find('L_Derived') != -1:# TODO sortare linkuri in functie de ip-uri
                st = re.findall('[\s]\d{1,3}[\s]', st)
                list_service.append(st)
        return list_service

    @classmethod
    def getswversion(self,num,user,pasw, out_queue):
        telnet = TelnetController.TelnetController(host_name = num.rstrip(), user_name = user, password = pasw, prompt = '#')
        telnet.login()
        sw=''
        while len(sw)==0:
            sw=telnet.run_command('get swver',1).splitlines()
        startindex=''.join(sw).rfind('=')
        endindex=''.join(sw).rfind(')')
        sw = ''.join(sw)[startindex+1:endindex+1]
        telnet.logout()
        out_queue.put(num.rstrip()+','+sw.replace(' ', ''))
        return sw

    @classmethod
    def getmac(self,num,user,pasw, out_queue):
        response = os.system("ping " +num.rstrip()+ " -n 2")
        if response != 0:
            print('Error: Device is not up  '+num+'\n')
            out_queue.put('')
            return

        telnet = TelnetController.TelnetController(host_name = num.rstrip(), user_name = user, password = pasw, prompt = '#')
        telnet.login()
        maclist=''
        while(len(maclist)<11):
            maclist=telnet.run_command('get mac',1)
            print maclist

        #time.sleep(1)
        startindex=''.join(maclist).rfind('=')
        endindex=len(''.join(maclist))
        #mac = ''.join(maclist)[startindex+1:endindex]
        mac = ''.join(maclist)[startindex+1:endindex]
        telnet.logout()
        #out_queue.put(mac.replace(' ', ''))
        out_queue.put(mac.replace(' ', '')+num.rstrip())
        print "get mac for ip: "+num
        #return mac

    @classmethod
    def getmacss(self,num,user,pasw, out_queue):
        response = os.system("ping " +num.rstrip()+ " -n 2")
        if response != 0:
            print('Error: Device is not up  '+num+'\n')
            out_queue.put('')
            return

        telnet = TelnetController.TelnetController(host_name = num.rstrip(), user_name = user, password = pasw, prompt = '#')
        telnet.login()
        maclist=''
        while(len(maclist)<11):
            maclist=telnet.run_command('get mac',1)
            print maclist

        #time.sleep(1)
        startindex=''.join(maclist).rfind('=')
        endindex=len(''.join(maclist))
        mac = ''.join(maclist)[startindex+1:endindex]
        #mac = ''.join(maclist)[startindex+1:endindex]
        telnet.logout()
        out_queue.put(num.rstrip()+','+mac.replace(' ', '').replace('\n',''))
        print "get mac for ip: "+num
        return mac

    def clearid(self,num):
        telnet = TelnetController.TelnetController(host_name = num.rstrip(), user_name = 'admin', password = 'admin', prompt = '#')
        status_login=telnet.login()
        if not status_login:
            print('Error: Unable to start a telnet session on device  '+num+'\n')
            return False

        telnet.run_command('clear idtable',0)
        telnet.run_command('save config',0)


        telnet.logout()
        return True
    #ChangeValue, args=(self.radio.IsChecked(),str(self.valuedlubr.GetValue()),str(self.valueulubr.GetValue())

    def ChangeLinksValue(self, device):


        num = device.sc
        user='admin'
        pasw='admin'
        if num.find(',') != -1:
            cred=num.split(',')
            user=cred[1]
            pasw=cred[2]
            num=num[0:num.find(',')]
        response = os.system("ping " +num.rstrip()+ " -n 1")
        if response != 0:
            return False
        telnet = TelnetController.TelnetController(host_name = num.rstrip(), user_name = user, password = pasw, prompt = '#')
        telnet.login()
        cmd=''
        list_id=[]
        count=0
        while len(list_id)<5:
            list_id=telnet.run_command('show idtable',1).splitlines()
            '''count+=1
            if count>10:
                print('Your idtable is incomplete(i.e. services missing)')
                break'''
        links=self.getlinkid(list_id)
        services=self.getserviceid(list_id)
        for i in links:
            if device.adapt != '':
                cmd = cmd + 'set adaptmod ' + ''.join(i) + ' ' + device.adapt + '\n'
            #telnet.run_command(cmd,0)
            if device.dlubr != '':
                cmd = cmd + 'set dlrate ' + ''.join(i) + ' ' + device.dlubr + '\n'
            if device.ulubr != '':
                cmd = cmd + 'set ulrate ' + ''.join(i) + ' ' + device.ulubr + '\n'
            if device.pir != '':
                cmd = cmd + 'set ldlpir ' + ''.join(i) + ' ' + device.pir + '\n'
                cmd = cmd + 'set lulpir ' + ''.join(i) + ' ' + device.pir + '\n'
        for i in services:
            if device.cir != '':
                cmd = cmd + 'set dlcir ' + ''.join(i) + ' ' + device.cir + '\n'
                cmd = cmd + 'set ulcir ' + ''.join(i) + ' ' + device.cir + '\n'
            if device.pir != '':
                cmd = cmd + 'set dlpir ' + ''.join(i) + ' ' + device.pir + '\n'
                cmd = cmd + 'set ulpir ' + ''.join(i) + ' ' + device.pir + '\n'
        if device.adapt != '' or device.dlubr != '' or device.ulubr != '' or device.cir != '' or device.pir != '':
            print "change links value according this command"+cmd
            telnet.run_command(cmd+'set radio off'+'\n',0)
            telnet.run_command(cmd+'set radio on'+'\n',0)
            telnet.run_command(cmd+'save config'+'\n',0)
        #telnet.run_command('logout',0)
        if device.radio_mode != '':
            cmd = cmd + ' ' + device.radio_mode + '\r\n'
        if device.freq != '':
            cmd = cmd + ' ' + device.freq + '\r\n'
        if device.cp != '':
            cmd = cmd + ' ' + device.cp + '\r\n'
        if device.chsize != '':
            cmd = cmd + ' ' + device.chsize + '\r\n'
        if device.vlanfilter != '':
            cmd = cmd + ' ' + device.vlanfilter + '\r\n'
        if device.syslog != '':
            cmd = cmd + ' ' + device.syslog + '\r\n'
        if device.vlanfilter != '':
            cmd = cmd + ' ' + device.vlanfilter + '\r\n'
        if device.radio_mode != '' or device.cp == '' or device.chsize == '':
            telnet.run_command(cmd+'save config'+'\r\n',0)
        telnet.run_command('logout',0)
        return True

    def ChangeDeviceValue(self,ip, device,user,pasw):
        num = ip
        response = os.system("ping " +ip.rstrip()+ " -n 1")
        if response != 0:
            print "Device is not found:"
            return False
        telnet = TelnetController.TelnetController(host_name = ip.rstrip(), user_name = user, password = pasw, prompt = '#')
        st=telnet.login()
        if st==False:
            print "Device can not reachable on telnet:"
            return False
        cmd=''
        if device.radio_mode != '':
            cmd = cmd + ' ' + device.radio_mode + '\r\n'
        if device.freq != '':
            cmd = cmd + ' ' + device.freq + '\r\n'
        if device.cp != '':
            cmd = cmd + ' ' + device.cp + '\r\n'
        if device.chsize != '':
            cmd = cmd + ' ' + device.chsize + '\r\n'
        if device.vlanfilter != '':
            cmd = cmd + ' ' + device.vlanfilter + '\r\n'
        if device.syslog != '':
            cmd = cmd + ' ' + device.syslog + '\r\n'
        if device.vlanfilter != '':
            cmd = cmd + ' ' + device.vlanfilter + '\r\n'
        if device.radio_mode != '' or device.cp == '' or device.chsize == '':
            telnet.run_command(cmd+'save config'+'\r\n',0)
        telnet.run_command('logout',0)



    def getip(self,num, out_queue):
        telnet = TelnetController.TelnetController(host_name = num.rstrip(), user_name = 'admin', password = 'admin', prompt = '#')
        telnet.login()
        iplist=telnet.run_command('set ipaddr',1).splitlines()
        startindex=''.join(iplist).rfind('=')
        endindex=len(''.join(iplist))
        ip = ''.join(iplist)[startindex+1:endindex]
        telnet.logout()
        out_queue.put(ip)
        return ip
    def setCredentials(self,ip):
            user='admin'
            pasw='admin'
            if ip.find(',') != -1:
                cred=ip.split(',')
                user=cred[1]
                pasw=cred[2]
                ip=ip[0:ip.find(',')]
            return ip
    

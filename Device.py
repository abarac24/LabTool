import re
import os

import TelnetController


class Device:
    def __init__(self, sc, freq, dlubr, ulubr, cp, chsize, radio_mode, adapt):
        self.sc = sc
        self.freq = freq
        self.dlubr = dlubr
        self.ulubr = ulubr
        self.cp = cp
        self.chsize = chsize
        self.radio_mode = radio_mode
        self.adapt = adapt


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
            list_id = telnet.run_command('show idtable',
                                         1).splitlines()  # TODO: In cazul in care nu exista linkuri userul trebuie avertizat
        
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

    @staticmethod
    def getserviceid(listid):
        list_service=[]
        for element in listid:
            st=''.join(element)
            if st.find('Service')!=-1:
                st = re.findall('[\s][\s]\d{3}', st)
                list_service.append(st)
        return list_service

    @staticmethod
    def getlinkid(listid):
        list_service=[]
        for element in listid:
            st=''.join(element)
            if st.find('Link') != -1:  # TODO this step should be implemented also for templeate links.
                st = re.findall('[\s]\d{1,3}[\s]', st)
                list_service.append(st)
        return list_service

    @staticmethod
    def getswversion(num):
        telnet = TelnetController.TelnetController(host_name = num.rstrip(), user_name = 'admin', password = 'admin', prompt = '#')
        telnet.login()
        sw=''
        while len(sw)==0:
            sw=telnet.run_command('get swver',1).splitlines()
        startindex=''.join(sw).rfind('=')
        sw = ''.join(sw)[startindex+1:startindex+4]
        telnet.logout()
        return sw

    @staticmethod
    def getmac(num, out_queue):
        response = os.system("ping " +num.rstrip()+ " -n 2")
        if response != 0:
            print('Error: Device is not up  '+num+'\n')
            out_queue.put('')
            return
        
        telnet = TelnetController.TelnetController(host_name = num.rstrip(), user_name = 'admin', password = 'admin', prompt = '#')
        telnet.login()
        maclist=''
        while len(maclist) < 11:
            maclist=telnet.run_command('get mac',1)

        #time.sleep(1)
        startindex=''.join(maclist).rfind('=')
        endindex=len(''.join(maclist))
        mac = ''.join(maclist)[startindex+1:endindex]
        telnet.logout()
        out_queue.put(mac.replace(' ', '')+num.rstrip())
        #return mac

    @staticmethod
    def clearid(num):
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
            if device.adapt != '':
                cmd = cmd + 'set adaptmod ' + ''.join(i) + ' ' + device.adapt + '\n'
            #telnet.run_command(cmd,0)
            if device.dlubr != '':
                cmd = cmd + 'set dlrate ' + ''.join(i) + ' ' + device.dlubr + '\n'
            if device.ulubr != '':
                cmd = cmd + 'set ulrate ' + ''.join(i) + ' ' + device.ulubr + '\n'
        if device.adapt != '' or device.dlubr != '' or device.ulubr != '':
            telnet.run_command(cmd+'save config'+'\n',0)
        telnet.logout()
        return True

    @staticmethod
    def ChangeDeviceValue(ip, device):
        telnet = TelnetController.TelnetController(host_name = ip.rstrip(), user_name = 'admin', password = 'admin', prompt = '#')
        telnet.login()
        cmd=''
        if device.radio_mode != '':
            cmd = cmd + 'set radio ' + device.radio_mode + '\r\n'
        if device.freq != '':
            cmd = cmd + ' ' + device.freq + '\r\n'
        if device.cp != '':
            cmd = cmd + ' ' + device.cp + '\r\n'
        if device.chsize != '':
            cmd = cmd + ' ' + device.chsize + '\r\n'
        if device.radio_mode != '' or device.cp == '' or device.chsize == '':
            telnet.run_command(cmd+'save config'+'\r\n',0)


    @staticmethod
    def getip(num, out_queue):
        telnet = TelnetController.TelnetController(host_name = num.rstrip(), user_name = 'admin', password = 'admin', prompt = '#')
        telnet.login()
        iplist=telnet.run_command('set ipaddr',1).splitlines()
        startindex=''.join(iplist).rfind('=')
        endindex=len(''.join(iplist))
        ip = ''.join(iplist)[startindex+1:endindex]
        telnet.logout()
        out_queue.put(ip)
        return ip   
    

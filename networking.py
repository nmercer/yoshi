import subprocess
import sqlite3
from database import Database

class Networking(object):
    # Todo - Add date_updated to mac list and bumb it here based on when it was seen
    def check_macs(self):
        macs = self.get_mac_list()
        for mac in macs:
            ip = self.mac_to_ip(mac[0])
            if ip:
                if self.ip_up(ip):
                    return mac[0]
        return None

    # Sort by date_seen
    def get_mac_list(self):
        db = Database('network.db')
        db.check('CREATE TABLE Macs (mac);')
        return db.fetch('SELECT * From Macs')

    def remove_by_ip(self, ip):
        mac = self.ip_to_mac(ip)
        if not mac:
            return False

        db = Database('network.db')
        db.check('CREATE TABLE Macs (mac);')
        if db.exists("SELECT * FROM Macs WHERE mac='%s';" % mac):
            pass # Todo - Write db delete function

    def register_by_ip(self, ip):
        mac = self.ip_to_mac(ip)

        if not mac:
            return False

        db = Database('network.db')
        db.check('CREATE TABLE Macs (mac);')
        if not db.exists("SELECT * FROM Macs WHERE mac='%s';" % mac):
            db.insert("INSERT INTO Macs (mac) VALUES('%s')" % mac)

        return mac

    def ip_up(self, ip):
        batcmd = "nmap -sn %s" % ip
        nmap = subprocess.check_output(batcmd, shell=True)
        if nmap.find('host up') >= 0:
            return True
        return False

    def mac_to_ip(self, mac):
        arpcmd="arp -a -n"
        arp = subprocess.check_output(arpcmd, shell=True)
        arp_num = arp.find(mac)

        if arp_num < 0:
            return False

        ip_found = False
        ip = ''
        ip_record = False

        while not ip_found:
            if arp[arp_num] == ')':
                ip_record = True
            elif arp[arp_num] == '(':
                ip_found = True
            elif ip_record:
                ip = arp[arp_num] + ip
            elif arp_num < 0:
                return False
            arp_num -= 1

        return ip

    def ip_to_mac(self, ip):
        arpcmd="arp -a -n"
        arp = subprocess.check_output(arpcmd, shell=True)
        arp_num = arp.find('(' + ip + ')')

        if arp_num < 0:
            return False

        mac = ''

        while True:
            try:
                if arp[arp_num] == 'a':
                    return arp[arp_num+3:arp_num+20]
            except:
                return False

            arp_num += 1


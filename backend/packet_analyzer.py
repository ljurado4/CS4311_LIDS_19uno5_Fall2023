# File: packet_analyzer.py
#
# Description:
#
# @ Author: Alejandro Hernandez
# @ Modifier: Lizbeth Jurado


from . import ipChecker, alerts_manager, loginCheck, PortChecker
from datetime import datetime
import pyshark
import threading
from threading import Semaphore
class PacketAnalyzer:
    sem = Semaphore(1)
    def __init__(self):
        self.loginCheck = loginCheck.LoginCheck()
        self.packetAnalyzer = None
        self.iC = ipChecker.ip_Checker()
        self.getAlerts = alerts_manager.AlertManager()
        self.portCheck = PortChecker.portDetection()

# @ Author: Alejandro Hernandez
# Receives packet data and calls methods to check if packet should cause an alert
    def analyze_packet(self, packet, time, identifier, sourceIP, sourcePort,destIP,destPort,protocol,handshake):

        if self.login_attempts(packet,protocol,destPort,time) == True:
            self.create_alert(packet, time, identifier, 3, sourceIP, sourcePort,destIP,destPort,"Failed Login Error","Multiple failed logins detected")
            print("Failed login")

        if self.ip_check(sourceIP) == False:

            res = self.port_scan_check(sourceIP, destPort, time, handshake)
            if res == "threshold1":
                self.create_alert(packet, time, identifier, 2, sourceIP, sourcePort,destIP,destPort,"Port Scan Error","Port Scan surpassing threshold1")
                print("Port Checker")
        if self.ip_check(sourceIP) == False:
            self.create_alert(packet, time, identifier, 1, sourceIP, sourcePort,destIP,destPort,"Unknown IP Error","Source IP detected that is not appart of approved IP list")
            

# @ Author: Alejandro Hernandez
# Calls method to check if packet contains unknown ip returns false if alert should be created
    def ip_check(self, IP):
        # print("IP check ",IP)
        return self.iC.ip_in_List(IP)

# @ Author: Alejandro Hernandez
# calls method to check if a port scan has occured, will return "threshold1" if alert should be created, creates destination threshold and time threshold
    def port_scan_check(self, IP, destPort, time, handshake):
        threshold1 = 500
        timeAllowed = 700
        timeOF = datetime.strptime(time,"%Y-%m-%d %H:%M:%S.%f")
        # print("Reach")
        # print("port_scan_check")
        if handshake == True:
            # print("handshake")
            return self.portCheck.port_Checking(IP, destPort, timeOF, timeAllowed, threshold1)
    
# @ Author: Alejandro Hernandez
# calls method to check if a mutiple failed login alerts should be created returns true if an alert should be created, creates time threshold 
    def login_attempts(self, packet,protocol,destPort,time):
        threshold = 700
        timeOF = datetime.strptime(time,"%Y-%m-%d %H:%M:%S.%f")
        return self.loginCheck.failedPssWrd(packet,protocol,timeOF,destPort,threshold)

# @ Author: Alejandro Hernandez
    
    def create_alert(self, packet, time, identifier, level, sourceIP, sourcePort,destIP,destPort,typeAlert,description):
        # Capture PCAP data as a string from the packet
        pcap_data = str(packet)
        # Call the AlertsManager class to create an alert
        self.getAlerts.create_alert(pcap_data,time, identifier, level, sourceIP, sourcePort,destIP,destPort,typeAlert,description)
        self.getAlerts.ident_list(pcap_data, identifier)
        alerts = self.getAlerts.get_alerts()

# @ Author: Lizbeth Jurado
    def read_pcap(self, pcap_file_path):
        try:
            # Open the pcap file with FileCapture
            cap = pyshark.FileCapture(pcap_file_path, only_summaries=True)
            packets_data = []

            for packet in cap:
                # Process each packet into a dictionary
                packet_dict = {
                    'number': packet.no,
                    'time': packet.time,
                    'source': packet.source,
                    'destination': packet.destination,
                    'protocol': packet.protocol,
                    'length': packet.length,
                    'info': packet.info
                }
                packets_data.append(packet_dict)

            cap.close()
            return packets_data

        except Exception as e:
            print(f"An error occurred while reading the pcap file: {e}")
            return []

    # format_for_frontend method
    def format_for_frontend(self, packet_data):
        # Convert packet data to JSON
        return json.dumps(packet_data)

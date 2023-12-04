# File: packet_capture.py
#
# Description: Capturing the network packets, analyzing them, creating alerts, and storing both the packets and alerts.
#
# @ Author: Lizbeth Jurado 

import pyshark
import threading
import os
from datetime import datetime
#import sys
#sys.path.append(r'C:\\Users\\velas\\OneDrive\\Documents\\Fall23\\SWE2Project\\CS4311_LIDS_19uno5_Fall2023')
from backend.packet_analyzer import PacketAnalyzer
from backend.alerts_manager import AlertManager
import json

class LNIDSPacketCapture:
    def __init__(self, interface, external_storage_path):
        self.interface = interface
        self.external_storage_path = external_storage_path
        self.packet_analyzer = PacketAnalyzer()
        self.alert_manager = AlertManager()
        self.capture = None
        self.running = False

    def start_capture(self):
        self.running = True
        self.capture = pyshark.LiveCapture(interface=self.interface)

        # Capture in a new thread
        capture_thread = threading.Thread(target=self.capture_packets)
        capture_thread.start()

    def capture_packets(self):
        for packet in self.capture.sniff_continuously():
            if not self.running:
                break

            # Analyze PacketAnalyzer
            processed_packet = self.process_packet(packet)
            self.packet_analyzer.analyze_packet(**processed_packet)

            # Save packets to external storage
            self.save_packet_external(packet)

            # Save alerts generated by PacketAnalyzer
            self.save_alerts()

    def process_packet(self, packet):
        # Extracting necessary data from the packet
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        identifier = 'some_unique_identifier'  # Generate or extract a unique identifier

        try:
            sourceIP = packet.ip.src
            destIP = packet.ip.dst
            sourcePort = packet[packet.transport_layer].srcport
            destPort = packet[packet.transport_layer].dstport
            protocol = packet.transport_layer
            handshake = self.determine_handshake(packet)
        except AttributeError:
            # packet does not have IP or transport layer
            sourceIP, destIP, sourcePort, destPort, protocol, handshake = None, None, None, None, None, False

        # You need to define how to handle packetList
        packetList = []  # Placeholder for your packet list

        return {
            'packet': packet,
            'time': time,
            'identifier': identifier,
            'sourceIP': sourceIP,
            'sourcePort': sourcePort,
            'destIP': destIP,
            'destPort': destPort,
            'protocol': protocol,
            'handshake': handshake,
            'packetList': packetList
        }

    def determine_handshake(self, packet):
        # See if the packet is part of a handshake
        if hasattr(packet, 'tcp'):
            return packet.tcp.flags_syn == '1' and packet.tcp.flags_ack == '0'
        return False

    def save_packet_external(self, packet):
       # Save the packet data to an external hard drive
        filename = f"packet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pcap"
        filepath = os.path.join(self.external_storage_path, filename)

        with open(filepath, 'wb') as f:
            f.write(packet.get_raw_packet())

    def save_alerts(self):
        # Save alerts locally and on the analyst's device
        alerts = self.alert_manager.get_alerts()
        for alert in alerts:
        #JSON File
            filename = f"alert_{alert.identifier}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(self.alerts_storage_path, filename)
            with open(filepath, 'w') as file:
                json.dump(alert.to_dict(), file, indent=4)

    def stop_capture(self):
        self.running = False
        self.capture.close()


#interface = 'eth0'  #   your actual network interface rememebr mac is differnt
interface = 'en0'  # 
#capture = pyshark.LiveCapture(interface="en0")
external_storage_path = '/path/to/external/hard/drive'  # Replace with your actual mount point
lnids_packet_capture = LNIDSPacketCapture(interface, external_storage_path)
lnids_packet_capture.start_capture()


# lnids_packet_capture.stop_capture()

# alerts_manager.py

from backend import Alerts

class AlertManager:
    sharedAlerts = []
    identifierList = []

    def __init__(self):
        self.alerts = []

    def create_alert(self, level, time, IP, Port, description, identifier, pcap_data):
        alert = Alerts.Alerts(level, time, IP, Port, description, identifier)
        alert.PCAPData = pcap_data  # Set the PCAPData property
        self.alerts.append(alert)
        self.sharedAlerts.append(alert)
    
    def ident_list(self, packet, identifier):
        self.identifierList.append({identifier: [packet]})

    def get_alerts(self):
        return self.alerts

#alerts.py

class Alerts:
    def __init__(self, level, time, IP, Port, description,identifier):
        self.level = level
        self.time = time
        self.IP = IP
        self.Port = Port
        self.description = description
        self.identifier = identifier
    
    def __str__(self):
        return f"Level: {self.level}, Time: {self.time}, IP: {self.IP}, Port: {self.Port}, Description: {self.description}"
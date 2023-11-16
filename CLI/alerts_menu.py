# File: alerts_menu.py

# Description: Displaying alerts through a command-line interface (CLI). The class includes a method called display_Alerts that initiates the capture of network packets and then prints a list of alerts obtained from an AlertManager

# @ Author: Benjamin Hansen
# @ Modifier: Alejandro Hernandez


import sys
import os
import threading
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from menu import Menu
from backend import packets, alerts_manager

# @ Author: Benjamin Hansen
class Alerts_CLI(Menu):


    def __init__(self) -> None:
        super().__init__()
        
        
    # @ Author: Benjamin Hansen
    # @ Modifier: Alejandro Hernandez
    def display_Alerts(self):
        

        print("Debugged Display alerts")
        lstAlerts = alerts_manager.AlertManager().sharedAlerts
        print("Printing list alerts ",lstAlerts) # printing list 
        for i in lstAlerts:

            print(i)
        
        next_menu = self.get_user_input(">> ",self.choice_set)  
        self.navigate_next_menu(next_menu)
        



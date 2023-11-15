#File: menu.py
#
# Description: This file contains the implementation of the Menu class, which provides common functions for the CLI (Command Line Interface) to use across different menus in the LIDS (Local Intrusion Detection System). It includes utility methods for obtaining and validating user input and stores shared system configuration attributes.
#
# @ Author: Benjamin Hansen
# @ Modifier: Benjamin Hansen 

import config_parser
"""
from CLI.help_menu import HelpMenu
from CLI.pcap_menu import PcapMenu
from CLI.alerts_menu import Alerts_CLI
from CLI.main_menu import MainMenu
"""
import help_menu
import pcap_menu
import alerts_menu
import main_menu
from backend import alerts_manager

# @ Author: Benjamin Hansen
# @ Modifier: Benjamin Hansen 

class Menu():
    """A class for common functions the CLI will use across different menus.
    
    This class provides utility methods for obtaining and validating user input
    when navigating through different menu options in the CLI. It also stores shared
    system configuration attributes.
    """
    host_name = ""
    ip_address = ""
    mac_address = ""
    open_ports = []
    whitelisted_ips = []

 # @ Author: Benjamin Hansen
# @ Modifier: Benjamin Hansen 

    def __init__(self) -> None:
        self.choice_set = {"Help", "Config", "Show PCAP", "Alert", "Exit","All PCAPs","Start Menu"}

# @ Author: Benjamin Hansen
# @ Modifier: Benjamin Hansen 
    @classmethod
    def update_system_config(cls, hostname, ip_address, mac_address, open_ports, whitelisted_ips):
        """
        Updates the shared system configuration attributes.

        Args:
            hostname (str): The system's hostname.
            ip_address (str): The system's IP address.
            mac_address (str): The system's MAC address.
            open_ports (list): A list of open ports on the system.
            whitelisted_ips (list): A list of IPs that are whitelisted for the system.
        """
        cls.host_name = hostname
        cls.ip_address = ip_address
        cls.mac_address = mac_address
        cls.open_ports = open_ports
        cls.whitelisted_ips = whitelisted_ips
        

# @ Author: Benjamin Hansen 
# @ Modified: Benjamin Hansen

    def get_user_input(self, message: str, valid_input: set) -> str:
        """Gets and validates user input."""
        user_input = input(message)
        
        while user_input not in valid_input:
            print("Wrong input. Valid inputs are:")
            for val_input in valid_input:
                print(val_input)
            user_input = input(message)
        
        return user_input

# @ Author: Benjamin Hansen 
# @ Modified: Benjamin Hansen

    def navigate_next_menu(self, menu_option_selected: str) -> None:
        """Navigate to the next menu based on the user's selection

        
        This function takes a menu option and navigated to the next appropriate menu
        based on the user's input. The function supports options "Help", "Config", 
        "Show PCAP", and "Alert".

        Args:
            menu_option_selected (str): The menu option that the user has selected.
       
        match menu_option_selected:
            case _ if menu_option_selected == "Start Menu":
                print('\n' * 24)
                print(">> Start Menu")
                main_menu_instance = main_menu.MainMenu()
                main_menu_instance.show_menu()

            case _ if menu_option_selected == "Help":
                print('\n' * 24)
                print(">> Help Menu")
                menu = help_menu.HelpMenu()
                menu.display_help()
            
            case _ if menu_option_selected == "Config":
                print('\n' * 24)
                print(">> Configuring System")
                path = input(">> Enter configuration file name\n")
                configuration = config_parser.ConfigureCLI()
                configuration.configure(path)
    
            case _ if menu_option_selected == "Show PCAP" or menu_option_selected == "All PCAPs":
                # call class for help Show PCAP
                print('\n' * 24)
                print(">> PCAP info")
                alert_manager = alerts_manager.AlertManager()
                print("IDENT")
                print(alert_manager.identifierList)#add dummy data to the list
                print("ALERTS")
                print(alert_manager.sharedAlerts)#add dumy data to the list
                pcap_menu_display = pcap_menu.PcapMenu()
                pcap_menu_display.handle_pcap_search(menu_option_selected)
            
            case _ if menu_option_selected == "Alert":
                # call class for Alert menu
                print('\n' * 24)
                print(">> Alert")
                print("Info: Displaying alert information as they are generated by system")
                alertList = [
                    [2, "11.6578", "192.128.0.1", 80, "Unknown host ping"],
                    [3, "11.6578", "193.127.0.2", 27, "port scan"],
                    [1, "11.6578", "192.128.0.1", 80, "fail login attempt"],
                    [2, "11.6578", "193.124.0.3", 4040, "Unknown host ping"],
                ]
                alert_men = alerts_menu.Alerts_CLI()
                alert_men.display_Alerts()

            case _ if menu_option_selected == "Show PCAP HTML":
                pcap_menu_instance.display_pcap_in_html()

            case _ if menu_option_selected == "Exit":
                print("Exiting")
                exit()
                 """

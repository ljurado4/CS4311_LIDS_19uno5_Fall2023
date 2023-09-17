import menu
import os
import xml.etree.ElementTree as ET

class ConfigureCLI:
    """
    Command Line Interface configuration class.
    
    This class is responsible for parsing the XML configuration file and updating 
    system accordingly.
    """

    
    def configure(self, config_file_name: str) -> None:
        """
        Parses the provided XML configuration file and updates system.

        Args:
            config_file_name (str): The name of the XML configuration file.

        """
        
        
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(dir_path, config_file_name)
        tree = ET.parse(config_path)
        root = tree.getroot()
        
       
        for system in root.findall('system'):
            name = system.find('name').text
            ip = system.find('ip').text
            mac = system.find('mac').text
            ports = system.find('ports').text.split(',')
            whitelist = system.find('whitelist').text.split(',')
            
            print(f"Hostname: {name}")
            print(f"IP Address: {ip}")
            print(f"MAC Address: {mac}")
            print(f"Open Ports: {ports}")
            print(f"Whitelisted IPs: {whitelist}")

            menu_instance = menu.Menu()
            menu_instance.update_system_config(name,ip,mac,ports,whitelist)
            
        #move to next menu selection 
        menu_instance = menu.Menu()
        next_menu = input(">> ")
        menu_instance.navigate_next_menu(next_menu)
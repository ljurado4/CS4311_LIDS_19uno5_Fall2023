import menu


class ConfigureCLI:
    
    def configure(path_config_file: str) -> None:

        
        #parse xml file and update

        menu = menu.Menu()
        next_menu = input(">> ")
        menu.navigate_next_menu(next_menu)
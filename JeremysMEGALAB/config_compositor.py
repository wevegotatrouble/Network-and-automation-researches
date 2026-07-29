#!/usr/bin/python3
from pathlib import Path
import time
from jinja2 import Environment, FileSystemLoader
import yaml

jinja_exts = ["*.jinja", "*.j2"] # Variables for jinja extensions
yaml_exts = ["*.yaml", "*.yml"] # Variables for yaml extensions
templates_dir = Path("templates") # The directory for our jinja templates
yaml_properties_dir = Path("yaml_properties") # The directory for our yaml properties for the futue configs
configs_dir = Path("configs") # The directory where script'll make configs in .txt format
dirs = [templates_dir, yaml_properties_dir, configs_dir] # List for dirs_checker
yamlFiles = [] # This list will save all yaml files which we have in the folder
jinjaFiles = [] # This list will save all jinja files which we have in the folder


def main_menu():
    headlines = """Hello! This script created for making configs for Jeremy's MEGALAB
    If  you wanted to make the similiar configs for your own 3-tier topology you should know how
    this script works.

    We have 4 jinja templates in template folder are access_switches.j2, core_switches.j2, 
    distributed_switches.j2, routers.j2

    If you want to make configs for your own topology keep in your mind the following dependencies:
        - All router configs must start with 'R' in yaml_properties
        - All core switches configs must start with 'C' in yaml_properties
        - All distributed switches configs must start with 'D' in yaml_properties
        - All access switches configs must start with 'A' in yaml_properties

    Choose the actions:
    1) Run the full scripts
    2) Check the directories in your folder where you run your script
    3) Check jinja templates
    4) Check yaml yaml properties 
    5) Make configs with the existed properties 
    6) Show the main menu again
    7) Exit from the script
        """
    choice = input(headlines)
    # I made the menu where you can choose what script must do with configs and check your templates and properties
    match choice:
        case '1':
            dirs_checker()
            jinja_files_checker()
            yaml_files_checker()
            config_creator()
            countdown()
            main_menu()
        case '2':
            dirs_checker()
            countdown()
            main_menu()
        case '3':
            jinja_files_checker()
            countdown()
            main_menu()
        case '4':
            yaml_files_checker()
            countdown()
            main_menu()
        case '5':
            config_creator()
            countdown()
            main_menu()
        case '6':
            main_menu()
        case '7':
            exit()
        case _:
            print("Make a choice!")
            print("You will be bring to the main menu")
            countdown()
            main_menu()

def dirs_checker():

    # The simple function which checks whether you have folders for our tasks or not. 
    # In case if you don't have the folders, the script will make it instead of you
    for dir in dirs:
        try:
            dir.mkdir()
            print(f"Directory '{dir}' created successfully.")
        except FileExistsError:
            print(f"Directory '{dir}' already exists")
        except PermissionError:
            print(f"Permision denied: Unable to create '{dir}'.")
        except Exception as e:
            print(f"An error occured '{e}'.")


def yaml_files_checker():

    # The functinon which check all yaml properties for the future configs
    p = Path.cwd() # Make a current folder where you run the cript the folder where we will manipulate with the files
    if list(p.rglob("*.yaml")) or list(p.rglob("*.yml")): # We check files in the current folder by the extansions
        for y in yaml_exts:
            yaml_files = list(p.rglob(y))
            if yaml_files:
                for k in yaml_files:
                    print(f"Your yaml file is {k.name}")
                    yamlFiles.append(k)
    else:
        print(
            "You don't have any config files. Please, create or copy your config files in YAML format"
        )


def jinja_files_checker():

    p = Path.cwd() # Same things we do for the jinja templates. We parse the directory for the files which we need
    if list(p.rglob("*.jinja")) or list(p.rglob("*.j2")):
        for j in jinja_exts:
            jinja_files = list(p.rglob(j))
            if jinja_files:
                for i in jinja_files:
                    print(f"Your template is {i.name}")
                    jinjaFiles.append(i)
    else:
        print(
            "You don't have any templates. Please, create or copy your template's files in Jinja format"
        )

def config_creator():
    # The following function created for parsing between yaml properties and templates
    # And makes config automatically
    for a in yamlFiles:
        env = Environment(loader=FileSystemLoader("templates"),trim_blocks=True,lstrip_blocks=True)
        # Reading YAML data from file
        device_name = a.name
        device_stem = a.stem
        with open(f"yaml_properties/{device_name}", "r") as f:
            yaml_data = yaml.load(f, Loader=yaml.FullLoader)


        if yaml_data is None:
            print(f"Your yaml property for {device_stem} is empty")

        elif device_name.startswith("R"):
            template = env.get_template("routers.j2")
            with open(f"configs/{device_stem}.txt", "w") as f:
                f.write(template.render(yaml_data))
            print(f"Your config file for {device_stem} is ready")

        elif device_name.startswith("C"):
            template = env.get_template("core_switches.j2")
            with open(f"configs/{device_stem}.txt", "w") as f:
                f.write(template.render(yaml_data))
            print(f"Your config file for {device_stem} is ready")

        elif device_name.startswith("D"):
            template = env.get_template("distributed_switches.j2")
            with open(f"configs/{device_stem}.txt", "w") as f:
                f.write(template.render(yaml_data))
            print(f"Your config file for {device_stem} is ready")

        else:
            template = env.get_template("access_switches.j2")
            with open(f"configs/{device_stem}.txt", "w") as f:
                f.write(template.render(yaml_data))
            print(f"Your config file for {device_stem} is ready")

def countdown():
    # This counter created for the main menu to make the main menu more attractive
    t = 5
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end='\r')  # Overwrite the line each second
        time.sleep(1)
        t -= 1

if __name__ == "__main__":
    main_menu()


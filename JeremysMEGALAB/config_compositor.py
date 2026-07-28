#!/usr/bin/python3
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import yaml

"""What must my project do?
I think it must have environment no mater where this script works.
This script should create dirs for the files and check whether these files exist or not.
I presume these should be directories, not files.
these script should parse  yaml configs.
I think it should scna jinja templates too
Or not
Probably this script should take data from yaml configs
And go through jinja templates for these configs
The main point of the script is to write configs in txt files   w"""

jinja_exts = ["*.jinja", "*.j2"]
yaml_exts = ["*.yaml", "*.yml"]
templates_dir = Path("templates")
yaml_properties_dir = Path("yaml_properties")
configs_dir = Path("configs")
dirs = [templates_dir, yaml_properties_dir, configs_dir]
yamlFiles = []
jinjaFiles = []



def dirs_checker():


    # Create the directory

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

    p = Path.cwd()
    if list(p.rglob("*.yaml")) or list(p.rglob("*.yml")):
        for y in yaml_exts:
            yaml_files = list(p.rglob(y))
            if yaml_files:
                for k in yaml_files:
                    print(f"Your config is {k.name}")
                    yamlFiles.append(k)
    else:
        print(
            "You don't have any config files. Please, create or copy your config files in YAML format"
        )


def jinja_files_checker():

    p = Path.cwd()
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
     # Check if the path is absolute
    for a in yamlFiles:
        env = Environment(loader=FileSystemLoader("templates"),trim_blocks=True,lstrip_blocks=True)
        # Reading YAML data from file
        device_name = a.name
        device_stem = a.stem
        with open(f"yaml_properties/{device_name}", "r") as f:
            yaml_data = yaml.load(f, Loader=yaml.FullLoader)

        #print(yaml_data)

        if yaml_data is None:
            print(f"Your config file {device_name} is empty")

        elif device_name.startswith("R"):
            #env = Environment(loader=FileSystemLoader("templates"))
            template = env.get_template("routers.j2")
            with open(f"configs/{device_stem}.txt", "w") as f:
                f.write(template.render(yaml_data))

        elif device_name.startswith("C"):
            #env = Environment(loader=FileSystemLoader("templates"))
            template = env.get_template("core_switches.j2")
            with open(f"configs/{device_stem}.txt", "w") as f:
                f.write(template.render(yaml_data))

        elif device_name.startswith("D"):
            #env = Environment(loader=FileSystemLoader("templates"))
            template = env.get_template("distributed_switches.j2")
            with open(f"configs/{device_stem}.txt", "w") as f:
                f.write(template.render(yaml_data))

        else:
            #env = Environment(loader=FileSystemLoader("templates"))
            template = env.get_template("access_switches.j2")
            with open(f"configs/{device_stem}.txt", "w") as f:
                f.write(template.render(yaml_data))

def read_lists():
    #print(yamlFiles)
    #print(jinjaFiles)

    # Check if the path is absolute
    for a in yamlFiles:
        #print("Is absolute:", a.is_absolute())

        # Check if the path is absolute
        print("File name:", a.name)

        # Check if the path is absolute
        #print("Extension:", a.suffix)

        # Check if the path is absolute
        #print("Parent Directory:", a.parent)
    #for b in jinjaFiles:
        #print("Is absolute:", b.is_absolute())

        ## Check if the path is absolute
        #print("File name:", b.name)

        ## Check if the path is absolute
        #print("Extension:", b.suffix)

        ## Check if the path is absolute
        #print("Parent Directory:", b.parent)

def yaml_parser():
    
    # Check if the path is absolute
    for a in yamlFiles:

        # Check if the path is absolute
        device_parameters = a.name
        device_stem = a.stem
        print("File name with extension:", device_parameters)
        print("File name without extension:", device_stem)
        #if device_parameters.startswith("R"):
        #    print("File name with extension:", device_parameters)




if __name__ == "__main__":
    dirs_checker()
    jinja_files_checker()
    yaml_files_checker()
    #yaml_parser()
    #read_lists()
    config_creator() 




I created the script which makes configs for Jeremy's IT LAB automatically
I used python modules like pathlib, time, jinja2, yaml

You can use this script for the similar topologies with editing or making your own topology

Folder Hierarchy:

```Linux
├── CCNA Mega Lab (Jeremy's IT Lab).pka
├── config_compositor.py
├── configs
│   ├── ASWA1.txt
│   ├── ASWA2.txt
│   ├── ASWA3.txt
│   ├── ASWB1.txt
│   ├── ASWB2.txt
│   ├── ASWB3.txt
│   ├── CSW1.txt
│   ├── CSW2.txt
│   ├── DSW-A1.txt
│   ├── DSW-A2.txt
│   ├── DSW-B1.txt
│   ├── DSW-B2.txt
│   └── R1.txt
├── templates
│   ├── access_switches.j2
│   ├── core_switches.j2
│   ├── distributed_switches.j2
│   └── routers.j2
└── yaml_properties
    ├── ASWA1.yml
    ├── ASWA2.yml
    ├── ASWA3.yml
    ├── ASWB1.yml
    ├── ASWB2.yml
    ├── ASWB3.yml
    ├── CSW1.yml
    ├── CSW2.yml
    ├── DSW-A1.yml
    ├── DSW-A2.yml
    ├── DSW-A3.yml
    ├── DSW-B1.yml
    ├── DSW-B2.yml
    ├── DSW-B3.yml
    └── R1.yml
```

yaml_properties - all properties which will be used for the future configs
templates - Jinja templates for our configs
configs - the directory where the script places config files in text format
CCNA Mega Lab (Jeremy's IT Lab).pka - the lab which we will use our configs
config_compositor.py - the python script which makes configs

This script parse YAML properties and accept the proper properties for the appropriate Jinja templates

Requirements for YAML properties:

- All router configs must start with 'R' in yaml_properties
- All core switches configs must start with 'C' in yaml_properties
- All distributed switches configs must start with 'D' in yaml_properties
- All access switches configs must start with 'A' in yaml_properties

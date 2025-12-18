#Guide for better understanding how Ansible works with Jinja templates and Cisco devices

If you watch the tutorial which demonstrated how to work with Jinja templates, but you don't understand where the author got all variables from the video, this short guide is for you.

What you need for this lab:
- EVE-NG
- image for switches i86bi_linux_l2-adventerprisek9-ms.SSA.high_iron_20180510.bin
- image for routers i86bi_LinuxL3-AdvEnterpriseK9-M2_157_3_May_2018.bin
- Host machine with Ansible ( you can use any cloud from VirtualBox or VMWare << personally me created a pool for virtual machine manager >>)
- Use your IP addresses which your cloud will assign for Cisco devices
- Write them down in host file
- activate ssh connection on each Cisco device manually in configuration mode with the command `crypto key generate rsa modulus 2048` 
- check connectivity with the ping command
- `ansible OSPF-SINGLE-AREA -m ping `
- ![[Pasted image 20251218153932.png | 200]]
- delete all files from host_vars
- Don't delete the directory host_vars

Let's get started
1) Run the playbook `ansible-playbook playbooks/cisco_ospf_facts.yml `
- with this playbook, you can see all information from ospfv2 and ospf_interfaces modules
- Why can you see variables from these modules? Because we have them in this line `gather_network_resources: [ospfv2, ospf_interfaces]`
- And we pointed the path with this line `var: cisco_facts.ansible_facts.ansible_network_resources`
- << You can check all Cisco facts which Ansible retrieves from Cisco devices, just cut the line to `var: cisco_facts`>> (#You may choose other variable and wrap your head in debug mode it will help you to understand Ansible better #)
1) Check the template in `playbooks/template/ospf.j2`
2) Compare with the data which we retrieved from the previous step (You can train a lot of modules and config just with comparing the data which you get and creating Jinja modules for them) << If someone knows the better method to understand how Ansible works with network devices, please, share with me your golden rules>>
3) Check the playbook that we are about to run `playbooks/cisco_ospf.yml`
```YAML
- name: Gather OSPF configs facts
  cisco.ios.ios_facts:
    gather_subset: ['!all', '!min']
    gather_network_resources: [ospfv2, ospf_interfaces]
  register: cisco_facts
```
 - You can see that the first part is a copy from the playbook which we played previously
 - It's the date where we are going to retrieve our variables for OSPF configuration
 4) Check the following part of our YAML file. We can see that we use built-in Ansible module
 ```YAML
 - name: Format OSPF configs (Cisco)
  template:
    src: templates/ospf2.j2
    dest: host_vars/{{ inventory_hostname }}.yml
 ```
- It's really inconvenient that we have a template for this task. 
- It can handle with chasm or routers and switches and each might have own unique host file
4) Look at the end part of our file
```YAML
vars:
  ospf_processes: '{{ cisco_facts.ansible_facts.ansible_network_resources.ospfv2.processes }}'
  ospf_interfaces: '{{ cisco_facts.ansible_facts.ansible_network_resources.ospf_interfaces }}'
```
- These variables ease our lives. Instead of using long paths, we use short variables in our Jinja template
6) Run the playbook
7) Check results in host_vars
8) Enjoy with done job

----------------------------------------------------------------------------------------
I took this lab and a little modified it from here https://www.networkacademy.io/ccna/ospf/configuring-single-area-ospf
I was inspired by https://github.com/learn-skillnuggets

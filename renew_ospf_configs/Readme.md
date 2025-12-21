We have host_vars for each device in our lab. We can change them or add some new variables or implement our configs for another topology. With this playbooks I show you how to delete, renew and check our new OSPF configs

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

Let's get started

1. Check the playbook `cisco_delete_and_show_ospf.yml`

- we have 4 tasks which delete all ospf configs from ospfv2, delete configs from ospf_interfaces module, gather and register show commands, show commands via debug mode

2. Run this book and check the output

- your devices are ready for new configs
- you may leave it without any new configs
- but we decide to continue in this lesson

3. Check the playbook `cisco_config_ospf.yml`

- we have two tasks which retrieve variables from the host_vars for each device for OSPF interfaces configs
- The first task changes OSPF interfaces priorities
- The second one enable OSPF process via enabling OSPF on interfaces

4. Run the book
5. Check `deploy_ospf_cisco.yml`

- this playbook based on the jinja template with cisco_config module
- I tried to make it with cisco_ospfv2 module, but it didn't work for me
- that so we can check the template `ospf_config.j2`
- this template imitates typical cisco OSPF configs

6. Run the playbook
7. Check `show_ospf_config.yml`

- you can see that we use cisco_command module
- all these commands which we use they used for OSPF verification workflow
  ![](https://cdn.networkacademy.io/sites/default/files/2024-07/ospf-verification-workflow.svg)
  Finally, you may check and run `renew_show_ospf_cisco_config.yml`. This playbook you can run if you changed OSPF networks and OSPF interfaces in your host_vars. We just imported all playbook that you've considered before.


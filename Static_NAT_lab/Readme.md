Today, I am gonna show you my solution to use Ansible for static NAT

![Static NAT Lab](https://www.networkacademy.io/ccna/network-services/static-nat)

If you like the lab and courses by the NetworkAcademy.IO, you can praise Ivan with the following link ![Ivan Ivanov is making hard networking concepts easy to understand](https://buymeacoffee.com/networkacademy)

### What you need for this lab:

- EVE-NG
- image for switches i86bi_linux_l2-adventerprisek9-ms.SSA.high_iron_20180510.bin
- image for routers i86bi_LinuxL3-AdvEnterpriseK9-M2_157_3_May_2018.bin
- Host machine with Ansible ( you can use any cloud from VirtualBox or VMWare << personally me created a pool for virtual machine manager >>)
- Use your IP addresses which your cloud will assign for Cisco devices
- Write them down in host file
- activate ssh connection on each Cisco device manually in configuration mode with the command `crypto key generate rsa modulus 2048` ( I did it once that it works each time when I run the lab what means you probably don't need to run this command )
- check connectivity with the ping command
- ` ansible NAT-Lab -m ping --ask-vault-pass`

### Configuration Tasks

1. PC1, PC2, and PC3 must be able to ping Google DNS 8.8.8.8
2. Google's server must be able to ping PC1, PC2 and PC3.
3. You must use Static NAT.

### Let's get started

1. I created a simple template for the NAT configuration playbook. You should open it in `templates/cisco_static_nat.j2`
2. What can you see the new. It is that we used `range(1,4)` in our playbook as so that we seemingly use Python script, but we actually don't. (It depends how to look at the discussion's object). This feature help us to make 3 lines configs without manual typing for each static NAT entry
3. We run our configuration with the `cisco_static_nat.yml`. Nothing new is there
4. After it you should run two check playbooks. First of them is `cisco_static_nat_check1.yml`. It allows check where we can ping the server from the clients. I repeated this task twice, because it work with lesser losses after ARP processing
5. Look at `cisco_statitc_nat_check2.yml`. You can see something new and it is `with_sequence` line. It allows to ping each client from the server. Run it

### How to use these playbooks

You may run each playbook for each task manually or you can use `cisco_static_nat_full.yml` which runs all playbooks at once.


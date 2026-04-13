Today, I am gonna show you my solution to use Ansible for HSRP Lab

![HSRP Lab](https://www.networkacademy.io/ccna/network-services/configuring-hsrp)

If you like the lab and courses by the NetworkAcademy.IO, you can praise Ivan with the following link ![Ivan Ivanov is making hard networking concepts easy to understand](https://buymeacoffee.com/networkacademy)

What you need for this lab:

- EVE-NG
- image for switches i86bi_linux_l2-adventerprisek9-ms.SSA.high_iron_20180510.bin
- image for routers i86bi_LinuxL3-AdvEnterpriseK9-M2_157_3_May_2018.bin
- Host machine with Ansible ( you can use any cloud from VirtualBox or VMWare << personally me created a pool for virtual machine manager >>)
- Use your IP addresses which your cloud will assign for Cisco devices
- Write them down in host file
- activate ssh connection on each Cisco device manually in configuration mode with the command `crypto key generate rsa modulus 2048` ( I did it once that it works each time when I run the lab what means you probably don't need to run this command )
- check connectivity with the ping command
- ` ansible HSRP-Lab -m ping --ask-vault-pass`

### Configuration Tasks

Requirement 1: Configure a resilient default gateway address in Vlans 10. Use HSRP as the first-hop redundancy protocol. Use version 1.

- The group number must be 10.
- The VIP address must be 10.10.1.1.
- The Hello interval must be 1 second. The hold timer must be 3 seconds.
- Preemption must be enabled.
- Distribution switch DSW1 must be the active router.
  Requirement 2: Configure a resilient default gateway address in Vlans 20.
- Use version 2.
- The group number must be 20.
- The VIP address must be 10.20.1.1.
- The Hello interval must be 2 seconds. The hold timer must be 6 seconds.
- Preemption must be enabled.
- Distribution switch DSW2 must be the active router.
  Requirement 3: If the active router has an uplink failure, the standby route must immediately take over.
  Verification 1: Traceroute from SRV1 (10.10.1.100) to EXT1(10.32.1.100) must go via the path DSW1-ISP1-EXT1.
  Verification 2: Traceroute from SRV2 (10.20.1.100) to EXT1(10.32.1.100) must go via the path DSW2-ISP2-EXT1.
  Verification 3: If DSW1's eth0/1 uplink is shut down, DSW2 must immediately become the Active router for group 10.

### Playbooks' structure

<img width="504" height="408" alt="image" src="https://github.com/user-attachments/assets/f58d8a74-3c9b-4dab-9e1c-7ae470d4874f" />


- You will run hsrp_full.yml for our lab, which consists the following playbooks
  <img width="290" height="259" alt="image" src="https://github.com/user-attachments/assets/22d1332d-355e-43c2-b45d-a9e14ba75c80" />

- If you want to use `cisco.ios.ios_config` instead of `cisco.ios.ios_hsrp_interfaces`, use `hsrp_dsw1_ver2.yml` and `hsrp_dsw2_ver2.yml` instead of `hsrp_dsw1.yml`, `hsrp_dsw2.yml`
- In case to try out other setting I created `interfaces_without_hsrp_settings.yml` what deletes HSRP settings and up interface Ethernet0/1 in DSW1

### Let's get started

1. I created two books which satisfy our requirements `hsrp_dsw1.yml`, `hsrp_dsw2.yml`. Open them and check them out. You can use my books for your settings just with replacing with your parameters
2. Run `hsrp_full.yml`. Ansible will accept the settings and show all accepted parameters
3. If you want to change something, use `interfaces_without_hsrp_settings.yml`

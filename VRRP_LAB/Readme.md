Today, I am gonna show you my solution to use Ansible for VRRP Lab

![VRRP Lab](https://www.networkacademy.io/ccna/network-services/virtual-router-redundancy-protocol-vrrp)
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
- ` ansible VRRP-Lab -m ping --ask-vault-pass`

### Configuration Tasks

Requirement 1: Configure a resilient default gateway address in Vlans 10.

- Use VRRP with VRID 10.
- The Virtual router address must be 10.10.1.1.
- Distribution switch DSW1 must be the active router.
  Requirement 2: Configure a resilient default gateway address in Vlans 20.
- Use VRRP with VRID 20.
- The Virtual router address must be 10.20.1.1.
- Distribution switch DSW2 must be the active router.
  Requirement 3: If the active router has an uplink failure, the standby route must immediately take over.
  Verification 1: Traceroute from SRV1 (10.10.1.100) to EXT1(10.32.1.100) must go via the path DSW1-ISP1-EXT1.
  Verification 2: Traceroute from SRV2 (10.20.1.100) to EXT1(10.32.1.100) must go via the path DSW2-ISP2-EXT1.
  Verification 3: If DSW1's eth0/1 uplink is shut down, DSW2 must immediately become the Active router for VRRP group 10.

### Playbooks' structure

- You will run vrrp_full.yml for our lab, which consists the following playbooks
  -unshutdown_port_dsw1.yml
  -unshutdown_port_dsw2.yml
  -uplink_trigger_dsw1.yml
  -uplink_trigger_dsw2.yml
  -vrrp_chk1.yml
  -vrrp_chk2.yml
  -vrrp_dsw1.yml
  -vrrp_dsw2.yml
  -vrrp_full.yml
  -vrrp_gather_facts.yml
  -vrrp_track_dsw1.yml
  -vrrp_track_dsw2.yml
  -vrrp_verification1.yml
  -vrrp_verification2.yml
  -vrrp_verification3.yml
  -vrrp_verification4.yml

### Let's get started

1. I created two books which satisfy our requirements `vrrp_dsw1.yml`, `vrrp_dsw2.yml`. Open them and check them out. You can use my books for your settings just replacing with your parameters
2. Run `vrrp_full.yml`. Ansible will accept the settings and show all accepted parameters

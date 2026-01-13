I decided to make an automation playbooks for OSPF configuration lab from this link ![Final OSPF Configuration Lab | NetworkAcademy.IO](https://www.networkacademy.io/ccna/ospf/final-ospf-configuration-lab)
If you want to complete this lab manually, you can click on the link above

If you like the lab and courses by the NetworkAcademy.IO, you can praise him with the following link ![Ivan Ivanov is making hard networking concepts easy to understand](https://buymeacoffee.com/networkacademy)

### What you need for this lab:

- EVE-NG
- image for switches i86bi_linux_l2-adventerprisek9-ms.SSA.high_iron_20180510.bin
- image for routers i86bi_LinuxL3-AdvEnterpriseK9-M2_157_3_May_2018.bin
- Host machine with Ansible ( you can use any cloud from VirtualBox or VMWare << personally me created a pool for virtual machine manager >>)
- Use your IP addresses which your cloud will assign for Cisco devices
- Write them down in host file
- activate ssh connection on each Cisco device manually in configuration mode with the command `crypto key generate rsa modulus 2048` ( I did it once that it works each time when I run the lab what means you probably don't need to run this command )
- check connectivity with the ping command
- `ansible OSPF-SINGLE-AREA -m ping `

### Configuration Tasks

    Task 1: Enable OSPFv2 on all routers:
        Routers R1 through R6 must use OSPF process ID 1.
        Router R7 must use OSPF Process ID 34.

    Task 2: Place all interfaces in OSPFv2 Area 0.
        You must not use the network command on routers R5 and R6 when enabling the routing process on the interfaces.
        You must use the most specific network command when enabling OSPFv2 on the data center routers R1-R4.
        R3's interface toward the internet must not be part of the OSPF routing.

    Task 3: Modify the OSPFv2 RIDs on all routers according to Table 1.
        Ensure the changes take effect and routers establish adjacencies using the new RIDs.

    Task 4: Ensure R1 is elected the Designated Router (DR) on network 10.1.1.0/24.
        R2 must be elected as the backup designated router (BDR).
        Ensure the changes take effect.

    Task 5: Ensure no DR/BDR election occurs on subnets 10.1.2.0/24 and 10.1.3.0/24.

    Task 6: Change the default reference bandwidth value (100Mbps) to 1Gbps on all OSPFv2 nodes.

    Task 7: Disable the OSPFv2 Hello packets on all interfaces connected to 10.16.1.0/24 and 10.16.2.0/24.

        Ensure the networks are advertised in the OSPFv2 domain.

    Task 8: Change the Hello and Dead intervals on subnet 10.1.4.0/24 to 1 and 4 seconds, respectively.

    Task 9: Enable clear text authentication between R3 and R5 using the password "Cisco."

    Task 10: Ensure that SRV1 and SRV2 connect to the large branch via the link R4-R6.
        You are not allowed to use the ip ospf cost command.
        You are not allowed to change the bandwidth of links 10.1.2.0/24 and 10.1.3.0/24.

    Task 11: Add an additional loopback interface on router R1.
        Configure the IP address 1.1.1.250/25.
        Enable OSPFv2 using the most specific network command possible.
        The loopback must be advertised into OSPF with its real subnet mask (/24).

    Task 12: Configure R3 to inject a default route (0.0.0.0/0) in the OSPF domain.
        R3 must inject a default route even when the Internet connection is down.

### Let's get started

1. What did I for this lab the first? I completed host_vars where I pointed values needed for this lab. You can check them in host_vars
2. Open `deploy_ospf_cisco.yml`, then open the template which is typed in the playbook
3. The first three lines covered tasks # 1, 3 and 6

```YAML
router ospf {{ ospf_process.process_id }}
 router-id {{ ospf_process.router_id }}
 auto-cost reference-bandwidth {{ospf_process.reference_bandwidth }}
```

As so that these parameters exist in each Router where we need configuring OSPF. We use them without looping, so that every configurable router will have own OSPF process, router-id and reference-bandwidth will be configured with 1 Gbps

4. Other lines work with the principle if we don't have a value while parsing host_vars, just pass it

```YAML
{% if ospf_process.passive_interface is undefined %}
{% else %}
 passive-interface {{ ospf_process.passive_interface
}}
```

5. Lines which working with loops covered task #2 partially and task #7
6. Look at `cisco_config_ospf.yml `. Mostly this playbook uses cisco_ospf_interface module. It allows us to make configurations for the proper interfaces. This file covers task # 2, 4, 5, 8
7. Check `cisco_assign_interfaces.yml` and its template `interfaces.j2`. This simple playbook resolves the task number #11
8. For completing task # 11 was used `cisco_assign_interfaces.yml` and the template `interfaces.j2`. It works with the same principle, "If you don't have a value, pass it"
9. To have path through R4-R6, we configure R5's bandwidth lower than others so that it will have lower priorities. Hence, it will make the path through R4-R6 is more preferable. This task resolved by `cisco_bandwidth.yml` and `bandwidth_cisco.j2`
10. The next what we should reset are OSPF processes. `clear_ip_ospf_process.yml` does it with cisco_ios_command module. After it, we use the built-in pause module to wait for OSPF negotiation's processes. I chose 60 second because we have average hello timer is 10 seconds and average dead timer is 40 seconds. 60 seconds is absolutely enough for assigning new routers roles
11. Verification playbooks with numbers 1–7 satisfied the following requirements

```
- SRV1 and SRV2 must be able to ping PC3 and PC4.
The traceroute from SRV1/SRV2 to PC3 must show that the traffic goes via R4-R6.
- All devices must be able to ping 8.8.8.8 (address on the Internet).
- The show ip ospf neighbor command on R3 must show that R1 is the DR on network 10.1.1.0/24.
- The show ip ospf neighbor command on R3/R4 must show that no DR/BDR exists on networks 10.1.2.0/24 and 10.1.3.0/24.
- The show ip ospf interface command on R4 must show that the Hello/Dead intervals on 10.1.4.0/24 are 1/4 seconds.
- The show ip route 1.1.1.250 on R7 must show that the network 1.1.1.128/25 is in the routing table.
```

### How to use these playbooks

You may run each playbook for each task manually or you can use `final_ospf_lab.yml` which runs all playbooks at once.
Everything it works, but to see all verification commands you must run every vitrification playbook manually


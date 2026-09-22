# Lab Topology Design — EVE-NG Airport IT Network

## 1. Simple Explanation

This lab is like a small airport terminal network. Each airport area gets its own VLAN so devices are separated and easier to secure:

- **Check-in VLAN**: counter PCs and bag-tag workstations.
- **Gate VLAN**: boarding/gate workstations and scanners.
- **Baggage VLAN**: baggage scanners and bag-tag printers.
- **Airport Operations VLAN**: operations/control-centre users who monitor airport or airline operational activity.
- **IT Management VLAN**: admin workstation and network-device management.
- **Guest Wi-Fi VLAN**: passengers/guests; blocked from internal airline systems.
- **Server VLAN**: DNS, mock DCS/check-in app, mock baggage app, monitoring server.

The router connects all VLANs using **router-on-a-stick**. The switch carries all VLANs to the router over one trunk link.

## 2. Employer Value

This lab demonstrates practical skills useful for IT Support, NOC, Network Support, Junior Network Administrator, and Airport/Airline IT roles:

- Designing segmented networks using VLANs.
- Mapping business departments to network zones.
- Configuring trunking and router-on-a-stick inter-VLAN routing.
- Supporting DHCP-based client connectivity.
- Applying ACL security policies between departments.
- Documenting topology, interface mapping, and verification evidence.
- Troubleshooting connectivity issues using structured network commands.

For employers, this project shows that I can translate a real workplace environment into a documented network design, then verify and troubleshoot it like an IT support or NOC technician.

## 3. Physical Topology Diagram

```text
                                  INTERNET / ISP CLOUD
                                         |
                                  [Optional later]
                                         |
                              G0/1  R1-AIRPORT-EDGE
                         +---------------+----------------+
                         | Router-on-a-stick / DHCP / ACLs |
                         +---------------+----------------+
                                         |
                                   G0/0 TRUNK
                              802.1Q VLANs 10-70
                                         |
                                  G0/0  SW1-CORE
                         +---------------+----------------+
                         |      Layer 2 VLAN Access Switch |
                         +---------------+----------------+
          G0/2 VLAN10     |      |      |      |      |      |      G0/1 VLAN70
      CHECKIN-PC1         |      |      |      |      |      +---- SRV-DNS-APP
                           |      |      |      |      |
          G0/3 VLAN20      |      |      |      |      +----------- G2/0 VLAN60
      GATE-PC1 ------------+      |      |      |                  GUEST-LAPTOP/AP
                                  |      |      |
          G1/0 VLAN30             |      |      +---------------- G1/3 VLAN50
      BAG-SCANNER1 ---------------+      |                       IT-ADMIN-PC
                                         |
          G1/1 VLAN30                    +---------------------- G1/2 VLAN40
      BAG-PRINTER1                                               OPS-PC1
```

## 4. Logical VLAN Topology Diagram

```text
                           R1-AIRPORT-EDGE G0/0
        -------------------------------------------------------------------
        |         |         |         |         |         |         |
     G0/0.10   G0/0.20   G0/0.30   G0/0.40   G0/0.50   G0/0.60   G0/0.70
     VLAN 10   VLAN 20   VLAN 30   VLAN 40   VLAN 50   VLAN 60   VLAN 70
   10.10.10.1 10.10.20.1 10.10.30.1 10.10.40.1 10.10.50.1 10.10.60.1 10.10.70.1
        |         |         |         |         |         |         |
   CHECK-IN    GATES    BAGGAGE    OPS/      IT MGMT   GUEST     SERVERS
   PCs/DCS   boarding   scanners   CONTROL     SSH      Wi-Fi    DNS/apps
                                  CENTRE
```

## 5. EVE-NG Device List

| Device | Suggested Image | Purpose |
|---|---|---|
| R1-AIRPORT-EDGE | Cisco IOSv / CSR1000v | Inter-VLAN routing, DHCP, ACLs, optional NAT later |
| SW1-CORE | Cisco IOSvL2 / Cisco IOL L2 | VLAN creation, trunking, access ports |
| SRV-DNS-APP | Ubuntu Server or VPCS | Mock DNS and internal application server in VLAN 70 |
| CHECKIN-PC1 | VPCS | Check-in counter workstation |
| GATE-PC1 | VPCS | Gate/boarding workstation |
| BAG-SCANNER1 | VPCS | Baggage scanner simulation |
| BAG-PRINTER1 | VPCS | Bag tag printer simulation; static IP recommended |
| OPS-PC1 | VPCS | Airport operations/control-centre workstation |
| IT-ADMIN-PC | VPCS | Admin workstation for SSH testing |
| GUEST-LAPTOP | VPCS | Guest Wi-Fi simulation |

> **DHCP design note:** DHCP is provided by `R1-AIRPORT-EDGE` in this lab. The server is named `SRV-DNS-APP` to avoid confusion between router-based DHCP and server-based DHCP.

## 6. Interface and Cable Map

| Link | From | Interface | To | Interface | VLAN/Mode |
|---|---|---|---|---|---|
| 1 | R1-AIRPORT-EDGE | G0/0 | SW1-CORE | G0/0 | 802.1Q trunk, VLANs 10-70 |
| 2 | SW1-CORE | G0/1 | SRV-DNS-APP | eth0 | Access VLAN 70 |
| 3 | SW1-CORE | G0/2 | CHECKIN-PC1 | eth0 | Access VLAN 10 |
| 4 | SW1-CORE | G0/3 | GATE-PC1 | eth0 | Access VLAN 20 |
| 5 | SW1-CORE | G1/0 | BAG-SCANNER1 | eth0 | Access VLAN 30 |
| 6 | SW1-CORE | G1/1 | BAG-PRINTER1 | eth0 | Access VLAN 30 |
| 7 | SW1-CORE | G1/2 | OPS-PC1 | eth0 | Access VLAN 40 |
| 8 | SW1-CORE | G1/3 | IT-ADMIN-PC | eth0 | Access VLAN 50 |
| 9 | SW1-CORE | G2/0 | GUEST-LAPTOP/AP | eth0 | Access VLAN 60 |

## 7. VLAN Security Policy

| Source VLAN | Allowed | Blocked |
|---|---|---|
| VLAN 10 CHECKIN | DNS, DCS/check-in server, required internal apps | Guest Wi-Fi |
| VLAN 20 GATE | DNS, DCS/boarding server, required internal apps | Guest Wi-Fi |
| VLAN 30 BAGGAGE | DNS and baggage server | Guest Wi-Fi and unnecessary lateral traffic |
| VLAN 40 AIRPORT_OPS | Internal apps and monitoring | Guest access to operations devices |
| VLAN 50 IT_MGMT | SSH/admin to network devices and servers | Not for regular users |
| VLAN 60 GUEST_WIFI | Internet only in real life; in this lab block internal 10.10.0.0/16 | All internal airport VLANs |
| VLAN 70 SERVERS | Provides DNS/app services | Should not initiate unnecessary user traffic |

## 8. Build Order

1. Create VLANs on SW1.
2. Configure SW1 access ports.
3. Configure SW1 trunk to R1.
4. Configure SW1 management SVI in VLAN 50.
5. Configure R1 physical G0/0 and subinterfaces.
6. Configure DHCP pools on R1.
7. Configure ACLs on R1.
8. Configure SSH on R1 and SW1.
9. Configure VPCS clients with DHCP.
10. Test communication and capture screenshots.

## 9. Key Verification Commands

Use these commands to confirm the topology, VLANs, trunking, DHCP, ACLs, routing, and SSH management are working correctly.

### Switch verification

```cisco
show vlan brief
show interfaces trunk
show interfaces status
show mac address-table
show running-config interface g0/0
show running-config interface g0/1
```

### Router verification

```cisco
show ip interface brief
show ip route
show ip dhcp binding
show ip dhcp pool
show access-lists
show running-config interface g0/0
show running-config | section ip dhcp pool
show ip ssh
```

### Client verification

```text
show ip
ping 10.10.70.10
ping 10.10.10.1
ping 10.10.20.1
ping 10.10.30.1
```

These commands prove that the portfolio is not only a diagram. They show that the network can be verified and troubleshot using Cisco-style operational commands.

## 10. Related Documentation

- [IP Addressing Plan](./ip-addressing-plan.md)
- [Verification Checklist](./verification-checklist.md)
- [Topology Overview](./topology.md)

## 11. Assumptions and Limitations

- This is a lab simulation built in EVE-NG, not a production airline network.
- Device names, VLANs, and services are inspired by common airport IT functions.
- The lab does not claim to represent the private internal network of WestJet, Porter, Air Transat, Toronto Pearson/GTAA, or any specific airline or airport organization.
- The purpose is to demonstrate networking, segmentation, troubleshooting, and documentation skills.
- Internet/NAT connectivity is optional and can be added later if the lab is expanded.

## 12. Screenshot Evidence for GitHub

Take screenshots of:

- EVE-NG topology diagram.
- `show vlan brief`.
- `show interfaces trunk`.
- `show ip interface brief` on R1.
- `show ip dhcp binding`.
- `show access-lists`.
- Successful check-in/gate/baggage to server ping.
- Failed guest Wi-Fi to internal network ping.
- SSH test from IT-ADMIN-PC to router/switch.

## 13. Airline Job Positioning

This topology file is useful for applications to aviation IT, NOC, IT Support, Network Support, Junior Network Administrator, MSP, and airport vendor roles. It is especially relevant for organizations connected to airline and airport operations, such as airlines, airport authorities, aviation service providers, and managed IT providers supporting airport environments.

Strong interview message:

```text
I can design and document a segmented airport-style network, map business functions to VLANs, apply security policies, and verify/troubleshoot connectivity.
```

## 14. Resume Bullet

```text
Built and documented an EVE-NG airport network lab using VLAN segmentation, 802.1Q trunking, router-on-a-stick inter-VLAN routing, DHCP, ACL security policies, SSH management, and Cisco verification commands to simulate airport IT network support workflows.
```

Shorter version:

```text
Built an EVE-NG airport network lab using VLANs, trunking, inter-VLAN routing, DHCP, ACLs, SSH, and verification commands to practice airport IT and NOC-style troubleshooting.
```

## 15. LinkedIn Featured Project Text

```text
Airport VLAN Network Lab — Aviation IT Portfolio Project

I built an EVE-NG airport network lab to practice VLAN segmentation, trunking, router-on-a-stick inter-VLAN routing, DHCP, ACLs, SSH management, and structured troubleshooting.

The lab simulates airport departments such as check-in, gate operations, baggage, airport operations, IT management, guest Wi-Fi, and servers. The goal was to document how segmented networks can support secure and reliable airport IT operations.

This project supports my target roles in IT Support, NOC, Network Support, Cloud/Network Support, and aviation IT.
```

## 16. Interview Explanation

If an interviewer asks, "Tell me about your airport VLAN project," say:

```text
I built an EVE-NG airport network lab to practice enterprise networking in an aviation-style environment. I separated departments like check-in, gates, baggage, airport operations, IT management, guest Wi-Fi, and servers into different VLANs. I used trunking and router-on-a-stick to route between VLANs, configured DHCP for clients, and planned ACL policies to restrict unnecessary access. I documented the physical topology, logical VLAN topology, interface map, build order, verification commands, and screenshot evidence. The project helped me practice both configuration and troubleshooting, especially the type of structured thinking needed in IT Support, NOC, and Network Support roles.
```

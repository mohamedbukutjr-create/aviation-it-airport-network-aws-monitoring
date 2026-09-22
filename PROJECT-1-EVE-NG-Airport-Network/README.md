# Project 1: EVE-NG Airport VLAN Network Design

## Project Goal

Build a realistic **Airport IT network lab** in EVE-NG for an airline operating at a major airport such as Toronto Pearson. This project is designed for GitHub portfolio use and for interviews for roles such as:

- IT Support Technician
- Airport IT Support
- NOC Analyst
- Network Support Technician
- Systems Support Analyst
- Cloud/Infrastructure Support
- Operational IT Analyst

## Simple Explanation

An airport has many different technology areas: check-in counters, gate boarding systems, baggage scanners, bag tag printers, operations users, IT admins, guest Wi-Fi, and servers. These should not all be in the same network. This lab separates each area into a different **VLAN**, then uses a router to allow only the traffic that should be allowed.

## Main Lab Topology

```text
                                  R1-AIRPORT-EDGE
                       Router-on-a-stick / DHCP / ACL firewall
                                          |
                                  G0/0 802.1Q trunk
                                          |
                                      SW1-CORE
                               Layer 2 airport access switch
       -----------------------------------------------------------------
       |          |          |           |           |          |       |
   VLAN 10    VLAN 20    VLAN 30     VLAN 40     VLAN 50    VLAN 60 VLAN 70
  CHECK-IN     GATES     BAGGAGE       OPS       IT-MGMT     GUEST  SERVERS
       |          |       |     |        |           |          |       |
 CHECKIN-PC  GATE-PC  SCANNER PRINTER  OPS-PC    IT-ADMIN  GUEST  DNS/APPS
```

For the full physical and logical topology diagrams, see:

`docs/lab-topology-design.md`

PDF version for interview preparation:

`docs/pdfs/Airport-VLAN-Project-Interview-Explanation.pdf`

## Technologies Demonstrated

- VLAN segmentation
- 802.1Q trunking
- Router-on-a-stick inter-VLAN routing
- DHCP per VLAN
- DNS design for internal airline apps
- ACLs to isolate guest Wi-Fi and protect baggage/check-in systems
- SSH device management
- Baggage scanner and bag-tag printer troubleshooting
- ITIL-style incident tickets
- GitHub-ready network documentation

## Folder Guide

```text
PROJECT-1-EVE-NG-Airport-Network/
├── README.md
├── configs/
│   ├── R1-AIRPORT-EDGE.cfg
│   └── SW1-CORE.cfg
├── docs/
│   ├── lab-topology-design.md
│   ├── ip-addressing-plan.md
│   ├── topology.md
│   └── verification-checklist.md
├── incidents/
│   └── mock-incident-tickets.md
└── runbooks/
    └── baggage-scanner-printer-troubleshooting.md
```

## VLAN and IP Summary

| VLAN | Name | Subnet | Gateway | Devices |
|---|---|---|---|---|
| 10 | CHECKIN | 10.10.10.0/24 | 10.10.10.1 | Check-in PCs |
| 20 | GATE | 10.10.20.0/24 | 10.10.20.1 | Gate/boarding PCs |
| 30 | BAGGAGE | 10.10.30.0/24 | 10.10.30.1 | Baggage scanners/printers |
| 40 | AIRPORT_OPS | 10.10.40.0/24 | 10.10.40.1 | Operations/SOCC users |
| 50 | IT_MGMT | 10.10.50.0/24 | 10.10.50.1 | Admin workstation, switch SVI |
| 60 | GUEST_WIFI | 10.10.60.0/24 | 10.10.60.1 | Guest Wi-Fi users |
| 70 | SERVERS | 10.10.70.0/24 | 10.10.70.1 | DNS, app, monitoring servers |

## Step-by-Step Build

1. Create the EVE-NG lab.
2. Add R1, SW1, and VPCS/Linux endpoints.
3. Cable the devices using `docs/lab-topology-design.md`.
4. Paste `configs/SW1-CORE.cfg` into SW1.
5. Paste `configs/R1-AIRPORT-EDGE.cfg` into R1.
6. Configure VPCS clients with `ip dhcp`.
7. Run verification commands.
8. Take screenshots for GitHub.
9. Complete incident tickets and runbook screenshots.

## Verification Commands

```cisco
show vlan brief
show interfaces trunk
show ip interface brief
show ip dhcp binding
show access-lists
show mac address-table dynamic
ping 10.10.70.10
```

## Resume Bullet

Designed and documented an EVE-NG airport IT network using VLAN segmentation, 802.1Q trunking, router-on-a-stick inter-VLAN routing, DHCP, DNS design, ACL security controls, SSH management, and troubleshooting runbooks for check-in, gate, baggage scanner/printer, operations, IT management, guest Wi-Fi, and server networks.

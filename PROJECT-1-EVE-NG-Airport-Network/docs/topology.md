# EVE-NG Topology Guide

This file gives the exact topology to build in EVE-NG. For the expanded physical/logical diagram and design explanation, see `lab-topology-design.md`.

## 1. Topology Objective

Create a small airport/airline network with separate VLANs for check-in, gate, baggage, operations, IT management, guest Wi-Fi and servers.

## 2. Physical Topology

```text
                           +------------------------------+
                           | R1-AIRPORT-EDGE              |
                           | G0/0 trunk to SW1            |
                           | DHCP + Inter-VLAN + ACLs     |
                           +---------------+--------------+
                                           |
                                           | 802.1Q trunk VLANs 10,20,30,40,50,60,70
                                           |
                           +---------------+--------------+
                           | SW1-CORE                     |
                           | Airport Layer 2 Access Switch|
                           +---------------+--------------+
         ------------------+------+------+------+------+------+------------------
         |                 |             |      |      |      |                 |
   CHECKIN-PC1        GATE-PC1   BAG-SCANNER BAG-PRINTER OPS-PC IT-ADMIN  SRV-DNS
    VLAN 10            VLAN 20      VLAN 30    VLAN 30   VLAN40  VLAN50    VLAN70
                                                                |
                                                           GUEST-LAPTOP
                                                             VLAN 60
```

## 3. Nodes to Add in EVE-NG

| Node | Suggested Image | Role |
|---|---|---|
| R1-AIRPORT-EDGE | Cisco IOSv / CSR1000v | Router-on-a-stick, ACLs, DHCP, NAT-ready edge |
| SW1-CORE | Cisco IOSvL2 / IOL L2 | VLANs, trunk, access ports |
| SRV-DNS-DHCP | Ubuntu Server / VPCS substitute | DNS/internal service testing |
| CHECKIN-PC1 | VPCS | Check-in counter test client |
| GATE-PC1 | VPCS | Gate/boarding test client |
| BAG-SCANNER1 | VPCS | Baggage scanner simulation |
| BAG-PRINTER1 | VPCS | Bag tag printer simulation |
| OPS-PC1 | VPCS | SOCC/Airport Ops user |
| IT-ADMIN-PC | VPCS | Admin workstation |
| GUEST-LAPTOP | VPCS | Guest Wi-Fi user simulation |

## 4. Cable Map

| From | Interface | To | Interface | Purpose |
|---|---|---|---|---|
| R1 | G0/0 | SW1 | G0/0 | 802.1Q trunk carrying VLAN 10-70 |
| SW1 | G0/1 | SRV-DNS-DHCP | eth0 | Server VLAN 70 |
| SW1 | G0/2 | CHECKIN-PC1 | eth0 | Check-in VLAN 10 |
| SW1 | G0/3 | GATE-PC1 | eth0 | Gate VLAN 20 |
| SW1 | G1/0 | BAG-SCANNER1 | eth0 | Baggage VLAN 30 |
| SW1 | G1/1 | BAG-PRINTER1 | eth0 | Baggage VLAN 30 |
| SW1 | G1/2 | OPS-PC1 | eth0 | Airport Ops VLAN 40 |
| SW1 | G1/3 | IT-ADMIN-PC | eth0 | IT Management VLAN 50 |
| SW1 | G2/0 | GUEST-LAPTOP | eth0 | Guest Wi-Fi VLAN 60 |

## 5. Router Subinterfaces

| Router Interface | VLAN | Gateway IP |
|---|---|---|
| G0/0.10 | 10 | 10.10.10.1 |
| G0/0.20 | 20 | 10.10.20.1 |
| G0/0.30 | 30 | 10.10.30.1 |
| G0/0.40 | 40 | 10.10.40.1 |
| G0/0.50 | 50 | 10.10.50.1 |
| G0/0.60 | 60 | 10.10.60.1 |
| G0/0.70 | 70 | 10.10.70.1 |

## 6. Design Logic

- All endpoints connect to SW1 access ports.
- R1 and SW1 connect through one trunk link.
- R1 subinterfaces become default gateways for each VLAN.
- DHCP pools on R1 give IP addresses to clients.
- ACLs on R1 restrict risky traffic.
- Guest Wi-Fi is blocked from internal airline networks.
- IT Management VLAN is used for SSH administration.

## 7. EVE-NG Build Tip

Interface names vary by Cisco image. If your image does not show the same interface names, keep the same design but adjust the config to match your actual interfaces.

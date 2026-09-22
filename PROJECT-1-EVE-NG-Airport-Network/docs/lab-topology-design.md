# Lab Topology Design — EVE-NG Airport IT Network

## 1. Simple Explanation

This lab is like a small airport terminal network. Each airport area gets its own VLAN so devices are separated and easier to secure:

- **Check-in VLAN**: counter PCs and bag-tag workstations.
- **Gate VLAN**: boarding/gate workstations and scanners.
- **Baggage VLAN**: baggage scanners and bag-tag printers.
- **Airport Operations VLAN**: operations/SOCC users.
- **IT Management VLAN**: admin workstation and network-device management.
- **Guest Wi-Fi VLAN**: passengers/guests; blocked from internal airline systems.
- **Server VLAN**: DNS, mock DCS/check-in app, mock baggage app, monitoring server.

The router connects all VLANs using **router-on-a-stick**. The switch carries all VLANs to the router over one trunk link.

## 2. Physical Topology Diagram

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
      CHECKIN-PC1         |      |      |      |      |      +---- SRV-DNS-DHCP
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

## 3. Logical VLAN Topology Diagram

```text
                           R1-AIRPORT-EDGE G0/0
        -------------------------------------------------------------------
        |         |         |         |         |         |         |
     G0/0.10   G0/0.20   G0/0.30   G0/0.40   G0/0.50   G0/0.60   G0/0.70
     VLAN 10   VLAN 20   VLAN 30   VLAN 40   VLAN 50   VLAN 60   VLAN 70
   10.10.10.1 10.10.20.1 10.10.30.1 10.10.40.1 10.10.50.1 10.10.60.1 10.10.70.1
        |         |         |         |         |         |         |
   CHECK-IN    GATES    BAGGAGE     OPS     IT MGMT   GUEST     SERVERS
   PCs/DCS   boarding   scanners    SOCC     SSH      Wi-Fi    DNS/apps
```

## 4. EVE-NG Device List

| Device | Suggested Image | Purpose |
|---|---|---|
| R1-AIRPORT-EDGE | Cisco IOSv / CSR1000v | Inter-VLAN routing, DHCP, ACLs, optional NAT later |
| SW1-CORE | Cisco IOSvL2 / Cisco IOL L2 | VLAN creation, trunking, access ports |
| SRV-DNS-DHCP | Ubuntu Server or VPCS | Mock DNS/app server in VLAN 70 |
| CHECKIN-PC1 | VPCS | Check-in counter workstation |
| GATE-PC1 | VPCS | Gate/boarding workstation |
| BAG-SCANNER1 | VPCS | Baggage scanner simulation |
| BAG-PRINTER1 | VPCS | Bag tag printer simulation; static IP recommended |
| OPS-PC1 | VPCS | Airport operations/SOCC workstation |
| IT-ADMIN-PC | VPCS | Admin workstation for SSH testing |
| GUEST-LAPTOP | VPCS | Guest Wi-Fi simulation |

## 5. Interface and Cable Map

| Link | From | Interface | To | Interface | VLAN/Mode |
|---|---|---|---|---|---|
| 1 | R1-AIRPORT-EDGE | G0/0 | SW1-CORE | G0/0 | 802.1Q trunk, VLANs 10-70 |
| 2 | SW1-CORE | G0/1 | SRV-DNS-DHCP | eth0 | Access VLAN 70 |
| 3 | SW1-CORE | G0/2 | CHECKIN-PC1 | eth0 | Access VLAN 10 |
| 4 | SW1-CORE | G0/3 | GATE-PC1 | eth0 | Access VLAN 20 |
| 5 | SW1-CORE | G1/0 | BAG-SCANNER1 | eth0 | Access VLAN 30 |
| 6 | SW1-CORE | G1/1 | BAG-PRINTER1 | eth0 | Access VLAN 30 |
| 7 | SW1-CORE | G1/2 | OPS-PC1 | eth0 | Access VLAN 40 |
| 8 | SW1-CORE | G1/3 | IT-ADMIN-PC | eth0 | Access VLAN 50 |
| 9 | SW1-CORE | G2/0 | GUEST-LAPTOP/AP | eth0 | Access VLAN 60 |

## 6. VLAN Security Policy

| Source VLAN | Allowed | Blocked |
|---|---|---|
| VLAN 10 CHECKIN | DNS, DCS/check-in server, required internal apps | Guest Wi-Fi |
| VLAN 20 GATE | DNS, DCS/boarding server, required internal apps | Guest Wi-Fi |
| VLAN 30 BAGGAGE | DNS and baggage server | Guest Wi-Fi and unnecessary lateral traffic |
| VLAN 40 AIRPORT_OPS | Internal apps and monitoring | Guest access to ops devices |
| VLAN 50 IT_MGMT | SSH/admin to network devices and servers | Not for regular users |
| VLAN 60 GUEST_WIFI | Internet only in real life; in this lab block internal 10.10.0.0/16 | All internal airport VLANs |
| VLAN 70 SERVERS | Provides DNS/app services | Should not initiate unnecessary user traffic |

## 7. Build Order

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

## 8. Screenshot Evidence for GitHub

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

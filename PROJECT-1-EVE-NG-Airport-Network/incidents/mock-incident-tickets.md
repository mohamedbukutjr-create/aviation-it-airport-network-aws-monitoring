# Mock Airline IT Incident Tickets

## INC-001 — Baggage scanner offline
Priority: P2
User: Ramp baggage lead
Symptoms: BAG-SCANNER1 cannot connect to baggage.airport.local.
Initial checks: Device has APIPA address / wrong VLAN suspected.
Resolution: Corrected switchport assignment to VLAN 30 and renewed DHCP.
Skills shown: VLAN troubleshooting, DHCP, documentation.

## INC-002 — Guest Wi-Fi can reach internal network
Priority: P1 Security
Symptoms: Guest laptop can ping 10.10.70.10.
Resolution: Applied GUEST-WIFI-IN ACL inbound on R1 G0/0.60.
Skills shown: ACL security, segmentation, verification.

## INC-003 — Gate workstation cannot reach DCS
Priority: P2
Symptoms: GATE-PC1 can ping gateway but cannot reach dcs.airport.local.
Resolution: Corrected DNS server from 8.8.8.8 to 10.10.70.10 in DHCP pool.
Skills shown: DNS/DHCP troubleshooting.

## INC-004 — Bag tag printer not printing
Priority: P2
Symptoms: CHECKIN-PC1 queue stuck for BAG-PRINTER1 at 10.10.30.50.
Resolution: Verified network path, cleared printer queue, restarted print spooler, confirmed test print.
Skills shown: Layered troubleshooting, endpoint support.

## INC-005 — IT admin cannot SSH to switch
Priority: P3
Symptoms: IT-ADMIN-PC cannot SSH to 10.10.50.2.
Resolution: Generated RSA keys, enabled SSH v2, configured VTY login local, verified VLAN50 gateway.
Skills shown: Secure management, Cisco IOS.

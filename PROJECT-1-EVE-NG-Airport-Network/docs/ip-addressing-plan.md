# IP Addressing Plan

| VLAN | Name | Subnet | Gateway | Purpose |
|---|---|---|---|---|
| 10 | CHECKIN | 10.10.10.0/24 | 10.10.10.1 | Check-in counter PCs and bag tag systems |
| 20 | GATE | 10.10.20.0/24 | 10.10.20.1 | Gate/boarding PCs and scanners |
| 30 | BAGGAGE | 10.10.30.0/24 | 10.10.30.1 | Baggage scanners and bag tag printers |
| 40 | AIRPORT_OPS | 10.10.40.0/24 | 10.10.40.1 | Airport operations/control-centre workstations |
| 50 | IT_MGMT | 10.10.50.0/24 | 10.10.50.1 | Admin workstations and network management |
| 60 | GUEST_WIFI | 10.10.60.0/24 | 10.10.60.1 | Passenger/guest Wi-Fi simulation |
| 70 | SERVERS | 10.10.70.0/24 | 10.10.70.1 | DNS, monitoring, internal app servers |

## Static Devices

| Device | IP | VLAN | Notes |
|---|---|---|---|
| SW1 management SVI | 10.10.50.2 | 50 | SSH management |
| SRV-DNS-APP | 10.10.70.10 | 70 | DNS/internal application services |
| BAG-PRINTER1 | 10.10.30.50 | 30 | Static printer IP for support scenario |

## DNS Records to Simulate

| Name | IP | Purpose |
|---|---|---|
| dcs.airport.local | 10.10.70.20 | Mock departure control/check-in app |
| baggage.airport.local | 10.10.70.30 | Mock baggage reconciliation app |
| monitor.airport.local | 10.10.70.40 | Mock monitoring dashboard |

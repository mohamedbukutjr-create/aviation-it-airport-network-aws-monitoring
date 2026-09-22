# Baggage Scanner and Bag Tag Printer Troubleshooting Runbook

## Scenario
A baggage scanner or bag tag printer at the airport counter/ramp cannot connect to the baggage application or cannot print bag tags.

## Common Symptoms
- Scanner shows offline.
- Bag tag printer not reachable by IP.
- Printer queue stuck.
- Device receives wrong IP address.
- Scanner works near one AP but not another.
- Baggage application cannot resolve DNS name.

## Step 1 — Identify Device and Network
Record:
- Device type: scanner, bag tag printer, workstation, AP
- Asset tag / hostname
- MAC address
- Switch port
- VLAN
- IP address
- Gateway
- DNS server

## Step 2 — Check Physical Layer
- Confirm power.
- Confirm Ethernet cable is connected.
- Check link light.
- Try known-good cable.
- If wireless scanner, confirm SSID and signal strength.

## Step 3 — Check IP Settings
Expected baggage VLAN:
- VLAN: 30
- Subnet: 10.10.30.0/24
- Gateway: 10.10.30.1
- DNS: 10.10.70.10
- Static printer example: 10.10.30.50

Commands:
```cisco
show vlan brief
show mac address-table dynamic
show interface status
show ip dhcp binding
```

## Step 4 — Test Connectivity
From router:
```cisco
ping 10.10.30.50
show arp | include 10.10.30.50
show access-lists BAGGAGE-IN
```

From client:
```text
ping 10.10.30.1
ping 10.10.70.10
ping 10.10.70.30
```

## Step 5 — Check DNS
Confirm baggage app name resolves:
```text
baggage.airport.local -> 10.10.70.30
```

## Step 6 — Printer-Specific Checks
- Confirm correct printer driver.
- Confirm printer IP did not change.
- Clear stuck queue.
- Restart print spooler on workstation.
- Test print locally.
- Check label size / media / ribbon.

## Step 7 — Scanner-Specific Checks
- Confirm Wi-Fi profile or Ethernet VLAN.
- Confirm scanner can reach gateway.
- Confirm application login works.
- Reboot scanner only after documenting current status.

## Step 8 — Escalation
Escalate to Network/NOC if:
- Multiple devices in VLAN 30 fail.
- Trunk or subinterface is down.
- DHCP scope is exhausted.
- ACL counters show unexpected denies.

Escalate to Application Support if:
- Network tests pass but baggage app fails.
- Authentication/API errors occur.
- Multiple airports report same app issue.

## Closure Note Template
Resolved by identifying incorrect switchport VLAN assignment. Moved port G1/0 to VLAN 30, renewed DHCP lease, verified scanner received 10.10.30.x address, confirmed ping to gateway and baggage server, and user confirmed successful bag scan.

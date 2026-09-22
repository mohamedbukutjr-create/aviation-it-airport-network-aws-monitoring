# Verification Checklist

## Switch Checks
```cisco
show vlan brief
show interfaces trunk
show ip interface brief
show mac address-table dynamic
show running-config interface g0/0
```

Expected:
- VLANs 10,20,30,40,50,60,70 exist.
- G0/0 is trunking.
- Access ports are in correct VLANs.
- VLAN50 SVI is up with IP 10.10.50.2.

## Router Checks
```cisco
show ip interface brief
show running-config | section dhcp
show ip dhcp binding
show access-lists
show ip route connected
```

Expected:
- Subinterfaces G0/0.10 through G0/0.70 are up/up.
- DHCP bindings appear after VPCS clients request DHCP.
- ACL hit counters increase during tests.

## Client Tests
From VPCS:
```text
ip dhcp
show ip
ping 10.10.10.1
ping 10.10.70.10
ping 10.10.50.1
```

## Security Tests
- Guest VLAN should NOT reach internal VLANs.
- IT_MGMT should be able to SSH to R1 and SW1.
- Baggage VLAN should reach baggage server/DNS but not guest Wi-Fi.

## Troubleshooting Questions
1. Is the access port in the correct VLAN?
2. Is the trunk allowing that VLAN?
3. Is the router subinterface up/up?
4. Is DHCP configured for the right subnet?
5. Is an ACL blocking traffic?
6. Is DNS pointed to 10.10.70.10?

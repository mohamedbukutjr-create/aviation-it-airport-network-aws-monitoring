# Mock AWS Cloud Incident Tickets

## AWS-INC-001 — Airline dashboard unavailable
Priority: P2
Symptoms: Ops team cannot access mock airline dashboard.
Checks: EC2 status, security group, route table, HTTP service.
Resolution: Started stopped web service and verified CloudWatch metrics.

## AWS-INC-002 — High CPU alarm
Priority: P2
Symptoms: CloudWatch alarm triggered above 70% CPU.
Checks: CPU metrics, logs, process list, recent changes.
Resolution: Identified test load, documented false-positive and adjusted runbook.

## AWS-INC-003 — SNS alert not received
Priority: P3
Symptoms: Alarm entered ALARM state but no email received.
Checks: SNS subscription confirmation, alarm action ARN, email spam folder.
Resolution: Confirmed SNS subscription and retested alarm notification.

## AWS-INC-004 — SSH blocked
Priority: P3
Symptoms: Admin cannot SSH to EC2.
Checks: Security group, public IP, route table, key pair, NACL.
Resolution: Corrected admin CIDR in Terraform variables and reapplied.

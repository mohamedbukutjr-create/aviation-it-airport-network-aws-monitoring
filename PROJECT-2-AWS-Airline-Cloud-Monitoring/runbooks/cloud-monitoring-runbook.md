# Cloud Monitoring Runbook

## Alert: Mock Airline App High CPU
Priority: P2

### Triage
1. Check CloudWatch alarm state.
2. Check EC2 instance status checks.
3. Review CPUUtilization metric for 1 hour.
4. Check application logs.
5. Confirm if users report slow check-in/baggage dashboard.

### Commands
```bash
aws cloudwatch describe-alarms --alarm-names mock-airline-app-high-cpu
aws ec2 describe-instance-status --include-all-instances
```

### Resolution Options
- Restart application service if hung.
- Scale instance size only with approval.
- Roll back recent deployment if issue started after change.
- Escalate if security incident suspected.

## Alert: App Unreachable
1. Confirm instance running.
2. Confirm security group inbound rules.
3. Confirm route table has 0.0.0.0/0 to IGW.
4. Confirm web service status.
5. Confirm DNS if using Route 53.

## Closure Template
Resolved by correcting security group source CIDR to allow only admin public IP, verified HTTP access, checked CloudWatch dashboard, and documented incident timeline.

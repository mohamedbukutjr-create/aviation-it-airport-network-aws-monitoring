# AWS Step-by-Step Guide

## Prerequisites
- AWS account
- IAM user or role with permissions for VPC, EC2, CloudWatch, SNS
- AWS CLI configured
- Terraform installed

## Safety
AWS can charge money. Use free-tier resources where possible and destroy resources after testing.

## Step 1 — Configure AWS CLI
```bash
aws configure
aws sts get-caller-identity
```

## Step 2 — Review Terraform Variables
Edit `terraform/variables.tf` or create `terraform.tfvars`:
```hcl
aws_region = "ca-central-1"
az = "ca-central-1a"
allowed_admin_cidr = "YOUR_PUBLIC_IP/32"
create_ec2 = false
```

Keep `create_ec2=false` until you choose a valid Amazon Linux AMI.

## Step 3 — Initialize Terraform
```bash
cd PROJECT-2-AWS-Airline-Cloud-Monitoring/terraform
terraform init
terraform validate
terraform plan
```

## Step 4 — Deploy Network and Monitoring Shell
```bash
terraform apply
```

## Step 5 — Optional EC2 Deployment
Find an Amazon Linux 2023 AMI for your region, set:
```hcl
create_ec2 = true
ami_id = "ami-xxxxxxxx"
```
Then:
```bash
terraform plan
terraform apply
```

## Step 6 — Verify CloudWatch
- Open CloudWatch Dashboards.
- Find `Aviation-IT-Operations-Dashboard`.
- Confirm SNS topic exists.
- If EC2 is enabled, check EC2 CPU metrics.

## Step 7 — Simulate Incident
Example incident: mock app unavailable.
Checks:
1. Is EC2 running?
2. Is security group allowing your IP?
3. Is HTTPD running?
4. Is route table connected to internet gateway?
5. Are CloudWatch metrics/logs present?

## Step 8 — Destroy Resources
```bash
terraform destroy
```

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ca-central-1"
}

variable "az" {
  description = "Availability zone"
  type        = string
  default     = "ca-central-1a"
}

variable "allowed_admin_cidr" {
  description = "Your public IP CIDR for SSH/HTTP testing, e.g. 203.0.113.10/32. Do not leave 0.0.0.0/0 for real use."
  type        = string
  default     = "0.0.0.0/0"
}

variable "create_ec2" {
  description = "Set true to deploy EC2 after choosing a valid AMI ID"
  type        = bool
  default     = false
}

variable "ami_id" {
  description = "Amazon Linux 2023 AMI ID for your region"
  type        = string
  default     = "ami-PLACEHOLDER"
}

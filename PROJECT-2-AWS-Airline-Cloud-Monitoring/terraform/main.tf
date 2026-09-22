terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "airport" {
  cidr_block           = "10.20.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = { Name = "aviation-it-vpc" }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.airport.id
  cidr_block              = "10.20.10.0/24"
  map_public_ip_on_launch = true
  availability_zone       = var.az
  tags = { Name = "aviation-public-subnet" }
}

resource "aws_subnet" "private_ops" {
  vpc_id            = aws_vpc.airport.id
  cidr_block        = "10.20.20.0/24"
  availability_zone = var.az
  tags = { Name = "aviation-private-ops-subnet" }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.airport.id
  tags = { Name = "aviation-igw" }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.airport.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
  tags = { Name = "aviation-public-rt" }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

resource "aws_security_group" "app_sg" {
  name        = "aviation-app-sg"
  description = "Allow HTTP and SSH for lab testing"
  vpc_id      = aws_vpc.airport.id

  ingress {
    description = "HTTP demo app"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [var.allowed_admin_cidr]
  }

  ingress {
    description = "SSH admin only"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_admin_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "aviation-app-sg" }
}

resource "aws_sns_topic" "alerts" {
  name = "aviation-it-alerts"
}

resource "aws_cloudwatch_log_group" "app" {
  name              = "/aviation-it/mock-airline-app"
  retention_in_days = 7
}

# EC2 is intentionally optional. Set create_ec2=true only when ready to deploy.
resource "aws_instance" "app" {
  count                       = var.create_ec2 ? 1 : 0
  ami                         = var.ami_id
  instance_type               = "t3.micro"
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.app_sg.id]
  associate_public_ip_address = true
  user_data = file("${path.module}/user_data.sh")
  tags = { Name = "mock-airline-ops-app" }
}

resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  count               = var.create_ec2 ? 1 : 0
  alarm_name          = "mock-airline-app-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 60
  statistic           = "Average"
  threshold           = 70
  alarm_description   = "High CPU on mock airline app server"
  alarm_actions       = [aws_sns_topic.alerts.arn]
  dimensions = {
    InstanceId = aws_instance.app[0].id
  }
}

resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "Aviation-IT-Operations-Dashboard"
  dashboard_body = jsonencode({
    widgets = [
      {
        type = "text",
        x = 0, y = 0, width = 24, height = 3,
        properties = { markdown = "# Aviation IT Operations Dashboard\nMock airline app monitoring: EC2 health, CPU, logs, and incident response." }
      }
    ]
  })
}

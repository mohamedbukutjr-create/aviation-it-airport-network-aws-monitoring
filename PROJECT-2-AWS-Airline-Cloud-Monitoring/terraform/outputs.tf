output "vpc_id" { value = aws_vpc.airport.id }
output "public_subnet_id" { value = aws_subnet.public.id }
output "private_ops_subnet_id" { value = aws_subnet.private_ops.id }
output "sns_topic_arn" { value = aws_sns_topic.alerts.arn }
output "dashboard_name" { value = aws_cloudwatch_dashboard.main.dashboard_name }
output "app_public_ip" {
  value = var.create_ec2 ? aws_instance.app[0].public_ip : "EC2 disabled"
}

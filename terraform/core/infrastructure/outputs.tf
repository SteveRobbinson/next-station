output "workspace_url" {
  value = databricks_mws_workspaces.this.workspace_url
}

output "workspace_id" {
  value = databricks_mws_workspaces.this.workspace_id
}

output "vpc_id" {
  value = aws_vpc.databricks_vpc.id
}

output "public_subnet_id" {
  value = aws_subnet.public_subnet.id
}

output "private_subnet_ids" {
  value = [aws_subnet.private_subnet_a.id, aws_subnet.private_subnet_b.id]
}

output "private_rt_id" {
  value = aws_route_table.private_rt.id
}

output "cross_account_role_arn" {
  value = aws_iam_role.cross_account.arn
}

output "workspace_name" {
  value = var.workspace_name
}

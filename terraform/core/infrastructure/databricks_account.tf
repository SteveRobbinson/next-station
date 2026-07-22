resource "databricks_mws_storage_configurations" "this" {
  provider                   = databricks.mws
  account_id                 = var.databricks_account_id
  bucket_name                = var.root_bucket_name
  storage_configuration_name = "${var.workspace_name}-storage"

  depends_on = [aws_s3_bucket_policy.root_storage_policy]
}

resource "databricks_mws_credentials" "this" {
  provider         = databricks.mws
  account_id       = var.databricks_account_id
  credentials_name = "${var.workspace_name}-credentials"
  role_arn         = aws_iam_role.cross_account.arn
}


resource "databricks_mws_networks" "this" {
  provider           = databricks.mws
  account_id         = var.databricks_account_id
  network_name       = "${var.workspace_name}-network"
  vpc_id             = aws_vpc.databricks_vpc.id
  subnet_ids         = [aws_subnet.private_subnet_a.id, aws_subnet.private_subnet_b.id]
  security_group_ids = [aws_security_group.databricks_sg.id]
  depends_on = [
    aws_route_table_association.private_assoc_a,
    aws_route_table_association.private_assoc_b
  ]
}

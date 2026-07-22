resource "random_string" "unique_suffix" {
  length  = 6
  special = false
  upper   = false
}


resource "databricks_mws_workspaces" "this" {

  provider       = databricks.mws
  account_id     = var.databricks_account_id
  aws_region     = var.aws_region
  workspace_name = var.workspace_name

  credentials_id           = databricks_mws_credentials.this.credentials_id
  storage_configuration_id = databricks_mws_storage_configurations.this.storage_configuration_id
  network_id               = databricks_mws_networks.this.network_id

  pricing_tier = "PREMIUM"
}


resource "databricks_sql_endpoint" "this" {
  provider                  = databricks.workspace
  name                      = "SQL Warehouse ${var.workspace_name}-${random_string.unique_suffix.result}"
  cluster_size              = "Small"
  min_num_clusters          = 1
  max_num_clusters          = 2
  auto_stop_mins            = 15
  warehouse_type            = "PRO"
  enable_serverless_compute = true
}

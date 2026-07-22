resource "databricks_mws_workspaces" "this" {

  provider       = databricks.mws
  account_id     = var.databricks_account_id
  aws_region     = var.aws_region
  workspace_name = var.workspace_name

  credentials_id           = data.terraform_remote_state.infrastructure.outputs.credentials_id
  storage_configuration_id = data.terraform_remote_state.infrastructure.outputs.storage_configuration_id
  network_id               = data.terraform_remote_state.infrastructure.outputs.network_id

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

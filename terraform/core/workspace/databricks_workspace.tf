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


resource "databricks_mws_permission_assignment" "add_user" {
  provider     = databricks.mws
  workspace_id = databricks_mws_workspaces.this.workspace_id
  principal_id = data.terraform_remote_state.infrastructure.outputs.databricks_user_id
  permissions  = ["ADMIN"]
}

resource "databricks_service_principal" "github_actions" {
  provider     = databricks.mws
  display_name = var.gh_actions_service_principal
}


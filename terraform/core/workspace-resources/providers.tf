terraform {
  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.121.0"
    }
  }
  required_version = ">= 1.5.0"
}

provider "databricks" {
  alias         = "workspace"
  host          = data.terraform_remote_state.workspace.outputs.workspace_url
  client_id     = var.databricks_client_id
  client_secret = var.databricks_client_secret
}

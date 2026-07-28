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
  alias   = "workspace"
  host    = data.terraform_remote_state.workspace.outputs.workspace_url
  profile = "account"
}

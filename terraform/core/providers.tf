terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.54.0"
    }
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.121.0"
    }
  }
  required_version = ">= 1.5.0"
}

provider "aws" {
  region = var.aws_region
}

provider "databricks" {
  alias         = "mws"
  host          = "https://accounts.cloud.databricks.com"
  account_id    = var.databricks_account_id
  client_id     = var.databricks_client_id
  client_secret = var.databricks_client_secret
}

provider "databricks" {
  alias         = "workspace"
  host          = databricks_mws_workspaces.this.workspace_url
  client_id     = var.databricks_client_id
  client_secret = var.databricks_client_secret
}

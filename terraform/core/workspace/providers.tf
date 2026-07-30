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

provider "databricks" {
  alias      = "mws"
  host       = "https://accounts.cloud.databricks.com"
  account_id = var.databricks_account_id
}

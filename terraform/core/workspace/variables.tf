variable "databricks_account_id" {
  type = string
}

variable "databricks_client_id" {
  type = string
}

variable "databricks_client_secret" {
  type      = string
  sensitive = true
}

variable "aws_region" {
  type    = string
  default = "eu-central-1"
}

variable "workspace_name" {
  type = string
}

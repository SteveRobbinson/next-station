variable "databricks_account_id" {
  type = string
}

variable "aws_region" {
  type    = string
  default = "eu-central-1"
}

variable "workspace_name" {
  type = string
}

variable "gh_actions_service_principal" {
  type = string
}

variable "github_org" {
  type = string
}

variable "github_repo" {
  type = string
}

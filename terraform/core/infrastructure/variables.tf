variable "databricks_admin_email" {
  type = string
}

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

variable "aws_account_id" {
  type = string
}

variable "cross_account_role_name" {
  type = string
}

variable "root_bucket_name" {
  type = string
}

variable "vpc_cidr" {
  type = string
}

variable "public_subnet_cidr" {
  type = string
}

variable "private_subnet_a_cidr" {
  type = string
}

variable "private_subnet_b_cidr" {
  type = string
}

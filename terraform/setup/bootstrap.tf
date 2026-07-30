resource "databricks_service_principal" "github_actions" {
  provider     = databricks.mws
  display_name = var.gh_actions_service_principal
}

resource "databricks_service_principal_federation_policy" "this" {
  provider             = databricks.mws
  service_principal_id = databricks_service_principal.github_actions.id
  policy_id            = "github-actions-policy"
  oidc_policy = {
    "issuer" : "https://token.actions.githubusercontent.com",
    "subject" : "repo:${var.github_org}/${var.github_repo}:environment:prod"
  }
}

resource "databricks_service_principal_role" "tf_admin_account" {
  service_principal_id = databricks_service_principal.github_actions.id
  role                 = "account_admin"
}

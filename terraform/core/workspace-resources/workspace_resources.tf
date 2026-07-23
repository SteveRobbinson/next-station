data "databricks_sql_warehouse" "starter" {
  provider = databricks.workspace
  name     = "Serverless Starter Warehouse"
}


import {
  to = databricks_sql_endpoint.starter
  id = data.databricks_sql_warehouse.starter.id
}


resource "databricks_sql_endpoint" "starter" {
  provider                  = databricks.workspace
  name                      = "Serverless Starter Warehouse"
  cluster_size              = "Small"
  min_num_clusters          = 1
  max_num_clusters          = 2
  auto_stop_mins            = 15
  warehouse_type            = "PRO"
  enable_serverless_compute = true
}


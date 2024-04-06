locals {
  pool_name = "fiap-user-pool"
  resource_server_name = "fiap-resource-server"
  resource_server_id = "https://fiap-api-${var.environment}.resource-server.com"
}

resource "aws_cognito_user_pool" "pool" {
  name = local.pool_name
}

resource "aws_cognito_resource_server" "resource" {
  identifier = local.resource_server_id
  name       = local.resource_server_name

  user_pool_id = aws_cognito_user_pool.pool.id
}

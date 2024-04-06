locals {
  pool_name            = "fiap-user-pool"
  domain_name          = "fiap-api-${var.environment}"
  resource_server_name = "fiap-resource-server"
  resource_server_id   = "https://fiap-api-${var.environment}.resource-server.com"
}

resource "aws_cognito_user_pool" "this" {
  name = local.pool_name
}

resource "aws_cognito_resource_server" "this" {
  identifier   = local.resource_server_id
  name         = local.resource_server_name
  user_pool_id = aws_cognito_user_pool.this.id

  scope {
    scope_name        = "all"
    scope_description = "Get access to all API Gateway endpoints."
  }
}

resource "aws_cognito_user_pool_domain" "main" {
  domain       = local.domain_name
  user_pool_id = aws_cognito_user_pool.this.id
}

resource "aws_cognito_user_pool_client" "client" {
  name                                 = "DefaultUser"
  user_pool_id                         = aws_cognito_user_pool.this.id
  generate_secret                      = true
  allowed_oauth_flows                  = ["code", "implicit", "client_credentials"]
  supported_identity_providers         = ["COGNITO"]
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes                 = aws_cognito_resource_server.this.scope_identifiers

  depends_on = [
    aws_cognito_user_pool.this,
    aws_cognito_resource_server.this,
  ]
}

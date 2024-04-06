output "lambda_invoke_arn" {
  value = aws_lambda_function.fiap_api.invoke_arn
}

output "scope_identifiers" {
  value = aws_cognito_resource_server.this.scope_identifiers
}
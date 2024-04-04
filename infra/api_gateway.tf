resource "aws_apigatewayv2_api" "lambda" {
  name          = "fiap-api-gw-${var.environment}"
  protocol_type = "HTTP"
}

resource "aws_cloudwatch_log_group" "api_gw" {
  name = "/aws/api_gw/${aws_apigatewayv2_api.lambda.name}"
  retention_in_days = 7
}

resource "aws_apigatewayv2_stage" "lambda" {
  api_id = aws_apigatewayv2_api.lambda.id

  name        = var.environment
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw.arn

    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }
}

#resource "aws_apigatewayv2_integration" "hello_world" {
#  api_id = aws_apigatewayv2_api.lambda.id
#  integration_uri    = aws_lambda_function.fiap_api.invoke_arn
#  integration_type   = "AWS_PROXY"
#  integration_method = "POST"
#}
#
#resource "aws_apigatewayv2_route" "hello_world" {
#  api_id = aws_apigatewayv2_api.lambda.id
#
#  route_key = "GET /hello"
#  target    = "integrations/${aws_apigatewayv2_integration.hello_world.id}"
#}





resource "aws_apigatewayv2_integration" "lambda" {
  api_id           = aws_apigatewayv2_api.lambda.id
  integration_type = "HTTP_PROXY"
  integration_method = "ANY"
#  integration_uri    = aws_lambda_function.fiap_api.invoke_arn
  integration_uri    = "arn:aws:apigateway:${local.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.fiap_api.arn}/invocations"
}

resource "aws_apigatewayv2_route" "example" {
  api_id    = aws_apigatewayv2_api.lambda.id
  route_key = "ANY /{proxy+}"
  target = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}









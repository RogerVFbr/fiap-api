# https://hands-on.cloud/terraform-deploy-python-lambda-container-image/

locals {
  media_lambda_name = "fiap-api-${var.environment}"
}

resource "aws_cloudwatch_log_group" "fiap_api" {
  name              = "/aws/lambda/${local.media_lambda_name}"
  retention_in_days = 7
}

resource "aws_lambda_function" "fiap_api" {
  depends_on = [
    null_resource.ecr_image,
    aws_cloudwatch_log_group.fiap_api
  ]
  function_name = local.media_lambda_name
  role          = aws_iam_role.fiap_api.arn
  kms_key_arn   = aws_kms_key.fiap_api.arn
  timeout       = 30
  memory_size   = "2048"
  description   = "FIAP Api Lambda"
  image_uri     = "${aws_ecr_repository.repo.repository_url}@${data.aws_ecr_image.lambda_image.id}"
  package_type  = "Image"
  publish       = true

  # snap_start {
  #   apply_on ="PublishedVersions"
  # }

  environment {
    variables = {
      IS_LOCAL    = "false"
      ENVIRONMENT = var.environment
      BUCKET_NAME = "${var.bucket_name}-${var.environment}"
      AWS_LWA_ASYNC_INIT = "true"
    }
  }
}

resource "aws_lambda_alias" "this" {
  name             = var.environment
  description      = "Alias for SnapStart"
  function_name    = aws_lambda_function.fiap_api.function_name
  function_version = aws_lambda_function.fiap_api.version
}

resource "aws_lambda_permission" "allow_api_gateway" {
  function_name = aws_lambda_function.fiap_api.function_name
  statement_id  = "AllowExecutionFromApiGateway"
  action        = "lambda:InvokeFunction"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.api.execution_arn}/*/*/*"
  qualifier     = aws_lambda_alias.this.name
  depends_on    = [
    aws_api_gateway_resource.proxy
  ]
}
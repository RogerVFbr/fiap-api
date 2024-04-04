# https://hands-on.cloud/terraform-deploy-python-lambda-container-image/

locals {
  media_lambda_name = "fiap-api-${var.environment}"
}

resource "aws_cloudwatch_log_group" "media_lambda_log_group" {
  name = "/aws/lambda/${local.media_lambda_name}"
  retention_in_days = 7
}

resource "aws_lambda_function" "image_post_lambda_container" {
  depends_on = [
    null_resource.ecr_image,
    aws_cloudwatch_log_group.media_lambda_log_group
  ]
  function_name = local.media_lambda_name
  role = aws_iam_role.fiap_api.arn
  kms_key_arn = aws_kms_key.fiap_api.arn
  timeout = 5
  memory_size = "512"
  description = "FIAP Api Lambda"
  image_uri = "${aws_ecr_repository.repo.repository_url}@${data.aws_ecr_image.lambda_image.id}"
  package_type = "Image"

  environment {
    variables = {
      IS_LOCAL = "false"
      ENVIRONMENT = var.environment
    }
  }
}

#resource "aws_lambda_permission" "image_post_lambda_events" {
#  statement_id = "AllowExecutionFromEventbridgeScheduler"
#  action = "lambda:InvokeFunction"
#  function_name = aws_lambda_function.image_post_lambda_container.function_name
#  principal = "scheduler.amazonaws.com"
#}
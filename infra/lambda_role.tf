resource "aws_iam_role" "fiap_api" {
  name               = "RoleforFiapApiLambda-${var.environment}"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "lambda_logging" {
  name        = "fiap_api_lambda_logging_${var.environment}"
  path        = "/"
  description = "IAM policy for logging from a lambda"
  policy      = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.fiap_api.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

#resource "aws_iam_policy" "lambda_s3" {
#  name        = "fiap_api_lambda_s3_${var.environment}"
#  path        = "/"
#  description = "IAM policy for reading/writing to S3 from a lambda"
#
#  policy = <<EOF
#{
#    "Version": "2012-10-17",
#    "Statement": [
#        {
#            "Sid": "ListObjectsInBucket",
#            "Effect": "Allow",
#            "Action": "s3:ListBucket",
#            "Resource": "arn:aws:s3:::${var.data_bucket_name}"
#        },
#        {
#            "Sid": "AllObjectActions",
#            "Effect": "Allow",
#            "Action": "s3:*Object",
#            "Resource": "arn:aws:s3:::${var.data_bucket_name}/*"
#        }
#    ]
#}
#EOF
#}
#
#resource "aws_iam_role_policy_attachment" "lambda_s3" {
#  role       = aws_iam_role.fiap_api.name
#  policy_arn = aws_iam_policy.lambda_s3.arn
#}

resource "aws_iam_policy" "lambda_parameter_store" {
  name        = "fiap_api_lambda_parameter_store_${var.environment}"
  path        = "/"
  description = "IAM policy for reading from Parameter Store from a lambda"
  policy      = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowGetParameter",
            "Effect": "Allow",
            "Action": "ssm:GetParameter",
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "parameter_store" {
  role       = aws_iam_role.fiap_api.name
  policy_arn = aws_iam_policy.lambda_parameter_store.arn
}

#resource "aws_iam_policy" "lambda_sns" {
#  name        = "lambda_sns_${var.environment}"
#  path        = "/"
#  description = "IAM policy for accessing SNS from a lambda"
#
#  policy = <<EOF
#{
#    "Version": "2012-10-17",
#    "Statement": [
#        {
#            "Effect": "Allow",
#            "Action": [
#              "sns:Publish",
#              "sns:Subscribe",
#              "sns:CreateTopic",
#              "sns:GetTopicAttributes",
#              "sns:SetTopicAttributes",
#              "sns:TagResource",
#              "sns:UntagResource",
#              "sns:ListTagsForResource",
#              "sns:ListSubscriptionsByTopic"
#            ],
#            "Resource": [
#              "arn:aws:sns:${local.region}:${local.account_id}:*"
#            ]
#        }
#    ]
#}
#EOF
#}
#
#resource "aws_iam_role_policy_attachment" "sns" {
#  role       = aws_iam_role.fiap_api.name
#  policy_arn = aws_iam_policy.lambda_sns.arn
#}
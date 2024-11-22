locals {
  ecr_repository_name = "fiap-repo-${var.environment}"
  ecr_image_tag       = "latest"
  ecr_slim_image_tag  = "slim"
  app_dir             = "../app"
}

resource "aws_ecr_repository" "repo" {
  name = local.ecr_repository_name
}

resource "aws_ecr_lifecycle_policy" "policy" {
  repository = aws_ecr_repository.repo.name
  policy     = <<EOF
{
    "rules": [
        {
            "rulePriority": 1,
            "description": "Keep last 1 image(s)",
            "selection": {
                "tagStatus": "any",
                "countType": "imageCountMoreThan",
                "countNumber": 1
            },
            "action": {
                "type": "expire"
            }
        }
    ]
}
EOF
}

data "archive_file" "init" {
  type        = "zip"
  source_dir  = local.app_dir
  output_path = "application_zip_for_hashing.zip"
}

resource "null_resource" "ecr_image" {
  triggers = {
    src_hash = data.archive_file.init.output_sha
  }

  # provisioner "local-exec" {
  #   command = <<EOF
  #     aws ecr get-login-password --region ${local.region} | docker login --username AWS --password-stdin ${local.account_id}.dkr.ecr.${local.region}.amazonaws.com
  #     cd ${local.app_dir}
  #     docker build -t ${aws_ecr_repository.repo.repository_url}:${local.ecr_image_tag} .
  #     docker push ${aws_ecr_repository.repo.repository_url}:${local.ecr_image_tag}
  #     EOF
  # }
  provisioner "local-exec" {
    command = <<EOF
      aws ecr get-login-password --region ${local.region} | docker login --username AWS --password-stdin ${local.account_id}.dkr.ecr.${local.region}.amazonaws.com
      cd ${local.app_dir}
      echo "Building image ..."
      docker build -t ${aws_ecr_repository.repo.repository_url}:${local.ecr_image_tag} .
      echo "Slim build ..."
      slim build --http-probe=false --tag ${aws_ecr_repository.repo.repository_url}:${local.ecr_slim_image_tag} ${aws_ecr_repository.repo.repository_url}:${local.ecr_image_tag}
      docker image ls
      echo "Pushing image ..."
      docker push ${aws_ecr_repository.repo.repository_url}:${local.ecr_slim_image_tag}
      EOF
  }
}

data "aws_ecr_image" "lambda_image" {
  depends_on      = [
    null_resource.ecr_image
  ]
  repository_name = local.ecr_repository_name
  image_tag       = local.ecr_slim_image_tag
}
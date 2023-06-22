terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

data "aws_iam_role" "lambda_role" {
  name = "AWSRoleForStudyLambda"
}

data "archive_file" "lambda_zip" {
  type = "zip"
  output_path = "${path.module}/neo-sentinel.zip"
  source_dir = "${path.module}"
}

resource "aws_lambda_function" "lambda_function" {
  filename = "neo-sentinel.zip"
  function_name = "lambda_function"
  role = data.aws_iam_role.lambda_role.arn
  handler = "lambda_handler"
  runtime = "python3.10"
}

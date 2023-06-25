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
  output_path = "/home/misteryoh/Coding/Git/neo-sentinel.zip"
  source_dir = "/home/misteryoh/Coding/Git/neo-sentinel"
}

resource "aws_lambda_function" "lambda_function" {
  filename = "/home/misteryoh/Coding/Git/neo-sentinel.zip"
  function_name = "lambda-neo-sentinel-getdata"
  role = data.aws_iam_role.lambda_role.arn
  handler = "lambda_handler"
  runtime = "python3.10"
}

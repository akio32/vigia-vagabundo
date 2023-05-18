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
  name = "AWSRoleForLambdaFgvEmissions"
}

data "archive_file" "lambda_zip" {
  type = "zip"
  source_file = "lambda_function.py"
  output_path = "neo-sentinel.zip"
}

resource "aws_lambda_function" "lambda_function" {
  filename = "neo-sentinel.zip"
  function_name = "neo-sentinel"
  role = aws_iam_role.lambda_role.arn
  handler = "lambda_handler"
  runtime = "python3.11"
}

# resource "aws_instance" "app_server" {
#  ami           = "ami-0da62eb5869c785b9"
#  instance_type = "t2.micro"
#
#  tags = {
#    Name = "ExampleAppServerInstance"
#  }
# }


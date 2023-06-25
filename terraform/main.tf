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
  source_dir = "../../neo-sentinel"
  output_path = "../../neo-sentinel/neo-sentinel.zip"
  
  excludes = [
    "terraform",
    "site-packages",
    ".git",
    ".github",
    ".gitignore",
    "site-packages.zip",
    "neo-sentinel.zip"
  ]
}

data "archive_file" "lambda_layer_zip" {
  type        = "zip"
  source_dir  = "../site-packages"
  output_path = "../../neo-sentinel/lambda_layer.zip"

  depends_on = [
    "null_resource.lambda_layer"
  ]
}

resource "null_resource" "lambda_layer" {
  triggers = {
    timestamp = timestamp()
  }

  provisioner "local-exec" {
    command = <<EOF
      mkdir site-packages
      pip install \
          -r ./requirements.txt \
          --platform linux_x86_64 \
          --target ./site-packages/python \
          --implementation cp \
          --python-version 3.10 \
          --only-binary=:all: --upgrade
    EOF
    working_dir = "../"
  }
}

resource "aws_lambda_layer_version" "lambda_layer" {
  filename   = data.archive_file.lambda_layer_zip.output_path
  layer_name = "dependencies-layer"
  compatible_runtimes = ["python3.10"]
}

resource "aws_lambda_function" "lambda_function" {
  filename = "../neo-sentinel.zip"
  description = "Função lambda para capturar os dados da API da Camara dos Deputados"
  function_name = "lambda-neo-sentinel-getdata"
  role = data.aws_iam_role.lambda_role.arn
  handler = "lambda_function.lambda_handler"
  runtime = "python3.10"
  memory_size = 128
  timeout = 900
  layers = [aws_lambda_layer_version.lambda_layer.arn]
}
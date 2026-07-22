terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                      = var.aws_region
  access_key                  = "test"
  secret_key                  = "test"
  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true



  endpoints {
    s3       = var.localstack_endpoint
    sqs      = var.localstack_endpoint
    dynamodb = var.localstack_endpoint
  }
}


resource "aws_s3_bucket" "notes_storage" {
  bucket = var.bucket_name
}

resource "aws_sqs_queue" "notes_events" {
  name = var.queue_name
}


resource "aws_dynamodb_table" "notes_table" {
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "note_id"

  attribute {
    name = "note_id"
    type = "S"
  }
}


moved {
  from = aws_s3_bucket.notes
  to   = aws_s3_bucket.notes_storage
}


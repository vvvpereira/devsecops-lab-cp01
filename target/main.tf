provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "insecure_bucket" {
  bucket        = "meu-bucket-devsecops-inseguro"
  force_destroy = true
}

# Vulnerabilidade IaC: Bucket publicamente legível
resource "aws_s3_bucket_acl" "insecure_acl" {
  bucket = aws_s3_bucket.insecure_bucket.id
  acl    = "public-read"
}


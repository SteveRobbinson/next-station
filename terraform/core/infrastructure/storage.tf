resource "aws_s3_bucket" "root_storage" {
  bucket        = var.root_bucket_name
  force_destroy = true

  tags = {
    Name    = var.root_bucket_name
    Project = "next-station"
  }
}


resource "aws_s3_bucket_public_access_block" "root_storage_pab" {
  bucket                  = aws_s3_bucket.root_storage.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}


resource "aws_s3_bucket_policy" "root_storage_policy" {
  bucket = aws_s3_bucket.root_storage.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "GrantDatabricksAccess"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::414351767826:root"
        }
        Action = [
          "s3:GetObject",
          "s3:GetObjectVersion",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket",
          "s3:GetBucketLocation"
        ]
        Resource = [
          aws_s3_bucket.root_storage.arn,
          "${aws_s3_bucket.root_storage.arn}/*"
        ]
      }
    ]
  })
  depends_on = [aws_s3_bucket_public_access_block.root_storage_pab]
}

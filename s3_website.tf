resource "aws_s3_bucket" "s3_website" {
  bucket = "chatoverflow-website"
  acl    = "public-read"
  
  website {
    index_document = "index.html"
  }
}

resource "aws_s3_object" "s3_website_html" {
  bucket = aws_s3_bucket.s3_website.id
  key    = "index.html"
  source = "search_test_website/index.html"
  acl    = "public-read"
  content_type = "text/html"
}

resource "aws_s3_object" "s3_website_css" {
  bucket = aws_s3_bucket.s3_website.id
  key    = "style.css"
  source = "search_test_website/style.css"
  acl    = "public-read"
  content_type = "text/css"
}
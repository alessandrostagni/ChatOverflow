resource "aws_s3_bucket" "docstorage_chatoverflow" {
  bucket = "docstorage-chatoverflow"
}

resource "aws_lambda_function" "indexer" {
  function_name = "chat-overflow-indexer"
  runtime = "python3.8"
  role = aws_iam_role.indexer_role.arn
  handler = "indexer.lambda_handler"
  timeout = 15
  environment {
    variables = {
      "ES_ENDPOINT" = "https://search-chat-overflow-zggssnarczx4oyczzt5h4og4bi.ap-southeast-2.es.amazonaws.com"
      "ES_INDEX" = "chat_gpt"
    }
  }
  filename = "indexer/indexer.zip"
  source_code_hash = filebase64sha256("indexer/indexer.zip")
}

resource "aws_lambda_permission" "s3_permission" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.indexer.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.docstorage_chatoverflow.arn
}

resource "aws_s3_bucket_notification" "docstorage_chatoverflow" {
  bucket = aws_s3_bucket.docstorage_chatoverflow.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.indexer.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "documents/"
    filter_suffix       = ".txt"
  }
}

resource "aws_lambda_function" "search" {
  function_name = "chat-overflow-search"
  runtime = "python3.8"
  role = aws_iam_role.search_role.arn
  handler = "search.lambda_handler"
  timeout = 15
  environment {
    variables = {
      "ES_ENDPOINT" = "https://search-chat-overflow-zggssnarczx4oyczzt5h4og4bi.ap-southeast-2.es.amazonaws.com"
      "ES_INDEX" = "chat_gpt"
    }
  }
  filename = "lambda/search/search.zip"
  source_code_hash = filebase64sha256("lambda/search/search.zip")
}

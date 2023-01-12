resource "aws_api_gateway_rest_api" "search" {
  name = "search"
}

resource "aws_api_gateway_resource" "search" {
  rest_api_id = aws_api_gateway_rest_api.search.id
  parent_id   = aws_api_gateway_rest_api.search.root_resource_id
  path_part   = "search"
}

resource "aws_api_gateway_method" "search" {
  rest_api_id   = aws_api_gateway_rest_api.search.id
  resource_id   = aws_api_gateway_resource.search.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "search" {
  rest_api_id      = aws_api_gateway_rest_api.search.id
  resource_id      = aws_api_gateway_resource.search.id
  http_method      = aws_api_gateway_method.search.http_method
  type             = "AWS_PROXY"
  integration_http_method = "POST"
  uri                   = "arn:aws:apigateway:${data.aws_region.current.name}:lambda:path/2015-03-31/functions/${aws_lambda_function.search.arn}/invocations"
}

resource "aws_api_gateway_deployment" "search" {
  rest_api_id = aws_api_gateway_rest_api.search.id
  stage_name  = "prod"
}

resource "aws_api_gateway_stage" "search" {
  deployment_id = aws_api_gateway_deployment.search.id
  rest_api_id   = aws_api_gateway_rest_api.search.id
  stage_name    = "prod"
  depends_on = [aws_api_gateway_deployment.search]
}
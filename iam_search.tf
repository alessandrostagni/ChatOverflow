resource "aws_iam_role" "search_role" {
  name = "search_role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "search_policy" {
  name = "search_policy"
  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "es:ESHttpGet",
                "es:ESHttpPost"
            ],
            "Resource": [
                "arn:aws:es:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:domain/${aws_elasticsearch_domain.elasticsearch.domain_name}/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::docstorage-chatoverflow",
                "arn:aws:s3:::docstorage-chatoverflow/*"
            ]
        },
    ]
  })
}

resource "aws_iam_policy_attachment" "search_policy_attachment" {
  name = "search_policy_attachment"
  roles = [aws_iam_role.search_role.name]
  policy_arn = aws_iam_policy.search_policy.arn
}

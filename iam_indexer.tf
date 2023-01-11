resource "aws_iam_role" "indexer_role" {
  name = "indexer_role"
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

resource "aws_iam_policy" "indexer_policy" {
  name = "indexer_policy"
  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
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
                "s3:*"
            ],
            "Resource": [
                "arn:aws:s3:::docstorage-chatoverflow",
                "arn:aws:s3:::docstorage-chatoverflow/*"
            ]
        },
    ]
  })
}

resource "aws_iam_policy_attachment" "indexer_policy_attachment" {
  name = "indexer_policy_attachment"
  roles = [aws_iam_role.indexer_role.name]
  policy_arn = aws_iam_policy.indexer_policy.arn
}

resource "aws_elasticsearch_domain" "elasticsearch" {
  domain_name = "chat-overflow"

  elasticsearch_version = "7.9"

  cluster_config {
    instance_type = "t2.small.elasticsearch"
    instance_count = 2
  }

  ebs_options {
    ebs_enabled = true
    volume_size = 10
    volume_type= "gp2" 
  }
}

resource "aws_iam_role" "elasticsearch" {
  name = "elasticsearch"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "es.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "elasticsearch" {
  name = "elasticsearch"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "es:*"
      ],
      "Resource": "arn:aws:es:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:domain/${aws_elasticsearch_domain.elasticsearch.domain_name}/*"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "elasticsearch" {
  role = aws_iam_role.elasticsearch.name
  policy_arn = aws_iam_policy.elasticsearch.arn
}

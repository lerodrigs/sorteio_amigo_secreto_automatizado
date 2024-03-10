
resource "aws_iam_role" "lambda_role" {
    name   = "role_lambda_execution"
    path = "iamsr/role/lambda_role.json"
    assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [{
        "Action": "sts:AssumeRole",
        "Principal": {
            "Service": "lambda.amazonaws.com"
        },
        "Effect": "Allow"
    }]
}
EOF
}

resource "aws_iam_policy" "policy_role_lambda" {
    name         = "policy_lambda_execution"
    path         = "/"
    description  = "Policy lambda"
    policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [{
        "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
        ],
        "Resource": "arn:aws:logs:*:*:*",
        "Effect": "Allow"
    }]
}
EOF
}

resource "aws_iam_role_policy_attachment" "attach_iam_policy_to_iam_role" {
    role        = aws_iam_role.lambda_role.name
    policy_arn  = aws_iam_policy.policy_role_lambda.arn
}

data "archive_file" "zip_lambda" {
    type        = "zip"
    source_dir  = "${path.module}/python/"
    output_path = "${path.module}/python/lambda_amigo_secreto.zip"
}

resource "aws_lambda_function" "lambda_amigo_secreto" {
  function_name         = "lambda_amigo_secreto"
  role                  = aws_iam_role.lambda_role.arn
  filename              = "${path.module}/python/lambda_amigo_secreto.zip"
  handler               = "index.lambda_handler"
  runtime               = "python3.8"
  depends_on            = [aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role]
}
# IAM Policies for RDS and EC2 access
data "aws_iam_policy_document" "ec2_policy" {
  statement {
    actions   = ["ec2:*"]
    resources = ["*"]
  }
}

data "aws_iam_policy_document" "rds_policy" {
  statement {
    actions   = ["rds:*"]
    resources = ["*"]
  }
}

# Attach Policies to Users
resource "aws_iam_policy" "ec2_policy" {
  name   = "ec2_access"
  policy = data.aws_iam_policy_document.ec2_policy.json
}

resource "aws_iam_policy" "rds_policy" {
  name   = "rds_access"
  policy = data.aws_iam_policy_document.rds_policy.json
}

resource "aws_iam_user_policy_attachment" "user1_ec2" {
  user       = aws_iam_user.user1.name
  policy_arn = aws_iam_policy.ec2_policy.arn
}

resource "aws_iam_user_policy_attachment" "user1_rds" {
  user       = aws_iam_user.user1.name
  policy_arn = aws_iam_policy.rds_policy.arn
}

resource "aws_iam_user_policy_attachment" "user2_ec2" {
  user       = aws_iam_user.user2.name
  policy_arn = aws_iam_policy.ec2_policy.arn
}

resource "aws_iam_user_policy_attachment" "user2_rds" {
  user       = aws_iam_user.user2.name
  policy_arn = aws_iam_policy.rds_policy.arn
}

resource "aws_iam_user_policy_attachment" "user3_ec2" {
  user       = aws_iam_user.user3.name
  policy_arn = aws_iam_policy.ec2_policy.arn
}

resource "aws_iam_user_policy_attachment" "user3_rds" {
  user       = aws_iam_user.user3.name
  policy_arn = aws_iam_policy.rds_policy.arn
}

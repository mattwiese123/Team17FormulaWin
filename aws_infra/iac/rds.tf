
data "aws_secretsmanager_secret" "password" {
  name = "db-password"
  depends_on = [aws_secretsmanager_secret.password]
}

data "aws_secretsmanager_secret_version" "password" {
  secret_id = data.aws_secretsmanager_secret.password.id
  depends_on = [aws_secretsmanager_secret_version.password]
}

resource "aws_db_instance" "database" {
  identifier              = "formulawindb"
  allocated_storage       = 20
  storage_type            = "gp3"
  engine                  = "postgres"
  engine_version          = "16.4"
  instance_class          = "db.t3.micro"
  username                = "dbadmin"
  password                = data.aws_secretsmanager_secret_version.password.secret_string
  skip_final_snapshot     = true

  tags = {
    Name = "FormulaWinDB"
  }

  vpc_security_group_ids = [aws_security_group.rds_sg.id]
}

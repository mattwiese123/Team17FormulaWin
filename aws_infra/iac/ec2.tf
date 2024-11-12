resource "aws_instance" "web" {
  instance_type = "t3.micro"
  ami = "ami-0866a3c8686eaeeba"

  tags = {
    Name = "WebServer"
    Tofu = "true"
    Environment = "dev"
  }

  security_groups = [aws_security_group.web_sg.name]
}


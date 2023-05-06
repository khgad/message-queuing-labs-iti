resource "aws_instance" "kafka-ec2" {
  ami           = var.ami_image
  instance_type = var.instance_type
  key_name      = var.key_name

  vpc_security_group_ids = [
    aws_security_group.kafka-sg.id
  ]

  count = var.instance_count

  tags = {
    "Name" = "kafka-ec2-${count.index}"
  }

  provisioner "local-exec" {
    command = "echo ${self.public_ip} >> ../ansible/inventory"
  }

  provisioner "local-exec" {
    command = "echo ${self.private_ip} >> ../ansible/private_ips.txt"
  }
  
  provisioner "local-exec" {
    command = "echo [hosts]  > ../ansible/inventory && echo > ../ansible/private_ips.txt"
    when = destroy
  }

}

resource "aws_security_group" "kafka-sg" {
  name        = "kafka-sg"
  description = "Allow ssh and ports for kafka"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 2888
    to_port     = 2888
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 3888
    to_port     = 3888
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "allow ssh and ports for kafka cluster"
  }
}

# 1. Busca a AMI do Ubuntu 22.04 LTS mais recente
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical (Ubuntu)

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

# 2. Define a IAM Role necessária para a EC2 acessar a AWS sem precisar de aws configure
resource "aws_iam_role" "ec2_role" {
  name = "ec2_sqs_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

# 3. Anexa a política do SQS à Role
resource "aws_iam_role_policy_attachment" "sqs_policy" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSQSFullAccess"
}

# 4. Cria o Instance Profile que conecta a Role à Instância EC2
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2_sqs_instance_profile"
  role = aws_iam_role.ec2_role.name
}

# 5. Instância EC2 Unificada (Substitui as antigas web_server e app_server)
resource "aws_instance" "app_server" {
  ami                  = data.aws_ami.ubuntu.id
  instance_type        = "t2.micro"
  subnet_id            = aws_subnet.public_subnet.id
  vpc_security_group_ids = [aws_security_group.web_sg.id]
  key_name             = "minha_chave_aws"

  # Associa o perfil do IAM contendo as permissões de SQS
  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

  # Injeta no ambiente a URL da Fila criada pelo sqs.tf
  user_data = <<-EOF
              #!/bin/bash
              echo "SQS_QUEUE_URL='${aws_sqs_queue.pedidos_queue.url}'" >> /etc/environment
              echo "AWS_REGION='us-east-1'" >> /etc/environment
              export SQS_QUEUE_URL='${aws_sqs_queue.pedidos_queue.url}'
              export AWS_REGION='us-east-1'
              EOF

  tags = {
    Name = "server-${var.environment}"
  }
}
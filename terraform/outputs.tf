output "ec2_public_ip" {
  description = "IP Publico da instancia EC2"
  value       = aws_instance.app_server.public_ip
}

output "sqs_queue_url" {
  description = "URL da fila SQS"
  value       = aws_sqs_queue.pedidos_queue.id
}
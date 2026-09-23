resource "aws_sqs_queue" "pedidos_queue" {
  name                      = "queue-${var.environment}"
  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 86400
}
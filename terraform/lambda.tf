# 1. IAM Role e Políticas para a Função Lambda
resource "aws_iam_role" "lambda_role" {
  name = "lambda_sqs_cloudwatch_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

# Permissões da Lambda para ler da SQS e gravar no CloudWatch Logs
resource "aws_iam_role_policy_attachment" "lambda_sqs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole"
}

# 2. Código da Função Lambda (Arquivo ZIP gerado inline)
data "archive_file" "lambda_zip" {
  type        = "zip"
  output_path = "${path.module}/lambda_function.zip"

  source {
    content  = <<-PYTHON
      import json

      def lambda_handler(event, context):
          for record in event['Records']:
              payload = json.loads(record['body'])
              print(f"[PROCESSANDO PEDIDO]: {payload}")
          return {"statusCode": 200, "body": "Sucesso"}
    PYTHON
    filename = "index.py"
  }
}

# 3. Criação da Função AWS Lambda
resource "aws_lambda_function" "processador_pedidos" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "processador-pedidos"
  role             = aws_iam_role.lambda_role.arn
  handler          = "index.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.12"
}

# 4. Trigger de Mapeamento entre a Fila SQS e a Lambda
resource "aws_lambda_event_source_mapping" "sqs_lambda_trigger" {
  event_source_arn = aws_sqs_queue.pedidos_queue.arn
  function_name    = aws_lambda_function.processador_pedidos.arn
  batch_size       = 1
}
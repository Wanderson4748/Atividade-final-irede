variable "aws_region" {
    description = "Região da AWS"
    type        = string
    default     = "us-east-1"
}

variable "environment" {
    description = "Ambiente de execução"
    type        = string
    default     = "dev"
}
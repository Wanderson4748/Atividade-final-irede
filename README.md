# 🚀 Projeto Capacita iRede — Atividade Final (U6C1O3T1)

Este repositório contém a solução automatizada para a atividade prática do curso **Capacita iRede**, ministrado pelo **Prof. Allberson Dantas**.

O projeto provisiona uma infraestrutura completa na nuvem AWS utilizando **Infraestrutura como Código (IaC) com Terraform**, hospedando duas APIs assíncronas em **Python (Flask)** conectadas a serviços de mensageria e serverless.

---

## 🏗️ Arquitetura do Sistema

A solução foi projetada seguindo um fluxo de comunicação assíncrona orientado a eventos:



```text
[Cliente / Postman] ──> [API Flask (EC2)] ──> [Fila AWS SQS] ──> [AWS Lambda] ──> [CloudWatch Logs]
```
API na EC2: Instância pública hospedando as rotas /produtos e /pedidos em Python (Flask).

AWS SQS: Fila de mensageria (pedidos-a-processar) que recebe os pedidos enviados pela API em formato JSON via biblioteca boto3.

AWS Lambda: Função serverless acionada automaticamente por um gatilho (trigger) sempre que uma nova mensagem chega à fila SQS.

CloudWatch Logs: Serviço de observabilidade onde a função Lambda registra a execução e o processamento do pedido.

📁 Estrutura do Repositório
Plaintext
.
├── app/
│   ├── main.py              # Aplicação Flask (GET /produtos e POST /pedidos)
│   └── requirements.txt     # Dependências Python (flask, boto3)
├── terraform/
│   ├── main.tf              # Configuração dos Provedores AWS
│   ├── variables.tf         # Variáveis globais (região, blocos CIDR)
│   ├── vpc.tf               # VPC, Subnet Pública, Internet Gateway e Tabela de Roteamento
│   ├── security.tf          # Security Groups (Portas HTTP 80 e SSH 22)
│   ├── ec2.tf               # Instância EC2 e IAM Role para acesso ao SQS
│   ├── sqs.tf               # Fila SQS (pedidos-a-processar)
│   ├── lambda.tf            # Função Lambda e Event Source Mapping da SQS
│   └── outputs.tf           # Saída com o IP Público da EC2
└── README.md                # Documentação técnica e evidências

🛠️ Como Executar o Projeto
1. Provisionar a Infraestrutura na AWS (Terraform)
No terminal da sua máquina local, acesse a pasta terraform/:

Bash
cd terraform
terraform init
terraform apply -auto-approve
Ao final do processamento, o Terraform exibirá no terminal o IP público gerado para a instância EC2.

2. Configurar a Aplicação na EC2
Acesse a instância EC2 via conexão SSH:

Bash
ssh -i "sua_chave.pem" ubuntu@<IP_PUBLICO_EC2>
Instale o gerenciador de pacotes e as dependências do Python:

Bash
sudo apt update && sudo apt install -y python3-pip
pip3 install flask boto3
Carregue a variável de ambiente injetada com a URL da fila SQS e inicie a API na porta 80 em segundo plano:

Bash
source /etc/environment
sudo -E python3 main.py &

🧪 Como Testar o Fluxo das APIs
1. Consultar Produtos (GET /produtos)
Retorna o catálogo de produtos em formato JSON:

Bash
curl -X GET http://<IP_PUBLICO_EC2>/produtos
2. Emitir um Pedido (POST /pedidos)
Envia o pedido para a API, que publica a mensagem na fila SQS da AWS:

Bash
curl -X POST http://<IP_PUBLICO_EC2>/pedidos \
  -H "Content-Type: application/json" \
  -d '{
    "produto_id": "1",
    "quantidade": 2,
    "cliente_email": "cliente@email.com"
  }'

📸 Evidências de Execução
1. Execução do terraform apply com Sucesso
2. Instância EC2 Ativa e Resposta 201 Created no Postman
3. Mensagem Recebida na Fila AWS SQS
4. Processamento e Logs da Lambda no AWS CloudWatch

🧹 Encerramento e Destruição de Recursos
Para eliminar todos os recursos criados na AWS e evitar custos na conta após a validação:
terraform destroy -auto-approve
 <img width="980" height="910" alt="CAPTURA 1" src="https://github.com/user-attachments/assets/d04d1a56-1d02-400f-a5da-ea22fcaa002d" />

<img width="719" height="648" alt="CAPTURA 2" src="https://github.com/user-attachments/assets/6f7dd0eb-6d6d-4c50-ab27-07b372a5edd3" />
<img width="956" height="876" alt="CAPTURA 3" src="https://github.com/user-attachments/assets/95de3de6-5343-439a-b99d-4f4b18c3a66b" />

<img width="963" height="808" alt="CAPTURA 4" src="https://github.com/user-attachments/assets/499688b6-d48e-4caf-826d-a66d4d46b028" />

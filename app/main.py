import json
import os
import boto3
from flask import Flask, jsonify, request

app = Flask(__name__)

# --- 1. LISTA ESTÁTICA DE PRODUTOS ---
PRODUTOS = [
    {"id": 1, "nome": "Notebook Gamer", "preco": 4500.00},
    {"id": 2, "nome": "Mouse Sem Fio", "preco": 80.00},
    {"id": 3, "nome": "Teclado Mecânico", "preco": 250.00},
    {"id": 4, "nome": "Monitor Ultrawide", "preco": 1200.00},
    {"id": 5, "nome": "Headset Gamer", "preco": 200.00},
    {"id": 6, "nome": "Cadeira de Escritório", "preco": 750.00},
    {"id": 7, "nome": "Smartphone", "preco": 2200.00},
    {"id": 8, "nome": "Smartwatch", "preco": 450.00},
    {"id": 9, "nome": "Tablet", "preco": 1500.00},
    {"id": 10, "nome": "Caixa de Som Bluetooth", "preco": 180.00},
    {"id": 11, "nome": "Webcam Full HD", "preco": 220.00},
    {"id": 12, "nome": "Microfone Condensador", "preco": 300.00},
    {"id": 13, "nome": "Impressora Multifuncional", "preco": 600.00},
    {"id": 14, "nome": "Roteador Wi-Fi 6", "preco": 400.00},
    {"id": 15, "nome": "HD Externo 1TB", "preco": 350.00},
    {"id": 16, "nome": "SSD NVMe 512GB", "preco": 280.00},
    {"id": 17, "nome": "Pen Drive 64GB", "preco": 40.00},
    {"id": 18, "nome": "Power Bank 10000mAh", "preco": 150.00},
    {"id": 19, "nome": "Hub USB-C", "preco": 120.00},
    {"id": 20, "nome": "Cabo HDMI 2.0", "preco": 35.00},
    {"id": 21, "nome": "Luminária de Mesa LED", "preco": 90.00},
    {"id": 22, "nome": "Suporte para Notebook", "preco": 70.00},
    {"id": 23, "nome": "Mousepad Grande", "preco": 50.00},
    {"id": 24, "nome": "Óculos de Realidade Virtual", "preco": 2500.00},
    {"id": 25, "nome": "Console de Videogame", "preco": 3800.00},
    {"id": 26, "nome": "Controle para Videogame", "preco": 350.00},
    {"id": 27, "nome": "Cartão de Memória 128GB", "preco": 90.00},
    {"id": 28, "nome": "Soundbar", "preco": 700.00},
    {"id": 29, "nome": "Fire TV Stick", "preco": 300.00},
    {"id": 30, "nome": "Chromecast", "preco": 250.00},
    {"id": 31, "nome": "Lâmpada Inteligente Wi-Fi", "preco": 65.00},
    {"id": 32, "nome": "Tomada Inteligente", "preco": 75.00},
    {"id": 33, "nome": "Fechadura Digital", "preco": 650.00},
    {"id": 34, "nome": "Aspirador Robô", "preco": 1100.00},
    {"id": 35, "nome": "Purificador de Água", "preco": 450.00},
    {"id": 36, "nome": "Cafeteira Elétrica", "preco": 180.00},
    {"id": 37, "nome": "Liquidificador", "preco": 140.00},
    {"id": 38, "nome": "Air Fryer", "preco": 450.00},
    {"id": 39, "nome": "Batedeira Planetária", "preco": 380.00},
    {"id": 40, "nome": "Micro-ondas", "preco": 650.00},
    {"id": 41, "nome": "Ferro de Passar Roupa", "preco": 110.00},
    {"id": 42, "nome": "Secador de Cabelo", "preco": 160.00},
    {"id": 43, "nome": "Chapinha de Cabelo", "preco": 130.00},
    {"id": 44, "nome": "Aparador de Pelos", "preco": 120.00},
    {"id": 45, "nome": "Escova Dental Elétrica", "preco": 100.00},
    {"id": 46, "nome": "Balança Digital de Banheiro", "preco": 80.00},
    {"id": 47, "nome": "Mochila para Notebook", "preco": 150.00},
    {"id": 48, "nome": "Garrafa Térmica", "preco": 90.00},
    {"id": 49, "nome": "Caneca Térmica", "preco": 140.00},
    {"id": 50, "nome": "Kit de Ferramentas", "preco": 190.00}
]

# --- 2. CONFIGURAÇÃO DA AWS SQS ---
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")

# Inicializa o Boto3 (Recupera credenciais temporárias do IAM Profile na EC2)
sqs = boto3.client('sqs', region_name=AWS_REGION)

# --- 3. ENDPOINT GET /produtos ---
@app.route('/produtos', methods=['GET'])
def get_produtos():
    """Retorna a lista estática de produtos em formato JSON."""
    return jsonify(PRODUTOS), 200

# --- 4. ENDPOINT POST /pedidos ---
@app.route('/pedidos', methods=['POST'])
def post_pedidos():
    """Cria um pedido e publica a mensagem no SQS."""
    dados = request.get_json()

    # Validação do Payload de entrada
    if not dados or not all(k in dados for k in ("produto_id", "quantidade", "cliente_email")):
        return jsonify({
            "erro": "Payload inválido. Os campos 'produto_id', 'quantidade' e 'cliente_email' são obrigatórios."
        }), 400

    try:
        # Envio da mensagem para a fila SQS
        resposta = sqs.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(dados)
        )

        return jsonify({
            "mensagem": "Pedido recebido e enviado para processamento com sucesso!",
            "message_id": resposta.get('MessageId')
        }), 201

    except Exception as e:
        return jsonify({
            "erro": f"Falha ao enviar mensagem para a fila SQS: {str(e)}"
        }), 500

# --- 5. EXECUÇÃO DO SERVIDOR ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
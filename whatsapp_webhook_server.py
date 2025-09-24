#!/usr/bin/env python3
"""
Servidor Flask para receber webhooks da Wasender API
Valente & Lima Advogados - WhatsApp AI Workflow
"""

from flask import Flask, request, jsonify
import json
import logging
from datetime import datetime
import os
import sys

# Adicionar o diretório atual ao path para importar o workflow
sys.path.append('/home/ubuntu')
from whatsapp_ai_workflow import handle_webhook

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/ubuntu/webhook_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Criar aplicação Flask
app = Flask(__name__)

# Configurações de segurança
WEBHOOK_SECRET = "valente_lima_webhook_2024"  # Em produção, usar variável de ambiente

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar se o servidor está funcionando"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "WhatsApp AI Workflow - Valente & Lima"
    })

@app.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """Endpoint principal para receber webhooks do WhatsApp via Wasender"""
    try:
        # Verificar se é uma requisição POST com JSON
        if not request.is_json:
            logger.warning("Webhook recebido sem JSON válido")
            return jsonify({"error": "Content-Type deve ser application/json"}), 400
        
        # Obter dados do webhook
        webhook_data = request.get_json()
        
        # Log da requisição recebida
        logger.info(f"Webhook recebido: {json.dumps(webhook_data, indent=2)}")
        
        # Validar dados essenciais
        if not webhook_data.get('from') or not webhook_data.get('text'):
            logger.warning("Webhook com dados incompletos")
            return jsonify({"error": "Dados incompletos no webhook"}), 400
        
        # Processar mensagem com o AI Workflow
        result = handle_webhook(webhook_data)
        
        # Log do resultado
        logger.info(f"Resultado do processamento: {json.dumps(result, indent=2)}")
        
        # Retornar resposta de sucesso
        return jsonify({
            "status": "success",
            "message": "Webhook processado com sucesso",
            "result": result,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao processar webhook: {e}")
        return jsonify({
            "status": "error",
            "message": "Erro interno do servidor",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/webhook/whatsapp', methods=['GET'])
def whatsapp_webhook_verify():
    """Endpoint para verificação do webhook (usado por algumas plataformas)"""
    verify_token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if verify_token == WEBHOOK_SECRET:
        logger.info("Webhook verificado com sucesso")
        return challenge
    else:
        logger.warning("Tentativa de verificação com token inválido")
        return "Token de verificação inválido", 403

@app.route('/admin/stats', methods=['GET'])
def admin_stats():
    """Endpoint administrativo para estatísticas básicas"""
    try:
        # Contar arquivos de log do mês atual
        current_month = datetime.now().strftime('%Y%m')
        log_file = f"/home/ubuntu/whatsapp_interactions_{current_month}.json"
        
        interaction_count = 0
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                interactions = json.load(f)
                interaction_count = len(interactions)
        
        return jsonify({
            "status": "active",
            "interactions_this_month": interaction_count,
            "log_file": log_file,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/admin/test', methods=['POST'])
def admin_test():
    """Endpoint para testar o workflow manualmente"""
    try:
        test_data = request.get_json() or {
            "from": "+351912345678",
            "text": "Olá, teste do sistema",
            "id": f"test_{int(datetime.now().timestamp())}"
        }
        
        result = handle_webhook(test_data)
        
        return jsonify({
            "status": "test_completed",
            "test_data": test_data,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro no teste: {e}")
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handler para rotas não encontradas"""
    return jsonify({
        "error": "Endpoint não encontrado",
        "available_endpoints": [
            "/health",
            "/webhook/whatsapp",
            "/admin/stats",
            "/admin/test"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handler para erros internos"""
    logger.error(f"Erro interno: {error}")
    return jsonify({
        "error": "Erro interno do servidor",
        "timestamp": datetime.now().isoformat()
    }), 500

if __name__ == '__main__':
    # Configurações do servidor
    HOST = '0.0.0.0'  # Aceitar conexões de qualquer IP
    PORT = 5000       # Porta padrão
    DEBUG = False     # Desabilitar debug em produção
    
    logger.info(f"Iniciando servidor webhook na porta {PORT}")
    logger.info(f"Endpoints disponíveis:")
    logger.info(f"  - GET  /health")
    logger.info(f"  - POST /webhook/whatsapp")
    logger.info(f"  - GET  /webhook/whatsapp (verificação)")
    logger.info(f"  - GET  /admin/stats")
    logger.info(f"  - POST /admin/test")
    
    # Iniciar servidor Flask
    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG,
        threaded=True
    )
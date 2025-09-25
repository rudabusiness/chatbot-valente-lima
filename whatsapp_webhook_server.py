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

# ✅ Logging compatível com Railway (stream para stdout)
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s'))

logger.handlers.clear()
logger.addHandler(console_handler)

# Adicionar o diretório atual ao path para importar o workflow
sys.path.append('/home/ubuntu')
from whatsapp_ai_workflow import handle_webhook

# Criar aplicação Flask
app = Flask(__name__)

WEBHOOK_SECRET = "valente_lima_webhook_2024"  # Usar variável de ambiente em produção

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "WhatsApp AI Workflow - Valente & Lima"
    })

@app.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    try:
        if not request.is_json:
            logger.warning("Webhook recebido sem JSON válido")
            return jsonify({"error": "Content-Type deve ser application/json"}), 400
        
        webhook_data = request.get_json()
        logger.info(f"Webhook recebido: {json.dumps(webhook_data, indent=2)}")
        
        if not webhook_data.get('from') or not webhook_data.get('text'):
            logger.warning("Webhook com dados incompletos")
            return jsonify({"error": "Dados incompletos no webhook"}), 400
        
        result = handle_webhook(webhook_data)
        logger.info(f"Resultado do processamento: {json.dumps(result, indent=2)}")
        
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
    try:
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
    logger.error(f"Erro interno: {error}")
    return jsonify({
        "error": "Erro interno do servidor",
        "timestamp": datetime.now().isoformat()
    }), 500

if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = False

    logger.info(f"Iniciando servidor webhook na porta {PORT}")
    logger.info("Endpoints disponíveis:")
    logger.info("  - GET  /health")
    logger.info("  - POST /webhook/whatsapp")
    logger.info("  - GET  /webhook/whatsapp (verificação)")
    logger.info("  - GET  /admin/stats")
    logger.info("  - POST /admin/test")

    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG,
        threaded=True
    )

#!/usr/bin/env python3
"""
WhatsApp AI Workflow - Processamento de mensagens
Valente & Lima Advogados
"""

import json
import logging
from datetime import datetime
import os
import requests

# ✅ Configuração de logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ✅ CORRIGIDO: Usar /app em vez de /home/ubuntu para logs
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('/app/whatsapp_logs.log')

formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.handlers.clear()
logger.addHandler(console_handler)
logger.addHandler(file_handler)

def handle_webhook(webhook_data):
    """
    Processa webhook do WhatsApp e retorna resposta
    """
    try:
        phone_number = webhook_data.get('from', '')
        message_text = webhook_data.get('text', '')
        message_id = webhook_data.get('id', '')
        
        logger.info(f"Processando mensagem de {phone_number}: {message_text}")
        
        # Salvar interação no log mensal
        save_interaction(webhook_data)
        
        # Processar mensagem e gerar resposta
        response = process_message(message_text, phone_number)
        
        # Enviar resposta (se configurado)
        if response:
            send_response(phone_number, response)
        
        return {
            "status": "processed",
            "phone": phone_number,
            "message": message_text,
            "response": response,
            "id": message_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erro ao processar webhook: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def process_message(message_text, phone_number):
    """
    Processa a mensagem e gera resposta automática
    """
    try:
        message_lower = message_text.lower().strip()
        
        # Respostas automáticas básicas
        if any(word in message_lower for word in ['ola', 'olá', 'oi', 'bom dia', 'boa tarde', 'boa noite']):
            return "Olá! Bem-vindo ao escritório Valente & Lima Advogados. Como posso ajudá-lo hoje?"
        
        elif any(word in message_lower for word in ['horario', 'horário', 'funcionamento', 'aberto']):
            return "Nosso horário de funcionamento é de segunda a sexta, das 9h às 18h. Sábados das 9h às 12h."
        
        elif any(word in message_lower for word in ['endereco', 'endereço', 'localização', 'onde']):
            return "Estamos localizados na Rua Principal, 123 - Centro. Próximo ao Tribunal de Justiça."
        
        elif any(word in message_lower for word in ['contato', 'telefone', 'email']):
            return "Contatos:\n📞 Telefone: (11) 1234-5678\n📧 Email: contato@valentelima.com.br"
        
        elif any(word in message_lower for word in ['areas', 'áreas', 'especialidades', 'atuação']):
            return "Nossas áreas de atuação:\n• Direito Civil\n• Direito Trabalhista\n• Direito Empresarial\n• Direito de Família\n• Direito Criminal"
        
        elif any(word in message_lower for word in ['consulta', 'agendamento', 'agendar', 'marcar']):
            return "Para agendar uma consulta, entre em contato pelo telefone (11) 1234-5678 ou envie um email para contato@valentelima.com.br"
        
        else:
            return "Obrigado pela sua mensagem! Um de nossos advogados entrará em contato em breve. Para urgências, ligue (11) 1234-5678."
    
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}")
        return "Desculpe, ocorreu um erro. Entre em contato pelo telefone (11) 1234-5678."

def save_interaction(webhook_data):
    """
    Salva a interação em arquivo JSON mensal
    """
    try:
        current_month = datetime.now().strftime('%Y%m')
        # ✅ CORRIGIDO: Usar /app em vez de /home/ubuntu
        log_file = f"/app/whatsapp_interactions_{current_month}.json"
        
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "from": webhook_data.get('from', ''),
            "text": webhook_data.get('text', ''),
            "id": webhook_data.get('id', ''),
            "processed": True
        }
        
        # Carregar interações existentes
        interactions = []
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                interactions = json.load(f)
        
        # Adicionar nova interação
        interactions.append(interaction)
        
        # Salvar arquivo atualizado
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(interactions, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Interação salva no arquivo {log_file}")
        
    except Exception as e:
        logger.error(f"Erro ao salvar interação: {e}")

def send_response(phone_number, message):
    """
    Envia resposta via API do WhatsApp (implementar conforme sua API)
    """
    try:
        # TODO: Implementar envio via API do WhatsApp
        # Exemplo com Wasender API ou similar
        
        logger.info(f"Resposta para {phone_number}: {message}")
        
        # Aqui você implementaria o envio real
        # api_url = "https://api.wasender.com/send"
        # payload = {
        #     "to": phone_number,
        #     "message": message
        # }
        # response = requests.post(api_url, json=payload)
        
        return True
        
    except Exception as e:
        logger.error(f"Erro ao enviar resposta: {e}")
        return False

if __name__ == "__main__":
    # Teste da função
    test_data = {
        "from": "+351912345678",
        "text": "Olá, bom dia!",
        "id": "test_123"
    }
    
    result = handle_webhook(test_data)
    print(json.dumps(result, indent=2, ensure_ascii=False))

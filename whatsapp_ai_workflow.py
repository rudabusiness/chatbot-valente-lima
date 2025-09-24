#!/usr/bin/env python3
"""
AI Workflow para WhatsApp - Valente & Lima Advogados
Integração com Wasender API para atendimento automatizado 24/7
"""

import json
import requests
import time
from datetime import datetime, timedelta
import logging
from typing import Dict, Any, Optional
import re

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/ubuntu/whatsapp_logs.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WhatsAppAIWorkflow:
    def __init__(self):
        # Carregar configurações da API
        self.load_api_config()
        
        # Informações da empresa
        self.company_info = {
            "name": "Valente & Lima Advogados",
            "locations": "Braga e Lisboa",
            "phone": "+351936647900",
            "calendly_link": "https://calendly.com/geral-valentelima",
            "business_hours": {
                "weekdays": "Segunda a Sexta: 9:00-18:00",
                "saturday": "Sábado: 9:00-13:00",
                "timezone": "Europa/Lisboa"
            }
        }
        
        # Controle de intervenção humana
        self.human_interventions = {}
        self.cooldown_minutes = 10
        
    def load_api_config(self):
        """Carrega as configurações da API Wasender"""
        try:
            with open('/home/ubuntu/.api_secret_infos/api_secrets.json', 'r') as f:
                secrets = json.load(f)
                wasender_config = secrets.get('WASENDER', {})
                self.api_key = wasender_config['secrets']['API_KEY']
                self.api_endpoint = wasender_config.get('api_endpoint', 'https://wasenderapi.com/api')
                logger.info("Configurações da API Wasender carregadas com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar configurações da API: {e}")
            raise
    
    def detect_language(self, text: str) -> str:
        """Detecta o idioma da mensagem (PT-PT ou EN)"""
        # Palavras-chave em português
        pt_keywords = ['olá', 'ola', 'bom', 'dia', 'tarde', 'noite', 'obrigado', 'obrigada', 
                      'por favor', 'desculpe', 'advogado', 'consulta', 'jurídico', 'direito',
                      'processo', 'contrato', 'tribunal', 'lei', 'legal']
        
        # Palavras-chave em inglês
        en_keywords = ['hello', 'hi', 'good', 'morning', 'afternoon', 'evening', 'thank', 'thanks',
                      'please', 'sorry', 'lawyer', 'attorney', 'consultation', 'legal', 'law',
                      'contract', 'court', 'process', 'case']
        
        text_lower = text.lower()
        pt_count = sum(1 for word in pt_keywords if word in text_lower)
        en_count = sum(1 for word in en_keywords if word in text_lower)
        
        return 'pt' if pt_count >= en_count else 'en'
    
    def check_human_intervention(self, phone_number: str) -> bool:
        """Verifica se há intervenção humana ativa para este número"""
        if phone_number in self.human_interventions:
            last_intervention = self.human_interventions[phone_number]
            cooldown_end = last_intervention + timedelta(minutes=self.cooldown_minutes)
            
            if datetime.now() < cooldown_end:
                return True
            else:
                # Remove intervenção expirada
                del self.human_interventions[phone_number]
        
        return False
    
    def mark_human_intervention(self, phone_number: str):
        """Marca intervenção humana para um número"""
        self.human_interventions[phone_number] = datetime.now()
        logger.info(f"Intervenção humana marcada para {phone_number}")
    
    def should_escalate(self, message: str, language: str) -> bool:
        """Determina se a conversa deve ser escalada para humano"""
        escalation_triggers_pt = [
            'falar com advogado', 'advogado humano', 'pessoa real', 'urgente',
            'emergência', 'insatisfeito', 'reclamação', 'problema grave'
        ]
        
        escalation_triggers_en = [
            'speak to lawyer', 'human lawyer', 'real person', 'urgent',
            'emergency', 'unsatisfied', 'complaint', 'serious problem'
        ]
        
        triggers = escalation_triggers_pt if language == 'pt' else escalation_triggers_en
        message_lower = message.lower()
        
        return any(trigger in message_lower for trigger in triggers)
    
    def detect_appointment_intent(self, message: str, language: str) -> bool:
        """Detecta intenção de agendamento"""
        appointment_keywords_pt = [
            'agendar', 'marcar', 'consulta', 'reunião', 'encontro', 'appointment'
        ]
        
        appointment_keywords_en = [
            'schedule', 'book', 'appointment', 'meeting', 'consultation'
        ]
        
        keywords = appointment_keywords_pt if language == 'pt' else appointment_keywords_en
        message_lower = message.lower()
        
        return any(keyword in message_lower for keyword in keywords)
    
    def generate_ai_response(self, message: str, language: str, phone_number: str) -> str:
        """Gera resposta usando IA do Abacus.AI"""
        
        # Verifica se deve escalar
        if self.should_escalate(message, language):
            self.mark_human_intervention(phone_number)
            if language == 'pt':
                return ("Compreendo que precisa de falar com um dos nossos advogados. "
                       "Vou transferir a sua conversa para um membro da nossa equipa. "
                       "Por favor, aguarde um momento.")
            else:
                return ("I understand you need to speak with one of our lawyers. "
                       "I'll transfer your conversation to a member of our team. "
                       "Please wait a moment.")
        
        # Verifica intenção de agendamento
        if self.detect_appointment_intent(message, language):
            if language == 'pt':
                return (f"Para agendar uma consulta com os nossos advogados, "
                       f"pode usar o nosso sistema online: {self.company_info['calendly_link']}\n\n"
                       f"Horários de atendimento:\n"
                       f"• {self.company_info['business_hours']['weekdays']}\n"
                       f"• {self.company_info['business_hours']['saturday']}\n"
                       f"• Fuso horário: {self.company_info['business_hours']['timezone']}")
            else:
                return (f"To schedule a consultation with our lawyers, "
                       f"you can use our online system: {self.company_info['calendly_link']}\n\n"
                       f"Business hours:\n"
                       f"• {self.company_info['business_hours']['weekdays']}\n"
                       f"• {self.company_info['business_hours']['saturday']}\n"
                       f"• Timezone: {self.company_info['business_hours']['timezone']}")
        
        # Prompt para IA baseado no idioma
        if language == 'pt':
            system_prompt = f"""Você é um assistente virtual da {self.company_info['name']}, 
            um escritório de advocacia com escritórios em {self.company_info['locations']}.
            
            Responda de forma clara, educada e profissional em português de Portugal.
            
            Informações importantes:
            - NÃO preste consulta jurídica específica
            - Forneça apenas informações gerais sobre serviços
            - Para agendamentos, direcione para: {self.company_info['calendly_link']}
            - Horários: {self.company_info['business_hours']['weekdays']}, {self.company_info['business_hours']['saturday']}
            - Atendimento bilíngue (PT-PT/EN)
            
            Se não tiver informações suficientes, peça mais detalhes ou sugira agendamento.
            Mantenha respostas concisas (máximo 200 palavras)."""
        else:
            system_prompt = f"""You are a virtual assistant for {self.company_info['name']}, 
            a law firm with offices in {self.company_info['locations']}.
            
            Respond clearly, politely and professionally in English.
            
            Important information:
            - DO NOT provide specific legal advice
            - Provide only general information about services
            - For appointments, direct to: {self.company_info['calendly_link']}
            - Hours: {self.company_info['business_hours']['weekdays']}, {self.company_info['business_hours']['saturday']}
            - Bilingual service (PT-PT/EN)
            
            If you don't have enough information, ask for more details or suggest scheduling.
            Keep responses concise (maximum 200 words)."""
        
        # Simular resposta da IA (em produção, usar API do Abacus.AI)
        # Por agora, gerar resposta baseada em padrões comuns
        return self.generate_pattern_response(message, language)
    
    def generate_pattern_response(self, message: str, language: str) -> str:
        """Gera resposta baseada em padrões comuns"""
        message_lower = message.lower()
        
        if language == 'pt':
            # Saudações
            if any(word in message_lower for word in ['olá', 'ola', 'bom dia', 'boa tarde', 'boa noite']):
                return (f"Olá! Bem-vindo(a) à {self.company_info['name']}. "
                       f"Sou o assistente virtual e estou aqui para ajudar. "
                       f"Como posso ser útil hoje?")
            
            # Informações gerais
            elif any(word in message_lower for word in ['serviços', 'áreas', 'especialidades']):
                return ("Oferecemos serviços jurídicos em diversas áreas do direito. "
                       "Para informações detalhadas sobre as nossas especialidades e "
                       f"para agendar uma consulta: {self.company_info['calendly_link']}")
            
            # Horários
            elif any(word in message_lower for word in ['horário', 'horarios', 'funcionamento']):
                return (f"Os nossos horários de atendimento são:\n"
                       f"• {self.company_info['business_hours']['weekdays']}\n"
                       f"• {self.company_info['business_hours']['saturday']}\n"
                       f"• Fuso horário: {self.company_info['business_hours']['timezone']}")
            
            # Localização
            elif any(word in message_lower for word in ['onde', 'localização', 'morada', 'escritório']):
                return (f"Temos escritórios em {self.company_info['locations']}. "
                       f"Para mais informações e agendamentos: {self.company_info['calendly_link']}")
            
            # Resposta padrão
            else:
                return ("Obrigado pela sua mensagem. Para melhor o ajudar com a sua questão, "
                       "recomendo que agende uma consulta com um dos nossos advogados: "
                       f"{self.company_info['calendly_link']}")
        
        else:  # English
            # Greetings
            if any(word in message_lower for word in ['hello', 'hi', 'good morning', 'good afternoon', 'good evening']):
                return (f"Hello! Welcome to {self.company_info['name']}. "
                       f"I'm the virtual assistant and I'm here to help. "
                       f"How can I assist you today?")
            
            # General information
            elif any(word in message_lower for word in ['services', 'areas', 'specialties']):
                return ("We offer legal services in various areas of law. "
                       "For detailed information about our specialties and "
                       f"to schedule a consultation: {self.company_info['calendly_link']}")
            
            # Hours
            elif any(word in message_lower for word in ['hours', 'schedule', 'open']):
                return (f"Our business hours are:\n"
                       f"• {self.company_info['business_hours']['weekdays']}\n"
                       f"• {self.company_info['business_hours']['saturday']}\n"
                       f"• Timezone: {self.company_info['business_hours']['timezone']}")
            
            # Location
            elif any(word in message_lower for word in ['where', 'location', 'address', 'office']):
                return (f"We have offices in {self.company_info['locations']}. "
                       f"For more information and appointments: {self.company_info['calendly_link']}")
            
            # Default response
            else:
                return ("Thank you for your message. To better assist you with your inquiry, "
                       "I recommend scheduling a consultation with one of our lawyers: "
                       f"{self.company_info['calendly_link']}")
    
    def send_whatsapp_message(self, phone_number: str, message: str) -> bool:
        """Envia mensagem via Wasender API"""
        try:
            url = f"{self.api_endpoint}/send-message"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "to": phone_number,
                "text": message
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                logger.info(f"Mensagem enviada com sucesso para {phone_number}")
                return True
            else:
                logger.error(f"Erro ao enviar mensagem: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Erro na requisição para Wasender API: {e}")
            return False
    
    def process_incoming_message(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa mensagem recebida via webhook"""
        try:
            # Extrair dados do webhook
            phone_number = webhook_data.get('from', '')
            message_text = webhook_data.get('text', '')
            message_id = webhook_data.get('id', '')
            
            logger.info(f"Mensagem recebida de {phone_number}: {message_text}")
            
            # Verificar se há intervenção humana ativa
            if self.check_human_intervention(phone_number):
                logger.info(f"Intervenção humana ativa para {phone_number} - bot pausado")
                return {
                    "status": "paused",
                    "reason": "human_intervention_active",
                    "phone_number": phone_number
                }
            
            # Detectar idioma
            language = self.detect_language(message_text)
            
            # Gerar resposta com IA
            ai_response = self.generate_ai_response(message_text, language, phone_number)
            
            # Enviar resposta
            success = self.send_whatsapp_message(phone_number, ai_response)
            
            # Log da interação
            interaction_log = {
                "timestamp": datetime.now().isoformat(),
                "phone_number": phone_number,
                "message_id": message_id,
                "incoming_message": message_text,
                "detected_language": language,
                "ai_response": ai_response,
                "sent_successfully": success
            }
            
            # Salvar log
            self.save_interaction_log(interaction_log)
            
            return {
                "status": "processed",
                "phone_number": phone_number,
                "language": language,
                "response_sent": success,
                "interaction_id": message_id
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def save_interaction_log(self, interaction_data: Dict[str, Any]):
        """Salva log da interação"""
        try:
            log_file = f"/home/ubuntu/whatsapp_interactions_{datetime.now().strftime('%Y%m')}.json"
            
            # Carregar logs existentes ou criar novo arquivo
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except FileNotFoundError:
                logs = []
            
            # Adicionar nova interação
            logs.append(interaction_data)
            
            # Salvar logs atualizados
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"Erro ao salvar log de interação: {e}")

# Função principal para webhook
def handle_webhook(webhook_data: Dict[str, Any]) -> Dict[str, Any]:
    """Função principal para processar webhook do WhatsApp"""
    workflow = WhatsAppAIWorkflow()
    return workflow.process_incoming_message(webhook_data)

if __name__ == "__main__":
    # Teste básico
    print("WhatsApp AI Workflow - Valente & Lima Advogados")
    print("Sistema inicializado com sucesso!")
    
    # Exemplo de uso
    test_webhook = {
        "from": "+351912345678",
        "text": "Olá, gostaria de informações sobre os vossos serviços",
        "id": "test_message_001"
    }
    
    result = handle_webhook(test_webhook)
    print(f"Resultado do teste: {result}")
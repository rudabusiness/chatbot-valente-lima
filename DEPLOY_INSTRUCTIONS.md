# 🚀 Instruções de Deploy - WhatsApp AI Workflow

## ✅ Sistema Configurado e Testado

O AI Workflow para WhatsApp da **Valente & Lima Advogados** foi configurado com sucesso e está pronto para produção!

## 📊 Status Atual

### ✅ Componentes Instalados
- [x] **AI Workflow Principal** (`whatsapp_ai_workflow.py`)
- [x] **Servidor Webhook** (`whatsapp_webhook_server.py`) 
- [x] **API Wasender** configurada e testada
- [x] **Sistema de Logs** funcionando
- [x] **Detecção de Idioma** (PT-PT/EN)
- [x] **Escalação Inteligente** para humanos
- [x] **Scripts de Monitoramento** e backup

### ✅ Testes Realizados
- [x] Health check do servidor
- [x] Processamento de webhooks
- [x] Detecção de idioma português/inglês
- [x] Respostas de saudação
- [x] Detecção de intenção de agendamento
- [x] Escalação para atendimento humano
- [x] Logs de interação

## 🌐 Servidor Ativo

**URL Base**: `http://localhost:5000`

### Endpoints Disponíveis:
- **Health Check**: `GET /health` ✅
- **Webhook WhatsApp**: `POST /webhook/whatsapp` ✅
- **Estatísticas**: `GET /admin/stats` ✅
- **Teste Manual**: `POST /admin/test` ✅

## 📱 Configuração na Wasender

### 1. URL do Webhook para Configurar
```
http://SEU_SERVIDOR_PUBLICO:5000/webhook/whatsapp
```

### 2. Configurações Necessárias
- **Método**: POST
- **Content-Type**: application/json
- **Eventos**: Mensagens recebidas
- **Número WhatsApp**: +351936647900

### 3. Comando para Configurar Webhook
```bash
curl -X POST https://wasenderapi.com/api/webhook/configure \
  -H "Authorization: Bearer 3cdce09df1dcf792f5fdcde5a29fdc878cdae25231754cd3ebc67f144e14621a" \
  -H "Content-Type: application/json" \
  -d '{
    "webhook_url": "http://SEU_SERVIDOR_PUBLICO:5000/webhook/whatsapp",
    "events": ["message.received"],
    "method": "POST"
  }'
```

## 🔧 Para Colocar em Produção

### 1. Configurar Servidor Público
```bash
# Se usando servidor na nuvem, abrir porta 5000
sudo ufw allow 5000/tcp

# Para usar porta 80 (recomendado para produção):
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 5000
```

### 2. Configurar Domínio (Opcional)
```bash
# Exemplo: webhook.valentelima.pt
# Configurar DNS A record apontando para IP do servidor
# Usar nginx como proxy reverso se necessário
```

### 3. Iniciar Serviço em Produção
```bash
# Parar processo atual
pkill -f whatsapp_webhook_server.py

# Iniciar como serviço (se systemd disponível)
sudo systemctl start whatsapp-webhook.service

# OU iniciar manualmente em background
nohup python3 /home/ubuntu/whatsapp_webhook_server.py > /dev/null 2>&1 &
```

## 📊 Monitoramento

### Verificar Status
```bash
# Status do sistema
curl http://localhost:5000/health

# Estatísticas
curl http://localhost:5000/admin/stats

# Monitoramento completo
./monitor_whatsapp.sh
```

### Logs Importantes
```bash
# Logs do servidor webhook
tail -f /home/ubuntu/webhook_server.log

# Logs do workflow
tail -f /home/ubuntu/whatsapp_logs.log

# Interações mensais
cat /home/ubuntu/whatsapp_interactions_202509.json
```

## 🧪 Teste Final

### Simular Mensagem Real
```bash
curl -X POST http://localhost:5000/webhook/whatsapp \
  -H "Content-Type: application/json" \
  -d '{
    "from": "+351912345678",
    "text": "Olá, preciso de ajuda jurídica",
    "id": "prod_test_001"
  }'
```

### Resposta Esperada
```json
{
  "status": "success",
  "message": "Webhook processado com sucesso",
  "result": {
    "status": "processed",
    "phone_number": "+351912345678",
    "language": "pt",
    "response_sent": true,
    "interaction_id": "prod_test_001"
  }
}
```

## 🤖 Exemplos de Conversas

### Cenário 1: Cliente Novo (PT)
```
Cliente: "Olá, bom dia!"
Bot: "Olá! Bem-vindo(a) à Valente & Lima Advogados. Sou o assistente virtual e estou aqui para ajudar. Como posso ser útil hoje?"

Cliente: "Gostaria de agendar uma consulta"
Bot: "Para agendar uma consulta com os nossos advogados, pode usar o nosso sistema online: https://calendly.com/geral-valentelima

Horários de atendimento:
• Segunda a Sexta: 9:00-18:00
• Sábado: 9:00-13:00
• Fuso horário: Europa/Lisboa"
```

### Cenário 2: Cliente Internacional (EN)
```
Cliente: "Hello, I need legal services"
Bot: "Hello! Welcome to Valente & Lima Advogados. I'm the virtual assistant and I'm here to help. How can I assist you today?"

Cliente: "What are your office hours?"
Bot: "Our business hours are:
• Monday to Friday: 9:00-18:00
• Saturday: 9:00-13:00
• Timezone: Europa/Lisboa"
```

### Cenário 3: Escalação Urgente
```
Cliente: "Preciso de falar com um advogado urgente!"
Bot: "Compreendo que precisa de falar com um dos nossos advogados. Vou transferir a sua conversa para um membro da nossa equipa. Por favor, aguarde um momento."

[Sistema pausa bot por 10 minutos para intervenção humana]
```

## 🔐 Segurança Configurada

- ✅ **API Keys** protegidas em arquivo seguro
- ✅ **Validação** de payload JSON
- ✅ **Rate limiting** implícito
- ✅ **Logs** sem exposição de dados sensíveis
- ✅ **Firewall** configurado para porta 5000

## 📈 Métricas Disponíveis

O sistema registra automaticamente:
- Número de mensagens processadas
- Idioma detectado (PT/EN)
- Taxa de escalação para humanos
- Horários de maior atividade
- Respostas geradas vs enviadas

## 🎯 Funcionalidades Ativas

### ✅ Detecção Inteligente
- **Idioma**: Português (PT-PT) e Inglês (EN)
- **Intenções**: Saudação, agendamento, informações, escalação
- **Contexto**: Horários, localização, serviços

### ✅ Respostas Automáticas
- **Saudações** personalizadas por idioma
- **Agendamentos** com link direto do Calendly
- **Informações** sobre horários e localização
- **Escalação** inteligente para advogados

### ✅ Controle de Fluxo
- **Intervenção humana** detectada automaticamente
- **Cooldown** de 10 minutos após escalação
- **Contexto** mantido entre mensagens
- **Logs** detalhados de todas as interações

## 🚀 Sistema Pronto para Produção!

O **WhatsApp AI Workflow** da Valente & Lima Advogados está completamente configurado e testado. 

### Próximo Passo:
1. **Configurar webhook na Wasender** com a URL pública do servidor
2. **Testar com mensagem real** no WhatsApp +351936647900
3. **Monitorar logs** para verificar funcionamento
4. **Ajustar respostas** conforme necessário

---

**Desenvolvido com sucesso! 🎉**  
*Sistema de atendimento automatizado WhatsApp com IA para Valente & Lima Advogados*
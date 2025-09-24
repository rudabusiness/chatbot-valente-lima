# Configuração do Webhook na Wasender API

## 📋 Informações para Configuração

### URL do Webhook
```
http://SEU_SERVIDOR_IP:5000/webhook/whatsapp
```

### Configurações Necessárias
- **Método**: POST
- **Content-Type**: application/json
- **Eventos**: Mensagens recebidas (incoming messages)

## 🔧 Exemplo de Configuração via API

### 1. Configurar Webhook na Wasender

```bash
curl -X POST https://wasenderapi.com/api/webhook/configure \
  -H "Authorization: Bearer 3cdce09df1dcf792f5fdcde5a29fdc878cdae25231754cd3ebc67f144e14621a" \
  -H "Content-Type: application/json" \
  -d '{
    "webhook_url": "http://SEU_SERVIDOR_IP:5000/webhook/whatsapp",
    "events": ["message.received"],
    "method": "POST"
  }'
```

### 2. Testar Envio de Mensagem

```bash
curl -X POST https://wasenderapi.com/api/send-message \
  -H "Authorization: Bearer 3cdce09df1dcf792f5fdcde5a29fdc878cdae25231754cd3ebc67f144e14621a" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+351936647900",
    "text": "Teste do sistema AI Workflow - Valente & Lima"
  }'
```

## 📨 Formato do Payload Recebido

Quando uma mensagem é recebida no WhatsApp, a Wasender enviará um payload similar a este:

```json
{
  "id": "message_unique_id_123",
  "from": "+351912345678",
  "to": "+351936647900",
  "text": "Olá, gostaria de informações sobre os vossos serviços",
  "timestamp": "2024-01-01T10:30:00Z",
  "type": "text",
  "status": "received"
}
```

## 🧪 Teste Manual do Webhook

### Simular Mensagem Recebida

```bash
curl -X POST http://localhost:5000/webhook/whatsapp \
  -H "Content-Type: application/json" \
  -d '{
    "from": "+351912345678",
    "text": "Olá, preciso de ajuda com um contrato",
    "id": "test_message_001",
    "timestamp": "2024-01-01T10:30:00Z"
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
    "interaction_id": "test_message_001"
  },
  "timestamp": "2024-01-01T10:30:01.123456"
}
```

## 🔍 Verificação e Monitoramento

### Verificar Status do Sistema

```bash
curl http://localhost:5000/admin/stats
```

### Ver Logs em Tempo Real

```bash
tail -f /home/ubuntu/webhook_server.log
```

### Monitoramento Completo

```bash
./monitor_whatsapp.sh
```

## 🚨 Resolução de Problemas

### Webhook Não Recebe Mensagens

1. **Verificar conectividade**:
   ```bash
   curl http://SEU_SERVIDOR_IP:5000/health
   ```

2. **Verificar firewall**:
   ```bash
   sudo ufw allow 5000/tcp
   ```

3. **Verificar logs**:
   ```bash
   tail -50 /home/ubuntu/webhook_server.log
   ```

### Mensagens Não São Enviadas

1. **Testar API Wasender**:
   ```bash
   curl -X POST https://wasenderapi.com/api/send-message \
     -H "Authorization: Bearer SUA_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"to":"+351936647900","text":"Teste manual"}'
   ```

2. **Verificar credenciais**:
   ```bash
   cat /home/ubuntu/.api_secret_infos/api_secrets.json
   ```

## 📊 Exemplos de Conversas

### Conversa em Português

**Cliente**: "Olá, bom dia!"
**Bot**: "Olá! Bem-vindo(a) à Valente & Lima Advogados. Sou o assistente virtual e estou aqui para ajudar. Como posso ser útil hoje?"

**Cliente**: "Gostaria de agendar uma consulta"
**Bot**: "Para agendar uma consulta com os nossos advogados, pode usar o nosso sistema online: https://calendly.com/geral-valentelima

Horários de atendimento:
• Segunda a Sexta: 9:00-18:00
• Sábado: 9:00-13:00
• Fuso horário: Europa/Lisboa"

### Conversa em Inglês

**Cliente**: "Hello, I need legal advice"
**Bot**: "Hello! Welcome to Valente & Lima Advogados. I'm the virtual assistant and I'm here to help. How can I assist you today?"

**Cliente**: "I want to schedule a consultation"
**Bot**: "To schedule a consultation with our lawyers, you can use our online system: https://calendly.com/geral-valentelima

Business hours:
• Monday to Friday: 9:00-18:00
• Saturday: 9:00-13:00
• Timezone: Europa/Lisboa"

### Escalação para Humano

**Cliente**: "Preciso de falar com um advogado urgente!"
**Bot**: "Compreendo que precisa de falar com um dos nossos advogados. Vou transferir a sua conversa para um membro da nossa equipa. Por favor, aguarde um momento."

*[Sistema marca intervenção humana e pausa bot por 10 minutos]*

## 🔐 Segurança

### Validação de Webhook

O sistema valida:
- Content-Type deve ser application/json
- Payload deve conter campos obrigatórios (from, text)
- Rate limiting implícito via Flask

### Proteção de Credenciais

- API keys nunca expostas em logs
- Armazenamento seguro em arquivo protegido
- Acesso apenas via sistema de secrets

---

**Sistema pronto para produção!** 🚀
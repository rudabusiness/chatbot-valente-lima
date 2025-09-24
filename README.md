[README_WhatsApp_AI_Workflow.md](https://github.com/user-attachments/files/22503816/README_WhatsApp_AI_Workflow.md)
# WhatsApp AI Workflow - Valente & Lima Advogados

## 📋 Visão Geral

Sistema de atendimento automatizado para WhatsApp que utiliza IA para responder mensagens de clientes 24/7, com suporte bilíngue (PT-PT/EN) e escalação inteligente para advogados humanos.

## 🎯 Objetivos

- ✅ Servir como primeiro ponto de contacto no WhatsApp
- ✅ Automatizar respostas iniciais e triagem de clientes  
- ✅ Oferecer suporte em tempo real 24/7
- ✅ Reduzir tempo de resposta e aumentar eficiência
- ✅ Detectar quando escalar para atendimento humano

## 🏗️ Arquitetura do Sistema

```
WhatsApp → Wasender API → Webhook Server → AI Workflow → Resposta Automática
                                ↓
                        Logs & Monitoramento
```

## 📁 Estrutura de Arquivos

```
/home/ubuntu/
├── whatsapp_ai_workflow.py      # Lógica principal do AI Workflow
├── whatsapp_webhook_server.py   # Servidor Flask para webhooks
├── whatsapp_config.json         # Configurações do sistema
├── setup_whatsapp_workflow.sh   # Script de instalação
├── test_whatsapp_workflow.py    # Script de testes
├── monitor_whatsapp.sh          # Script de monitoramento
├── backup_whatsapp_data.sh      # Script de backup
├── logs/                        # Diretório de logs
├── backups/                     # Diretório de backups
└── .api_secret_infos/          # Credenciais da API (seguro)
```

## 🚀 Instalação e Configuração

### 1. Executar Setup Automático

```bash
cd /home/ubuntu
chmod +x setup_whatsapp_workflow.sh
./setup_whatsapp_workflow.sh
```

### 2. Iniciar o Serviço

```bash
# Iniciar serviço
sudo systemctl start whatsapp-webhook.service

# Verificar status
sudo systemctl status whatsapp-webhook.service

# Ver logs em tempo real
sudo journalctl -u whatsapp-webhook.service -f
```

### 3. Testar o Sistema

```bash
# Teste básico
python3 test_whatsapp_workflow.py

# Monitoramento completo
./monitor_whatsapp.sh
```

## 🔧 Configuração da Wasender API

### 1. Configurar Webhook na Wasender

- **URL do Webhook**: `http://SEU_SERVIDOR:5000/webhook/whatsapp`
- **Método**: POST
- **Content-Type**: application/json
- **Eventos**: Mensagens recebidas

### 2. Formato do Payload Esperado

```json
{
  "from": "+351936647900",
  "text": "Mensagem do cliente",
  "id": "message_id_unique",
  "timestamp": "2024-01-01T10:00:00Z"
}
```

## 🤖 Funcionalidades da IA

### Detecção de Idioma
- Automática baseada em palavras-chave
- Suporte para PT-PT e EN
- Resposta no mesmo idioma da mensagem

### Intenções Reconhecidas

#### Português (PT-PT)
- **Saudações**: "olá", "bom dia", "boa tarde"
- **Serviços**: "serviços", "áreas", "especialidades"  
- **Agendamento**: "agendar", "marcar", "consulta"
- **Horários**: "horário", "funcionamento"
- **Localização**: "onde", "morada", "escritório"

#### Inglês (EN)
- **Greetings**: "hello", "good morning", "good afternoon"
- **Services**: "services", "areas", "specialties"
- **Appointment**: "schedule", "book", "appointment"
- **Hours**: "hours", "schedule", "open"
- **Location**: "where", "location", "address"

### Escalação Automática

O sistema escala para atendimento humano quando detecta:

#### Português
- "falar com advogado"
- "pessoa real"
- "urgente" / "emergência"
- "insatisfeito" / "reclamação"

#### Inglês  
- "speak to lawyer"
- "real person"
- "urgent" / "emergency"
- "unsatisfied" / "complaint"

## 🔄 Fluxo de Atendimento

### 1. Mensagem Recebida
```
Cliente → WhatsApp → Wasender → Webhook Server
```

### 2. Processamento
```
Webhook Server → AI Workflow → Detecção de Idioma → Geração de Resposta
```

### 3. Controle de Escalação
```
Verificar Intervenção Humana → Pausar Bot (se ativo) → Cooldown 10min
```

### 4. Resposta Automática
```
AI Workflow → Wasender API → WhatsApp → Cliente
```

## 📊 Monitoramento e Logs

### Endpoints de Monitoramento

- **Health Check**: `GET /health`
- **Estatísticas**: `GET /admin/stats`  
- **Teste Manual**: `POST /admin/test`

### Arquivos de Log

- **Servidor**: `/home/ubuntu/webhook_server.log`
- **Workflow**: `/home/ubuntu/whatsapp_logs.log`
- **Interações**: `/home/ubuntu/whatsapp_interactions_YYYYMM.json`

### Script de Monitoramento

```bash
# Executar monitoramento completo
./monitor_whatsapp.sh
```

## 💾 Backup e Recuperação

### Backup Automático
- Executa diariamente às 02:00
- Mantém últimos 7 backups
- Inclui logs, configurações e credenciais

### Backup Manual
```bash
./backup_whatsapp_data.sh
```

### Restaurar Backup
```bash
cd /home/ubuntu/backups
tar -xzf whatsapp_backup_YYYYMMDD_HHMMSS.tar.gz -C /
```

## 🔒 Segurança

### Credenciais
- API keys armazenadas em `/home/ubuntu/.api_secret_infos/`
- Arquivo protegido com permissões 600
- Nunca expostas em logs

### Webhook Security
- Token de verificação configurado
- Validação de payload JSON
- Rate limiting implícito via Flask

### Firewall
```bash
# Permitir apenas porta necessária
sudo ufw allow 5000/tcp
```

## 🛠️ Manutenção

### Comandos Úteis

```bash
# Reiniciar serviço
sudo systemctl restart whatsapp-webhook.service

# Ver logs em tempo real
tail -f /home/ubuntu/webhook_server.log

# Verificar espaço em disco
df -h /home/ubuntu

# Limpar logs antigos (>30 dias)
find /home/ubuntu -name "*.log" -mtime +30 -delete
```

### Atualizações

1. Parar serviço: `sudo systemctl stop whatsapp-webhook.service`
2. Fazer backup: `./backup_whatsapp_data.sh`
3. Atualizar arquivos
4. Reiniciar serviço: `sudo systemctl start whatsapp-webhook.service`
5. Testar: `python3 test_whatsapp_workflow.py`

## 📞 Informações de Contacto

### Empresa
- **Nome**: Valente & Lima Advogados
- **Localizações**: Braga e Lisboa  
- **WhatsApp**: +351936647900
- **Agendamentos**: https://calendly.com/geral-valentelima

### Horários de Atendimento
- **Segunda a Sexta**: 9:00-18:00
- **Sábado**: 9:00-13:00
- **Fuso Horário**: Europa/Lisboa
- **Bot**: 24/7 (triagem inicial)

## 🐛 Resolução de Problemas

### Serviço Não Inicia
```bash
# Verificar logs
sudo journalctl -u whatsapp-webhook.service -n 50

# Verificar dependências
pip3 install flask requests python-dateutil

# Verificar permissões
chmod +x /home/ubuntu/whatsapp_webhook_server.py
```

### Webhook Não Recebe Mensagens
```bash
# Testar conectividade
curl http://localhost:5000/health

# Verificar firewall
sudo ufw status

# Testar webhook manualmente
curl -X POST http://localhost:5000/admin/test
```

### Mensagens Não São Enviadas
```bash
# Verificar credenciais da API
cat /home/ubuntu/.api_secret_infos/api_secrets.json

# Testar API Wasender manualmente
curl -X POST https://wasenderapi.com/api/send-message \
  -H "Authorization: Bearer SUA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"to":"+351936647900","text":"Teste"}'
```

## 📈 Métricas e KPIs

### Métricas Disponíveis
- Número de mensagens processadas
- Taxa de escalação para humanos
- Tempo de resposta médio
- Distribuição por idioma
- Horários de maior atividade

### Relatórios Mensais
Os logs de interação são salvos mensalmente em:
`/home/ubuntu/whatsapp_interactions_YYYYMM.json`

## 🔮 Próximas Funcionalidades

- [ ] Integração com CRM
- [ ] Análise de sentimento
- [ ] Respostas personalizadas por cliente
- [ ] Dashboard web de monitoramento
- [ ] Integração com Google Calendar
- [ ] Suporte a anexos (imagens, documentos)
- [ ] Chatbot mais avançado com contexto de conversa

---

**Desenvolvido para Valente & Lima Advogados**  
*Sistema de atendimento automatizado WhatsApp com IA*

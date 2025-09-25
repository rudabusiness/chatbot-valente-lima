Aqui está um README_DEPLOY.md 100% adaptado para o Railway, com instruções claras, passo a passo, prontas para incluir no seu repositório:

⸻

📄 README_DEPLOY.md

# 🚀 Deploy do WhatsApp AI Workflow – Valente & Lima Advogados

Este repositório contém o sistema de atendimento automatizado via WhatsApp, com IA multilíngue (PT-PT/EN), escalonamento inteligente para humanos e integração com a API Wasender.

---

## ✅ Visão Geral do Projeto

- Recebe mensagens via WhatsApp usando a Wasender API
- Processa mensagens com inteligência artificial (detecção de idioma e intenção)
- Responde automaticamente ou escala para advogados humanos
- Totalmente funcional com logs, backup e monitoramento
- Deploy fácil e gratuito via Railway

---

## ⚙️ Tecnologias Usadas

- Python 3.8+
- Flask
- Wasender API
- Railway.app (deploy cloud)

---

## 🪜 Etapas para Deploy via Railway

### 1. 🧬 Pré-requisitos

- Conta no [https://railway.app](https://railway.app)
- Conta no GitHub com este repositório clonado
- Chave da API da Wasender

---

### 2. 📁 Estrutura Esperada no Repositório

Certifique-se de que seu projeto contenha:

```bash
.
├── whatsapp_webhook_server.py       # Servidor Flask principal
├── whatsapp_ai_workflow.py          # Lógica do assistente
├── whatsapp_config.json             # Configurações
├── requirements.txt                 # Dependências Python
├── Procfile                         # Comando para rodar no Railway


⸻

3. 🧪 Criar os Arquivos Necessários

requirements.txt

flask
requests
python-dateutil

Procfile

web: python3 whatsapp_webhook_server.py

Adicione e suba os arquivos com:

git add requirements.txt Procfile
git commit -m "Add arquivos para deploy Railway"
git push origin main


⸻

4. 🚀 Deploy no Railway
	1.	Acesse https://railway.app
	2.	Clique em “New Project” → “Deploy from GitHub”
	3.	Escolha o repositório chatbot-valente-lima
	4.	Railway detecta Python automaticamente e usa:
	•	requirements.txt para dependências
	•	Procfile para iniciar o app

⸻

5. 🌍 URL Pública

Após o deploy, você receberá uma URL como:

https://chatbot-valente-lima.up.railway.app

Teste com:

curl https://chatbot-valente-lima.up.railway.app/health

Resposta esperada:

{"status": "ok"}


⸻

6. 🔗 Configurar Wasender API

Configure o webhook com a URL da Railway:

curl -X POST https://wasenderapi.com/api/webhook/configure \
  -H "Authorization: Bearer SUA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "webhook_url": "https://chatbot-valente-lima.up.railway.app/webhook/whatsapp",
    "events": ["message.received"],
    "method": "POST"
  }'


⸻

7. 🧪 Teste o Bot

Simule:

curl -X POST https://chatbot-valente-lima.up.railway.app/webhook/whatsapp \
  -H "Content-Type: application/json" \
  -d '{
    "from": "+351912345678",
    "text": "Olá, preciso de ajuda jurídica",
    "id": "teste001"
  }'


⸻

✅ Endpoints Disponíveis

Endpoint	Método	Descrição
/health	GET	Verifica status do servidor
/webhook/whatsapp	POST	Recebe mensagens do WhatsApp
/admin/stats	GET	Estatísticas básicas
/admin/test	POST	Teste manual de resposta


⸻

📊 Métricas Coletadas
	•	Total de mensagens
	•	Idioma detectado (PT/EN)
	•	Interações por horário
	•	Escalações para humanos

⸻

🔐 Segurança
	•	API Key protegida em arquivo .api_secret_infos/
	•	Webhook com payload validado
	•	Limite de taxa via lógica Flask
	•	Nenhum dado sensível exposto nos logs

⸻

🤝 Contato

Valente & Lima Advogados
📍 Escritórios em Braga e Lisboa
📱 WhatsApp: +351 936 647 900
📅 Agendamentos: https://calendly.com/geral-valentelima
🌐 Website: https://valentelima.com

⸻

Desenvolvido com ❤️ para automatizar, servir e escalar!

---

### ✅ O que fazer agora

1. Crie esse arquivo `README_DEPLOY.md` direto no GitHub:
   - Clique em **“Add file” → “Create new file”**
   - Nome: `README_DEPLOY.md`
   - Cole o conteúdo acima
   - Commit direto na branch `main`

2. Pronto! Agora seu projeto está totalmente documentado para qualquer dev ou sócio da equipa poder implantar ou escalar 🚀

---

Se quiser, posso também gerar:

- `Dockerfile` para futuro deploy em VPS
- Um **Painel React** para ver as métricas em tempo real
- Uma integração com Google Sheets, Google Calendar, ou Notion

Só dizer!

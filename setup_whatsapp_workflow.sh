#!/bin/bash

# Setup script para WhatsApp AI Workflow - Valente & Lima Advogados
# Este script instala e configura todo o ambiente necessário

echo "🚀 Configurando WhatsApp AI Workflow - Valente & Lima Advogados"
echo "=============================================================="

# Atualizar sistema
echo "📦 Atualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar Python e pip se necessário
echo "🐍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "Instalando Python3..."
    sudo apt install python3 python3-pip -y
fi

# Instalar dependências Python
echo "📚 Instalando dependências Python..."
pip3 install flask requests python-dateutil

# Criar diretórios necessários
echo "📁 Criando estrutura de diretórios..."
mkdir -p /home/ubuntu/logs
mkdir -p /home/ubuntu/backups

# Tornar scripts executáveis
echo "🔧 Configurando permissões..."
chmod +x /home/ubuntu/whatsapp_ai_workflow.py
chmod +x /home/ubuntu/whatsapp_webhook_server.py

# Criar serviço systemd para o webhook server
echo "⚙️ Criando serviço systemd..."
sudo tee /etc/systemd/system/whatsapp-webhook.service > /dev/null <<EOF
[Unit]
Description=WhatsApp AI Workflow Webhook Server
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu
ExecStart=/usr/bin/python3 /home/ubuntu/whatsapp_webhook_server.py
Restart=always
RestartSec=10
Environment=PYTHONPATH=/home/ubuntu

[Install]
WantedBy=multi-user.target
EOF

# Recarregar systemd e habilitar serviço
sudo systemctl daemon-reload
sudo systemctl enable whatsapp-webhook.service

# Criar script de backup
echo "💾 Criando script de backup..."
tee /home/ubuntu/backup_whatsapp_data.sh > /dev/null <<EOF
#!/bin/bash
# Script de backup dos dados do WhatsApp AI Workflow

BACKUP_DIR="/home/ubuntu/backups"
DATE=\$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="\$BACKUP_DIR/whatsapp_backup_\$DATE.tar.gz"

echo "Criando backup em \$BACKUP_FILE..."

tar -czf "\$BACKUP_FILE" \\
    /home/ubuntu/whatsapp_*.json \\
    /home/ubuntu/whatsapp_*.log \\
    /home/ubuntu/.api_secret_infos/ \\
    2>/dev/null

echo "Backup criado com sucesso!"

# Manter apenas os últimos 7 backups
find "\$BACKUP_DIR" -name "whatsapp_backup_*.tar.gz" -mtime +7 -delete
EOF

chmod +x /home/ubuntu/backup_whatsapp_data.sh

# Criar cron job para backup diário
echo "⏰ Configurando backup automático..."
(crontab -l 2>/dev/null; echo "0 2 * * * /home/ubuntu/backup_whatsapp_data.sh") | crontab -

# Criar script de monitoramento
echo "📊 Criando script de monitoramento..."
tee /home/ubuntu/monitor_whatsapp.sh > /dev/null <<EOF
#!/bin/bash
# Script de monitoramento do WhatsApp AI Workflow

echo "=== Status do WhatsApp AI Workflow ==="
echo "Data: \$(date)"
echo ""

# Verificar se o serviço está rodando
echo "🔍 Status do serviço:"
sudo systemctl status whatsapp-webhook.service --no-pager -l

echo ""
echo "📊 Estatísticas do servidor:"
curl -s http://localhost:5000/admin/stats | python3 -m json.tool

echo ""
echo "📝 Últimas linhas do log:"
tail -10 /home/ubuntu/webhook_server.log

echo ""
echo "💾 Espaço em disco:"
df -h /home/ubuntu
EOF

chmod +x /home/ubuntu/monitor_whatsapp.sh

# Criar arquivo de teste
echo "🧪 Criando script de teste..."
tee /home/ubuntu/test_whatsapp_workflow.py > /dev/null <<EOF
#!/usr/bin/env python3
"""
Script de teste para o WhatsApp AI Workflow
"""

import requests
import json
from datetime import datetime

def test_webhook_server():
    """Testa o servidor webhook"""
    print("🧪 Testando servidor webhook...")
    
    # Teste de health check
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check: OK")
        else:
            print(f"❌ Health check falhou: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro no health check: {e}")
    
    # Teste de webhook
    try:
        test_data = {
            "from": "+351912345678",
            "text": "Olá, este é um teste do sistema",
            "id": f"test_{int(datetime.now().timestamp())}"
        }
        
        response = requests.post(
            "http://localhost:5000/admin/test",
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Teste de webhook: OK")
            result = response.json()
            print(f"📄 Resultado: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Teste de webhook falhou: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro no teste de webhook: {e}")

if __name__ == "__main__":
    test_webhook_server()
EOF

chmod +x /home/ubuntu/test_whatsapp_workflow.py

# Configurar firewall (se ufw estiver instalado)
if command -v ufw &> /dev/null; then
    echo "🔒 Configurando firewall..."
    sudo ufw allow 5000/tcp
fi

echo ""
echo "✅ Configuração concluída com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo "1. Iniciar o serviço: sudo systemctl start whatsapp-webhook.service"
echo "2. Verificar status: sudo systemctl status whatsapp-webhook.service"
echo "3. Testar sistema: python3 /home/ubuntu/test_whatsapp_workflow.py"
echo "4. Monitorar: /home/ubuntu/monitor_whatsapp.sh"
echo ""
echo "🌐 Endpoints disponíveis:"
echo "- Health check: http://localhost:5000/health"
echo "- Webhook: http://localhost:5000/webhook/whatsapp"
echo "- Estatísticas: http://localhost:5000/admin/stats"
echo "- Teste: http://localhost:5000/admin/test"
echo ""
echo "📚 Configurar na Wasender:"
echo "URL do webhook: http://SEU_SERVIDOR:5000/webhook/whatsapp"
echo "Método: POST"
echo "Content-Type: application/json"
EOF

chmod +x /home/ubuntu/setup_whatsapp_workflow.sh
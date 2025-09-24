#!/bin/bash
# Script de monitoramento do WhatsApp AI Workflow

echo "=== Status do WhatsApp AI Workflow ==="
echo "Data: $(date)"
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

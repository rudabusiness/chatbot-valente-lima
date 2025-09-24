#!/bin/bash
# Script de backup dos dados do WhatsApp AI Workflow

BACKUP_DIR="/home/ubuntu/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/whatsapp_backup_$DATE.tar.gz"

echo "Criando backup em $BACKUP_FILE..."

tar -czf "$BACKUP_FILE" \
    /home/ubuntu/whatsapp_*.json \
    /home/ubuntu/whatsapp_*.log \
    /home/ubuntu/.api_secret_infos/ \
    2>/dev/null

echo "Backup criado com sucesso!"

# Manter apenas os últimos 7 backups
find "$BACKUP_DIR" -name "whatsapp_backup_*.tar.gz" -mtime +7 -delete

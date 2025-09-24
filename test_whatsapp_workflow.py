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

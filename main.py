import requests
import config


def obter_cotacao_dolar() -> float:
    """Busca a cotação atual do Dólar (USD-BRL) via AwesomeAPI."""
    url = "https://economia.awesomeapi.com.br/last/USD-BRL"
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        dados = response.json()
        return float(dados["USDBRL"]["bid"])
    else:
        raise Exception(f"Erro ao buscar cotação na API: Status {response.status_code}")


def enviar_mensagem_telegram(mensagem: str) -> None:
    """Envia uma notificação para o Telegram configurado e valida a resposta."""
    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, json=payload, timeout=10)

    if response.status_code == 200:
        print("✅ Notificação enviada com sucesso para o Telegram!")
    else:
        print(f"❌ Falha ao enviar mensagem no Telegram. Código HTTP: {response.status_code}")
        print(f"📄 Resposta detalhada da API do Telegram: {response.text}")


def monitorar():
    print("🚀 Iniciando monitoramento da cotação do Dólar...")

    try:
        cotacao_atual = obter_cotacao_dolar()
        print(f"💵 Cotação atual do Dólar: R$ {cotacao_atual:.2f}")

        if cotacao_atual <= config.LIMITE_DOLAR:
            alerta = (
                f"⚠️ *ALERTA DE PREÇO!*\n\n"
                f"O Dólar atingiu a meta!\n"
                f"🔹 Valor atual: *R$ {cotacao_atual:.2f}*\n"
                f"🎯 Limite configurado: *R$ {config.LIMITE_DOLAR:.2f}*"
            )
            enviar_mensagem_telegram(alerta)
        else:
            print(
                f"ℹ️ Cotação (R$ {cotacao_atual:.2f}) acima do limite (R$ {config.LIMITE_DOLAR:.2f}). Nenhum alerta enviado.")

    except Exception as e:
        print(f"❌ Ocorreu um erro no script: {e}")


if __name__ == "__main__":
    monitorar()
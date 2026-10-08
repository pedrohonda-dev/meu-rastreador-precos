import telebot
import requests
from config import TELEGRAM_BOT_TOKEN

# Inicializa o bot do Telegram com o seu token
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


def obter_cotacao_dolar():
    """Consulta a API para obter o valor atual do Dólar."""
    url = "https://economia.awesomeapi.com.br/last/USD-BRL"
    try:
        response = requests.get(url)
        data = response.json()
        cotacao = float(data['USDBRL']['bid'])
        return cotacao
    except Exception as e:
        print(f"Erro ao obter cotação: {e}")
        return None


# Responde aos comandos /start e /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    texto = (
        "Olá! 🤖\n"
        "Eu sou o Bot de Cotação do Dólar.\n\n"
        "Envie qualquer mensagem ou digite /dolar para saber o valor atual do Dólar em tempo real!"
    )
    bot.reply_to(message, texto)


# Responde a qualquer mensagem enviada ao bot
@bot.message_handler(func=lambda message: True)
def responder_cotacao(message):
    cotacao = obter_cotacao_dolar()

    if cotacao:
        resposta = f"💵 A cotação atual do Dólar (USD-BRL) é: **R$ {cotacao:.2f}**"
    else:
        resposta = "⚠️ Desculpe, não consegui obter a cotação no momento. Tente novamente em instantes."

    bot.reply_to(message, resposta, parse_mode="Markdown")


if __name__ == "__main__":
    print("🤖 Bot iniciado e aguardando mensagens no Telegram...")
    # Mantém o script em execução escutando novas mensagens continuamente
    bot.infinity_polling()
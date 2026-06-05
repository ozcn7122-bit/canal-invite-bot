import os
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_1 = os.environ.get("CHANNEL_1")
CHANNEL_2 = os.environ.get("CHANNEL_2")

from flask import Flask, request
app = Flask(__name__)

def send_message(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup:
        data["reply_markup"] = reply_markup
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json=data)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if not data:
        return "ok", 200
    msg = data.get("message", {})
    callback = data.get("callback_query", {})

    if msg.get("text") == "/start":
        chat_id = msg["chat"]["id"]
        keyboard = {
            "inline_keyboard": [
                [{"text": "📢 NeedKYC", "callback_data": "channel_1"}],
                [{"text": "🛍 ShopYourStore", "callback_data": "channel_2"}]
            ]
        }
        send_message(chat_id, "👋 Bienvenue ! Choisis un canal :", keyboard)

    elif callback:
        chat_id = callback["message"]["chat"]["id"]
        message_id = callback["message"]["message_id"]
        channel_id = CHANNEL_1 if callback["data"] == "channel_1" else CHANNEL_2
        name = "NeedKYC" if callback["data"] == "channel_1" else "ShopYourStore"

        r = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/createChatInviteLink",
            json={"chat_id": channel_id, "member_limit": 1}
        )
        link = r.json().get("result", {}).get("invite_link", "Erreur")

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText",
            json={"chat_id": chat_id, "message_id": message_id,
                  "text": f"✅ Ton lien pour *{name}* :\n{link}", "parse_mode": "Markdown"}
        )
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",
                      json={"callback_query_id": callback["id"]})

    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

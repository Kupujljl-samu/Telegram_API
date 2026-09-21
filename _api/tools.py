import json, urllib.request, urllib.error, urllib.parse
from pydantic import BaseModel

class Packet(BaseModel):
    token: str
    chat: int
    text: str

def send_and_forget(chat_id, token, text):
    try:
        response = send_telegram_message(
            token,
            chat_id,
            text
        )
        
        if not response.get("ok"):
            return(f"❌ Ошибка: {response}")  
    except urllib.error.HTTPError as e:
        return f"❌ HTTP ошибка: {e.code} — {e.read().decode()}"
    except Exception as e:
        return f"❌ Ошибка: {e}"

def send_telegram_message(bot_token: str, chat_id: str, text: str) -> dict:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"  # или "Markdown"
    }).encode("utf-8")
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST"
    )
    
    with urllib.request.urlopen(req, timeout=10) as response:
        result = json.loads(response.read().decode("utf-8"))
        return result

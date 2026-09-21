from endstone.plugin import Plugin
from endstone.event import event_handler, PlayerJoinEvent
import subprocess, sys

class Main(Plugin):
    api_version = "0.11"
    authors = ["Samurai_project"]
    prefix = "TG_Bot"

    def on_load(self):
        self.save_default_config()
        self.reload_config()
        try: import requests
        except ImportError: 
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
            import requests
        self.lib = requests

    def on_enable(self):
        self.register_events(self)

    @event_handler
    def ev_join(self, e:PlayerJoinEvent):
        text = f"Игрок '{e.player.name}' присоединился к серверу!"
        self.server.scheduler.run_task(self, lambda t=text: self.send_to_api(t), 20)

    def send_to_api(self, text: str):
        url = f"http://{self.config.get('ip')}:{self.config.get('port')}/telegram" 
        payload = {
            "token": str(self.config.get('token')),
            "chat": int(self.config.get('chat', -1)),
            "text": text
        }
        try:
            response = self.lib.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                return True
            else:
                self.logger.warning(f"API вернул ошибку {response.status_code}: {response.text}")
                return False
        except self.lib.exceptions.RequestException as e:
            self.logger.warning(f"Не удалось связаться с сервером: {e}")
            return False

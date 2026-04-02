import requests

class TelegramNotification:
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id

    def send_message_whith_document(self, message: str, path_to_file: str):
        api_url = f"https://api.telegram.org/bot{self.bot_token}/sendDocument"

        with open(path_to_file, "rb") as file_content:
            response = requests.post(
                api_url,
                data={
                    "chat_id": self.chat_id,
                    "caption": message
                },
                files={"document": file_content}
            )

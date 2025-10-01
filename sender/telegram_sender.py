import os
import re

import requests


class TelegramSender:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send_message(self, text: str, parse_mode="MarkdownV2") -> bool:
        url = self.base_url + "/sendMessage"

        if parse_mode == "MarkdownV2":
            text = self._escape_special_chars(text)

        params = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode,
        }

        try:
            response = requests.post(url, params=params)
            response.raise_for_status()
            data = response.json()
            if data.get("ok"):
                return True
            else:
                print(
                    f"Failed to send message: {data.get('description', 'Unknown error')}"
                )
                return False

        except requests.exceptions.HTTPError as e:
            print(
                f"HTTP error occurred while sending message: {e} - Response: {e.response.text}"
            )
            return False
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error occurred while sending message: {e}")
            return False
        except requests.exceptions.Timeout as e:
            print(f"Timeout error occurred while sending message: {e}")
            return False
        except requests.exceptions.RequestException as e:
            print(f"An unknown request error occurred while sending message: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def _escape_special_chars(self, text: str) -> str:
        special_chars = "_*[]()~`>#+-=|{}.!"

        # Split text into different parts: code blocks and simple text
        parts = []
        pos = 0

        # Pattern to search PAIRED code block quotes (``` или `)
        # First search ```, than single ` (always paired)
        pattern = r"(```[\s\S]*?```|`[^`]+?`)"

        for match in re.finditer(pattern, text):
            # Add text before code block (escape it)
            before = text[pos : match.start()]
            parts.append(self._escape_text(before, special_chars))

            # Add code block as it is
            parts.append(match.group(0))

            pos = match.end()

        # Add remain text after last code block (escape it)
        parts.append(self._escape_text(text[pos:], special_chars))

        return "".join(parts)

    def _escape_text(self, text, special_chars) -> str:
        result = []
        for char in text:
            if char in special_chars:
                result.append("\\" + char)
            else:
                result.append(char)
        return "".join(result)

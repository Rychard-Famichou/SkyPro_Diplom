import base64
import re

from django.core.mail.backends.console import EmailBackend


class ReadableConsoleEmailBackend(EmailBackend):

    def write_message(self, message):
        # Получаем сырой текст письма
        raw_message = message.message().as_string()

        # Функция для поиска и декодирования блоков base64
        def decode_base64_block(match):
            try:
                decoded_bytes = base64.b64decode(match.group(1))
                return decoded_bytes.decode("utf-8", errors="replace")
            except Exception:
                return match.group(0)

        # Декодируем тело письма, если оно в base64
        readable_message = re.sub(
            r"\n\n([A-Za-z0-9+/=\s\n]+)\n\n--===",
            decode_base64_block,
            raw_message,
        )

        # Передаем уже читаемый текст в стандартный поток вывода
        self.stream.write(readable_message)
        self.stream.flush()

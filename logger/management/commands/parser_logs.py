import json
from datetime import datetime
from typing import Optional
import httpx
from django.core.management.base import BaseCommand
from logger.models import NginxLog


class Command(BaseCommand):
    help = 'Parses logs from log files'

    def add_arguments(self, parser):
        parser.add_argument('log_file_url', type=str, help='URL of log file')

    def handle(self, *args, **kwargs) -> None:
        """
        Читаем файл с логами по ссылке построчно и сохраняем записи в базу данных.
        """
        log_file_url = kwargs['log_file_url']
        direct_link = self.convert_google_drive_url(log_file_url)
        log_entries = []  # Список для накопления записей

        try:
            with httpx.stream('GET', direct_link, follow_redirects=True) as response:
                response.raise_for_status()  # Проверка статуса ответа

                for line in response.iter_lines():
                    if line:
                        log_entry = self.process_log_line(line)  # Обрабатываем строку
                        if log_entry:
                            log_entries.append(log_entry)  # Добавляем запись в список

            # Сохраняем все записи в базу данных одной транзакцией
            NginxLog.objects.bulk_create(log_entries)

            self.stdout.write(self.style.SUCCESS("Парсинг завершён"))
        except httpx.RequestError as e:
            self.stderr.write(self.style.ERROR(f"Ошибка при загрузке файла: {e}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Ошибка при обработке файла: {e}"))

    def convert_google_drive_url(self, url: str) -> str:
        """
        Преобразуем стандартную Google Drive ссылку в прямую ссылку для скачивания.
        """
        if "drive.google.com" in url and "/file/d/" in url:
            # Извлекаем ID файла
            file_id = url.split('/d/')[1].split('/')[0]
            # Создаем прямую ссылку
            return f"https://drive.google.com/uc?export=download&id={file_id}"
        return url

    def process_log_line(self, line: str) -> Optional[NginxLog]:
        """
        Извлекаем данные из строки лога и создаем объект NginxLog.
        """
        try:
            log_data = json.loads(line)
            request_data = log_data['request'].split()
            method = request_data[0]
            uri = request_data[1]
            protocol = request_data[2]

            log_entry = NginxLog(
                ip_address=log_data["remote_ip"],
                request_date=datetime.strptime(log_data['time'], "%d/%b/%Y:%H:%M:%S %z"),
                remote_user=log_data.get("remote_user", "-"),
                http_method=method,
                uri=uri,
                protocol=protocol,
                response_code=log_data["response"],
                response_size=log_data["bytes"],
                referrer=log_data.get("referrer", "-"),
                user_agent=log_data["agent"]
            )
            return log_entry
        except (KeyError, ValueError, IndexError) as e:
            self.stdout.write(self.style.WARNING(f"Ошибка при парсинге строки: {e}"))
            return None
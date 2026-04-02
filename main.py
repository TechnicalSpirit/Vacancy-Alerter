from datetime import datetime, timedelta, timezone

from src.job_sources.hh import HHClient
from src.standardized_vacancie_by_template.vacancie_by_template import VacancieByTemplate
from src.notification_channels.telegram.telegram_notification import TelegramNotification
from src.report_сreator.report_сreator import CreateExelReport

from dotenv import load_dotenv
import os

load_dotenv() 

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

now = datetime.now(timezone.utc)
yesterday_start = (now - timedelta(days=1)).replace(
    hour=0, minute=0, second=0, microsecond=0
)

yesterday_end = yesterday_start.replace(
    hour=23, minute=59, second=59
)

hh = HHClient()
respons = hh.search_vacancies_by_parameters(
    {
        "schedule": "remote",
        "date_from": yesterday_start.isoformat(),
        "date_to": yesterday_end.isoformat(),
    }
)

standardizer = VacancieByTemplate()
standart_vacancies = []
for vacancie in respons["items"]:
    standart_vacancie = standardizer.standardized_hh_vacancie_by_template(vacancie)
    standart_vacancies.append(standart_vacancie)

report_creator = CreateExelReport()
path_to_report = report_creator.create_report(standart_vacancies)

telegram_notification = TelegramNotification(BOT_TOKEN, CHAT_ID)
telegram_notification.send_message_whith_document(f"""
Отчёт по вакансиям

Количество вакансий: {len(standart_vacancies)}

С {yesterday_start.strftime('%H:%M:%S %d.%m.%Y')}
По {yesterday_end.strftime('%H:%M:%S %d.%m.%Y')}
""",path_to_report)
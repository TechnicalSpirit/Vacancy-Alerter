from datetime import datetime, timedelta

class VacancieByTemplate:

    def standardized_hh_vacancie_by_template(self, vacancie:dict):
        salary = vacancie.get("salary") or {}
        time_info = self._get_time_info(vacancie)

        return {
            "Должность": vacancie["name"],
            "Формат": vacancie["schedule"]["name"],
            "Ссылка": vacancie["alternate_url"],
            "Зарплата от": salary.get("from"),
            "Зарплата до": salary.get("to"),
            "Валюта": salary.get("currency"),
            "Время публикации вакансии": time_info["published_formatted"],
            "Время публичной доступности вакансии": time_info["time_online_formatted"],
            "Время публикации вакансии с корректировкой": time_info["adjusted_published_formatted"],
        }
    
    def _get_time_info(self, vacancie):
        published = datetime.strptime(vacancie["published_at"], "%Y-%m-%dT%H:%M:%S%z")
        now = datetime.now(published.tzinfo)

        time_online = now - published
        adjusted_published = published + timedelta(hours=3) - timedelta(days=1)

        published_formatted = published.strftime("%H:%M:%S %d.%m.%Y")
        adjusted_published_formatted = adjusted_published.strftime("%H:%M:%S %d.%m.%Y")

        days = time_online.days
        hours, remainder = divmod(time_online.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_online_formatted = f"{days}d {hours:02}:{minutes:02}:{seconds:02}"

        return {
            "published_formatted": published_formatted,
            "adjusted_published_formatted": adjusted_published_formatted,
            "time_online_formatted": time_online_formatted,
        }
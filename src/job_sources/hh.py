import requests


class HHClient:
    BASE_URL = "https://api.hh.ru"

    def __init__(self, user_agent="hh-client/1.0"):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": user_agent
        })

    def get_vacancy_by_id(self, vacancy_id:str):
        response = self.session.get(f"{self.BASE_URL}/vacancies/{vacancy_id}")
        response.raise_for_status()
        return response.json()

    def search_vacancies_by_parameters(self, params:dict):
        response = self.session.get(f"{self.BASE_URL}/vacancies", params=params)
        response.raise_for_status()
        return response.json()
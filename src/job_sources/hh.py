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

    def search_vacancies_by_parameters(self, params: dict):
        all_vacancies = []
        page = 0

        while True:
            params.update({
                "page": page,
                "per_page": 100  # максимум
            })

            response = self.session.get(f"{self.BASE_URL}/vacancies", params=params)
            response.raise_for_status()
            data = response.json()

            all_vacancies.extend(data["items"])

            if page >= data["pages"] - 1:
                break

            page += 1

        return all_vacancies
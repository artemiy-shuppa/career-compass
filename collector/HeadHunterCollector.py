import requests


class HeadHunterCollector:
    def collect(self, text: str):
        response = self._get_vacancy_list(text=text)

        vacancies = response.json()["items"]

        return vacancies

    def _get_vacancy_list(self, text: str) -> requests.Response:
        params = {
            "text": text,
            "page": 0,
            "per_page": 10,
        }

        url = "https://api.hh.ru/vacancies"
        response = requests.get(url, params=params)
        return response

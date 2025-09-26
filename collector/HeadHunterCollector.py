from typing import Dict

import requests


class HeadHunterCollector:
    def collect(self, text: str):
        response = self._get_vacancy_list(text=text)

        vacancies = response.json()["items"]

        detailed_vacancy_list = []

        ids = [vacancy["id"] for vacancy in vacancies]
        for id in ids:
            detailed_vacancy = self._get_detailed_vacancy(id)

            filtered_vacancy = HeadHunterCollector._filter_vacancy(
                detailed_vacancy.json()
            )

            detailed_vacancy_list.append(filtered_vacancy)

        return detailed_vacancy_list

    def _get_vacancy_list(self, text: str) -> requests.Response:
        params = {
            "text": text,
            "page": 0,
            "per_page": 10,
        }

        url = "https://api.hh.ru/vacancies"
        response = requests.get(url, params=params)
        return response

    def _get_detailed_vacancy(self, vacancy_id: str) -> requests.Response:
        url = f"https://api.hh.ru/vacancies/{vacancy_id}"
        response = requests.get(url)

        return response

    @classmethod
    def _filter_vacancy(cls, vacancy: Dict) -> Dict:
        return {
            "id": vacancy["id"],
            "name": vacancy["name"],
            "employer_name": vacancy["employer"]["name"],
            "description": vacancy["description"],
            "alternate_url": vacancy["alternate_url"],
            "key_skills": vacancy["key_skills"],
        }

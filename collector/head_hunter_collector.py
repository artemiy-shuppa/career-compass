import requests

from config_schema import SearchParameters


class HeadHunterCollector:
    def collect(self, config: SearchParameters):
        vacancies = self._get_vacancy_list(config.keywords, config.max_vacancies)

        detailed_vacancy_list = []

        ids = [vacancy["id"] for vacancy in vacancies]
        for id in ids:
            detailed_vacancy = self._get_detailed_vacancy(id)

            filtered_vacancy = HeadHunterCollector._filter_vacancy(
                detailed_vacancy.json()
            )

            detailed_vacancy_list.append(filtered_vacancy)

        return detailed_vacancy_list

    def _get_vacancy_list(
        self, keywords: str, max_vacancies: int, max_per_page=100
    ) -> list[dict]:
        if max_vacancies < 0:
            raise ValueError("Bad 'max_vacancies' value")

        page = 0  # hh.ru starts from 0
        elements_collected = 0
        all_data = []

        while elements_collected < max_vacancies:
            remaining_elements = max_vacancies - elements_collected
            current_per_page = min(remaining_elements, max_per_page)

            params = {
                "text": keywords,
                "page": page,
                "per_page": current_per_page,
            }
            url = "https://api.hh.ru/vacancies"
            response = requests.get(url, params=params)

            # Handle response
            current_data = response.json()["items"]
            all_data.extend(current_data)
            elements_collected += len(current_data)

            # Check for case when got less elements - meaning end of data
            if len(current_data) < current_per_page:
                break

            page += 1

        # return all we got
        return all_data[:max_vacancies]

    def _get_detailed_vacancy(self, vacancy_id: str) -> requests.Response:
        url = f"https://api.hh.ru/vacancies/{vacancy_id}"
        response = requests.get(url)

        return response

    @classmethod
    def _filter_vacancy(cls, vacancy: dict) -> dict:
        return {
            "id": vacancy["id"],
            "name": vacancy["name"],
            "employer_name": vacancy["employer"]["name"],
            "description": vacancy["description"],
            "alternate_url": vacancy["alternate_url"],
            "key_skills": vacancy["key_skills"],
        }

import json

import requests


def main():
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": "DevOps",
        "per_page": 2,
    }

    try:
        response = requests.get(url, params=params)
        print(json.dumps(response.json(), ensure_ascii=False, indent=4))

    except Exception as e:
        print(f"Something goes wrong: {e}")


if __name__ == "__main__":
    main()

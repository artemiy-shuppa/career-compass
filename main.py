import json

from collector.HeadHunterCollector import HeadHunterCollector


def main():
    try:
        collector = HeadHunterCollector()
        vacancies = collector.collect("DevOps")
        print(json.dumps(vacancies, ensure_ascii=False, indent=4))

    except Exception as e:
        print(f"Something goes wrong: {e}")


if __name__ == "__main__":
    main()

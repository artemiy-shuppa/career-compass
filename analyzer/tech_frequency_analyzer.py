import pandas as pd

from model.report_model import ReportItem, Table


class TechFrequencyAnalyzer:
    def analyze(self, vacancies: list[dict]) -> list[ReportItem]:
        if not vacancies:
            return []

        skills = [
            skill["name"].lower()
            for vac in vacancies
            for skill in vac.get("key_skills", [])
        ]

        skill_counts = pd.Series(skills).value_counts().nlargest(20)

        total_vacancies = len(vacancies)

        skill_percentages = (skill_counts / total_vacancies) * 100

        rows = [
            (i, skill, count, f"{percentage:.1f}%")
            for i, (skill, count, percentage) in enumerate(
                zip(skill_counts.index, skill_counts, skill_percentages, strict=False),
                1,
            )
        ]

        table = Table(headers=["Rank", "Tech", "Mention", "Share"], rows=rows)
        return [table]

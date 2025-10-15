import yaml
from pydantic import BaseModel


class SearchParameters(BaseModel):
    """Scheme for search parameters"""

    keywords: str
    max_vacancies: int


class AnalysisRules(BaseModel):
    """Scheme for analysis rules"""

    frequency_top_tech_limit: int


class ConfigSchema(BaseModel):
    """Main configuration scheme for the app"""

    search_parameters: SearchParameters
    analysis_rules: AnalysisRules

    @classmethod
    def from_yaml(cls, path: str) -> "ConfigSchema":
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls(**data)

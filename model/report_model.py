class ReportItem:
    pass


class Title(ReportItem):
    def __init__(self, text: str, level: int = 1):
        self.text = text
        self.level = level


class Paragraph(ReportItem):
    def __init__(self, text: str):
        self.text = text


class Table(ReportItem):
    def __init__(self, headers: list[str], rows: list[tuple]):
        self.headers = headers
        self.rows = rows


class ReportContent:
    def __init__(self, sections: list[ReportItem]):
        self.sections = sections

from model.report_model import Paragraph, ReportContent, Table, Title


class MarkdownFormatter:
    @staticmethod
    def format_report(report_content: ReportContent) -> str:
        lines = []

        for item in report_content.sections:
            if isinstance(item, Title):
                lines.append(MarkdownFormatter._format_title(item))
            elif isinstance(item, Paragraph):
                lines.append(MarkdownFormatter._format_paragraph(item))
            elif isinstance(item, Table):
                lines.append(MarkdownFormatter._format_table(item))

        return "\n".join(lines)

    @staticmethod
    def _format_title(title: Title) -> str:
        return f"{'#' * title.level} {title.text}"

    @staticmethod
    def _format_paragraph(paragraph: Paragraph) -> str:
        return paragraph.text

    @staticmethod
    def _format_table(table: Table) -> str:
        if not table.rows:
            return ""

        col_widths = [len(h) for h in table.headers]
        for row in table.rows:
            for i, cell in enumerate(row):
                if len(str(cell)) > col_widths[i]:
                    col_widths[i] = len(str(cell))

        header_line = " | ".join(
            header.ljust(col_widths[i]) for i, header in enumerate(table.headers)
        )

        separator_line = "-+-".join("-" * width for width in col_widths)

        row_lines = []
        for row in table.rows:
            line = " | ".join(
                str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)
            )
            row_lines.append(line)

        full_table = "\n".join([header_line, separator_line] + row_lines)
        return "```table\n" + full_table + "\n```"

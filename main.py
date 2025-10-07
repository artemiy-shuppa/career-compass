from datetime import datetime
from formatter.MarkdownFormatter import MarkdownFormatter

from dotenv import load_dotenv

from analyzer.TechFrequencyAnalyzer import TechFrequencyAnalyzer
from collector.HeadHunterCollector import HeadHunterCollector
from model.report_model import ReportContent, Title
from sender.telegram_sender import TelegramSender


def main():
    load_dotenv()

    try:
        collector = HeadHunterCollector()
        vacancies = collector.collect("DevOps")

        reports = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        reports.append(Title(f"Report for {timestamp}"))

        analyzer = TechFrequencyAnalyzer()
        reports.append(Title("TechFrequencyAnalyzer", level=2))
        reports.extend(analyzer.analyze(vacancies))

        formatter = MarkdownFormatter()
        final_result = formatter.format_report(ReportContent(reports))

        sender = TelegramSender()
        sender.send_message(final_result)

    except Exception as e:
        print(f"Something goes wrong: {e}")


if __name__ == "__main__":
    main()

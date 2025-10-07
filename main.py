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
        try:
            error_message = format_error_message(e)
            sender = TelegramSender()
            sender.send_message(error_message)

        except Exception as send_error:
            print("Critical Error: can't send notification to telegram")
            print(f"Initial Error: {e!r}")
            print(f"Error sending to telegram: {send_error!r}")


def format_error_message(e: Exception):
    error_type = type(e).__name__
    error_message = str(e)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    final_message = [
        "**Error in Career Compass pipeline**\n",
        f"**Time** `{timestamp}`",
        f"**Error type**: `{error_type}`",
        "**Message**:\n```",
        f"{error_message}```",
    ]
    return "\n".join(final_message)


if __name__ == "__main__":
    main()

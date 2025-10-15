from datetime import datetime

import structlog
from dotenv import load_dotenv

from analyzer.tech_frequency_analyzer import TechFrequencyAnalyzer
from collector.head_hunter_collector import HeadHunterCollector
from config_schema import ConfigSchema
from formatter.MarkdownFormatter import MarkdownFormatter
from model.report_model import ReportContent, Title
from sender.telegram_sender import TelegramSender


def main():
    logger = structlog.get_logger()

    load_dotenv()

    try:
        config = ConfigSchema.from_yaml("config.yml")
        logger.info("Config loaded", event_type="config_loaded")

        logger.info(
            "Pipeline execution initiated",
            event_type="pipeline_start",
        )

        collector = HeadHunterCollector()
        vacancies = collector.collect(config.search_parameters)
        logger.info(
            "Vacancies collected",
            event_type="data_collection_complete",
            source="hh.ru",
            vacancies_found=len(vacancies),
        )

        reports = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        reports.append(Title(f"Report for {timestamp}"))

        analyzer = TechFrequencyAnalyzer()
        reports.append(Title("TechFrequencyAnalyzer", level=2))
        reports.extend(analyzer.analyze(vacancies, config.analysis_rules))
        logger.info(
            "Vacancies analyzed",
            event_type="analysis_complete",
        )

        formatter = MarkdownFormatter()
        final_result = formatter.format_report(ReportContent(reports))

        sender = TelegramSender()
        sender.send_message(final_result)
        logger.info(
            "Report sent",
            event_type="report_sent_successfully",
        )

    except Exception as e:
        try:
            logger.error(
                "Pipeline got an error",
                event_type="pipeline_error",
                error_type=type(e).__name__,
                error_message=str(e),
            )
            error_message = format_error_message(e)
            sender = TelegramSender()
            sender.send_message(error_message)

        except Exception as send_error:
            logger.critical(
                "Critical Error: can't send notification to telegram",
                event_type="pipeline_error",
                initial_error=f"{e!r}",
                send_error=f"{send_error!r}",
            )


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

# Career Compass

Batch pipeline that collects job vacancies from hh.ru, analyzes the
frequency of required skills, and sends a Markdown report to Telegram.

## Architecture

Single-process Python script orchestrated by `main.py`. Stages run
sequentially in memory:

- `collector/head_hunter_collector.py` — fetches vacancies from
  `https://api.hh.ru/vacancies` (paginated list, then per-vacancy
  details) and keeps a subset of fields.
- `analyzer/tech_frequency_analyzer.py` — counts `key_skills`
  occurrences with pandas and builds a top-N table.
- `formatter/MarkdownFormatter.py` — renders domain objects from
  `model/report_model.py` (`Title`, `Paragraph`, `Table`) into Markdown.
- `sender/telegram_sender.py` — sends the report via the Telegram Bot
  API in `MarkdownV2`, escaping special characters outside fenced and
  inline code blocks.

Data is held in memory for the duration of a run; nothing is persisted
between runs.

## Configuration

- `config.yml` — search and analysis parameters, validated by the
  pydantic schema in `config_schema.py`. See `config.example.yml` for
  the structure.
- Environment variables (loaded via `python-dotenv`):
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_CHAT_ID`

## Running locally

```
pip install -r requirements.txt
cp config.example.yml config.yml
python main.py
```

## CI/CD

Two GitHub Actions workflows in `.github/workflows/`:

- `ci-lint` — runs `pre-commit` on every push and pull request.
- `Career Compass CI/CD` — runs `main.py` on a cron schedule (Mondays
  at 05:00 UTC) and on manual `workflow_dispatch`. Reads `config.yml`
  and Telegram credentials from repository secrets.

## Tooling

- Python 3.10.
- Dependencies pinned with `pip-tools`: `requirements.in` →
  `requirements.txt` (and the dev pair).
- `ruff` and `black` configured in `pyproject.toml`, enforced via
  `pre-commit`.
- Structured logging via `structlog`.

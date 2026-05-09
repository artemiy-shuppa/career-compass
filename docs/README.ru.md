# Career Compass

Batch-пайплайн, который собирает вакансии с hh.ru, анализирует частоту
упоминания навыков и отправляет Markdown-отчёт в Telegram.

## Архитектура

Однопроцессный Python-скрипт, оркеструемый `main.py`. Стадии
выполняются последовательно, данные передаются в памяти:

- `collector/head_hunter_collector.py` — забирает вакансии с
  `https://api.hh.ru/vacancies` (постраничный список и детальная
  карточка по каждой вакансии) и оставляет нужные поля.
- `analyzer/tech_frequency_analyzer.py` — считает частоту
  `key_skills` через pandas и формирует таблицу топ-N.
- `formatter/MarkdownFormatter.py` — рендерит доменные объекты из
  `model/report_model.py` (`Title`, `Paragraph`, `Table`) в Markdown.
- `sender/telegram_sender.py` — отправляет отчёт через Telegram Bot
  API в режиме `MarkdownV2`, экранируя спецсимволы вне блочного и
  строчного кода.

Данные живут в памяти в пределах одного запуска и нигде не
сохраняются.

## Конфигурация

- `config.yml` — параметры поиска и анализа, валидируется
  pydantic-схемой в `config_schema.py`. Структура — в
  `config.example.yml`.
- Переменные окружения (читаются через `python-dotenv`):
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_CHAT_ID`

## Локальный запуск

```
pip install -r requirements.txt
cp config.example.yml config.yml
python main.py
```

## CI/CD

Два workflow в `.github/workflows/`:

- `ci-lint` — запускает `pre-commit` на каждый push и pull request.
- `Career Compass CI/CD` — запускает `main.py` по расписанию cron
  (понедельник, 05:00 UTC) и по ручному `workflow_dispatch`. Берёт
  `config.yml` и токены Telegram из repository secrets.

## Инструментарий

- Python 3.10.
- Зависимости пинятся через `pip-tools`: `requirements.in` →
  `requirements.txt` (и аналогичная пара для dev).
- `ruff` и `black` настроены в `pyproject.toml`, прогоняются через
  `pre-commit`.
- Структурное логирование через `structlog`.

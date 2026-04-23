# 🎭 Plane.so E2E Automation Showcase

> Python + Playwright + Allure Report — автоматизация E2E тестирования open-source SaaS
> [Plane.so](https://app.plane.so) (Jira/Linear alternative).

![CI](https://img.shields.io/badge/CI-pending-lightgrey)
![Tests](https://img.shields.io/badge/tests-0%2F25-lightgrey)
![Python](https://img.shields.io/badge/python-3.11-blue)

📊 **Live Allure Report:** _будет после первого прогона CI_

## Stack

- **Python 3.11** + **Playwright** + **pytest**
- **Allure Report** — интерактивный дашборд с трендами
- **Page Object Model** — все селекторы и действия инкапсулированы в классах
- **GitHub Actions** — CI на push/PR + daily schedule, деплой отчёта на GitHub Pages
- **Custom logger** — человекочитаемые логи STEP / ASSERT / ERROR с таймстампами

## Quick Start

```bash
git clone <this-repo>
cd <this-repo>

python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
playwright install --with-deps chromium

cp .env.example .env
# Заполни .env реальными credentials тестового аккаунта Plane

pytest                           # все тесты
pytest -m smoke                  # только smoke
pytest --browser=firefox         # другой браузер
allure serve allure-results      # смотрим отчёт локально
```

## Structure

(детали — в этапах дальше)

## License

MIT
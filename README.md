# 🎭 Plane.so E2E Automation Showcase



![CI](https://github.com/zahar-pr/boldo_qa_task/actions/workflows/tests.yml/badge.svg)
![Allure](https://img.shields.io/badge/Allure-Report-blue?logo=qmeta)
![Python](https://img.shields.io/badge/python-3.10-blue?logo=python)
![Playwright](https://img.shields.io/badge/Playwright-1.49-2EAD33?logo=playwright)
![Tests](https://img.shields.io/badge/tests-30%20passed-success)

**📊 Live Allure Report:** https://zahar-pr.github.io/boldo_qa_task/




pkill -f "/opt/google/chrome" 2>/dev/null
sudo swapoff -a && sudo swapon -a
rm -f auth/storage_state.json
python scripts/save_auth_state.py
pytest -v



rm -f auth/storage_state.json
python scripts/save_auth_state.py
pkill -f "/opt/google/chrome" 2>/dev/null
sudo swapoff -a && sudo swapon -a
free -h
pytest tests/project/ -v


HEADLESS=false pytest tests/project/test_project.py::TestProject::test_tc009_create_project_with_full_data -v


pytest tests/workspace/ -v
pytest -v


pkill -f "/opt/google/chrome" 2>/dev/null
sudo swapoff -a && sudo swapon -a
free -h
pytest tests/project/test_project.py::TestProject::test_tc009_create_project_with_full_data -v




pkill -f "/opt/google/chrome" 2>/dev/null
sudo swapoff -a && sudo swapon -a
free -h
rm -f auth/storage_state.json
python scripts/save_auth_state.py
# Этап 5.3
pytest tests/project/ -v
# Этап 5.4
pytest tests/issues/ -v
# Этап 5.5
pytest tests/views/ -v
# Этап 5.6
pytest tests/cycles/ -v
# Этап 5.7
pytest tests/pages/ -v
# Smoke suite
pytest -m "smoke and not serial" -v
# Полный прогон
pytest -v






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
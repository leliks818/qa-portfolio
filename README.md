# QA Automation Portfolio

Pytest-based QA automation portfolio: Selenium UI + Playwright API, with HTML and Allure reports.

![CI](https://github.com/leliks818/qa-portfolio/actions/workflows/ci.yml/badge.svg)

CI: GitHub Actions workflow in `.github/workflows/ci.yml` (uploads `reports/` as an artifact).

## Current Metrics

- Tests: 6 total (5 passing + 1 xfail example kept intentionally)
- Reports: [HTML report](reports/report.html), [Allure results](reports/allure-results)

Add screenshots to `docs/` for README visuals:
- `docs/report-html.png` (pytest-html table)
- `docs/allure-dashboard.png` (Allure dashboard)

## Reports

Run locally and generate proof artifacts:

```bash
pytest tests/ -v --html=reports/report.html --self-contained-html --alluredir=reports/allure-results
```

Allure dashboard options:

1) GitHub Pages (recommended): after push to `main`, workflow `.github/workflows/pages.yml` publishes a live dashboard.
Expected URL: `https://leliks818.github.io/qa-portfolio/`

2) Locally, if you have Allure CLI installed:

```bash
allure serve reports/allure-results
```

Screenshots (add these files to `docs/`):

![pytest-html report](docs/report-html.png)

![Allure dashboard](docs/allure-dashboard.png)

## Quick Run (Poetry)

```bash
poetry install --with dev
poetry run pytest -v --html=reports/report.html --self-contained-html --alluredir=reports/allure-results
```

## Quick Run (pip, no Poetry)

If you are using a plain interpreter in PyCharm (no Poetry env), install the needed plugins once:

```bash
python -m pip install selenium playwright pytest-playwright pytest-html allure-pytest requests
python -m pytest tests/ -v --html=reports/report.html --self-contained-html --alluredir=reports/allure-results
```

## Notes

- Selenium UI uses `https://the-internet.herokuapp.com` by default (override with `BASE_URL`).
- `HEADLESS=0` disables headless browser mode for Selenium tests.

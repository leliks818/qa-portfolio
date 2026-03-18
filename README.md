# QA Automation Portfolio

Automation QA portfolio project built on `pytest` with:
- Selenium UI test(s) against `the-internet.herokuapp.com`
- Playwright API test(s) (request context)
- Reports: `pytest-html` + Allure
- CI: GitHub Actions + published reports via GitHub Pages

![CI](https://github.com/leliks818/qa-portfolio/actions/workflows/ci.yml/badge.svg)

## Live Reports (GitHub Pages)

After each push to `main` (and also on schedule), GitHub Actions publishes the latest reports:

- Allure dashboard: `https://leliks818.github.io/qa-portfolio/allure/`
- pytest-html report: `https://leliks818.github.io/qa-portfolio/report.html`

If Pages is not enabled yet: `Settings` → `Pages` → `Source: GitHub Actions`.

## Current Metrics

- Tests: 36 total (35 passing + 1 xfail example kept intentionally)
- Proof artifacts in repo: [reports/report.html](reports/report.html), [reports/allure-results](reports/allure-results)

## What’s Covered

- UI (Selenium): 30+ browser tests on a demo app (configurable base URL)
- API (Playwright): REST smoke validation via Playwright request context
- Pytest regression patterns: parametrization, markers, and an `xfail` example

## Quick Start

Generate both HTML report and Allure results:

```bash
pytest tests/ -v --html=reports/report.html --self-contained-html --alluredir=reports/allure-results
```

If you have Allure CLI installed locally:

```bash
allure serve reports/allure-results
```

Windows helper (optional):

```powershell
.\scripts\reports.ps1
```

## Setup Options

### Option A: Poetry (recommended for CI parity)

```bash
poetry install --with dev
poetry run pytest -v --html=reports/report.html --self-contained-html --alluredir=reports/allure-results
```

### Option B: pip (PyCharm plain interpreter)

```bash
python -m pip install selenium playwright pytest-playwright pytest-html allure-pytest requests
python -m pytest tests/ -v --html=reports/report.html --self-contained-html --alluredir=reports/allure-results
```

## Configuration

- `BASE_URL` (default: `https://the-internet.herokuapp.com`)
- `HEADLESS=0` disables headless mode for Selenium tests

## CI/CD

- CI workflow: `.github/workflows/ci.yml` (runs tests, generates reports, uploads `reports/` as an artifact)
- Pages workflow: `.github/workflows/pages.yml` (builds a static site with Allure + pytest-html and deploys to Pages)

## Screenshots (for README visuals)

Add your own screenshots here (not generated automatically):
- `docs/report-html.png` (pytest-html table)
- `docs/allure-dashboard.png` (Allure dashboard overview)

![pytest-html report](docs/report-html.png)
![Allure dashboard](docs/allure-dashboard.png)

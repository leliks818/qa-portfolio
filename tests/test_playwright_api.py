import pytest


@pytest.mark.api
def test_playwright_api_httpbin_get(playwright):
    # API test without extra deps: use Playwright request context.
    api = playwright.request.new_context(base_url="https://httpbin.org")
    try:
        resp = api.get("/get")
        assert resp.ok
        body = resp.json()
        assert body["url"].endswith("/get")
    finally:
        api.dispose()


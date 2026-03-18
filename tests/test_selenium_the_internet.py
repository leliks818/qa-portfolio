import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from pages.the_internet.add_remove_elements_page import AddRemoveElementsPage
from pages.the_internet.checkboxes_page import CheckboxesPage
from pages.the_internet.context_menu_page import ContextMenuPage
from pages.the_internet.dropdown_page import DropdownPage
from pages.the_internet.dynamic_controls_page import DynamicControlsPage
from pages.the_internet.dynamic_loading_page import DynamicLoadingExamplePage, DynamicLoadingPage
from pages.the_internet.file_upload_page import FileUploadPage
from pages.the_internet.frames_page import IFramePage, NestedFramesPage
from pages.the_internet.horizontal_slider_page import HorizontalSliderPage
from pages.the_internet.hovers_page import HoversPage
from pages.the_internet.js_alerts_page import JSAlertsPage
from pages.the_internet.key_presses_page import KeyPressesPage
from pages.the_internet.login_page import LoginPage
from pages.the_internet.inputs_page import InputsPage
from pages.the_internet.status_codes_page import StatusCodesPage
from pages.the_internet.windows_page import WindowsPage


pytestmark = pytest.mark.ui


def test_login_invalid_shows_error(driver, base_url):
    page = LoginPage(driver=driver, base_url=base_url)
    page.open()
    page.login("tomsmith", "bad-password")
    assert "Your password is invalid!" in page.flash_text()


def test_checkboxes_can_toggle_both(driver, base_url):
    page = CheckboxesPage(driver=driver, base_url=base_url)
    page.open()

    page.set_checked(0, True)
    assert page.is_checked(0) is True

    page.set_checked(1, False)
    assert page.is_checked(1) is False


@pytest.mark.parametrize("option", ["Option 1", "Option 2"])
def test_dropdown_selects_option(driver, base_url, option):
    page = DropdownPage(driver=driver, base_url=base_url)
    page.open()
    page.select_by_visible_text(option)
    assert page.selected_text() == option


def test_js_alert_accept(driver, base_url):
    page = JSAlertsPage(driver=driver, base_url=base_url)
    page.open()
    page.click_alert()
    driver.switch_to.alert.accept()
    assert "You successfully clicked an alert" in page.result_text()


def test_js_confirm_dismiss(driver, base_url):
    page = JSAlertsPage(driver=driver, base_url=base_url)
    page.open()
    page.click_confirm()
    driver.switch_to.alert.dismiss()
    assert "You clicked: Cancel" in page.result_text()


def test_js_prompt_send_text(driver, base_url):
    page = JSAlertsPage(driver=driver, base_url=base_url)
    page.open()
    page.click_prompt()
    alert = driver.switch_to.alert
    alert.send_keys("hello")
    alert.accept()
    assert "You entered: hello" in page.result_text()


@pytest.mark.parametrize("example_num", [1, 2])
def test_dynamic_loading_examples_show_hello_world(driver, base_url, example_num):
    hub = DynamicLoadingPage(driver=driver, base_url=base_url)
    hub.open()
    hub.open_example(example_num)

    page = DynamicLoadingExamplePage(driver=driver, base_url=base_url)
    page.start()
    assert page.wait_finished_text() == "Hello World!"


def test_dynamic_controls_remove_and_add_checkbox(driver, base_url):
    page = DynamicControlsPage(driver=driver, base_url=base_url)
    page.open()

    assert page.checkbox_present() is True
    page.remove_checkbox()
    assert page.checkbox_present() is False
    assert "It's gone!" in page.message_text()
    assert "Add" in page.checkbox_button_text()

    page.add_checkbox()
    assert "It's back!" in page.message_text()
    assert "Remove" in page.checkbox_button_text()


def test_dynamic_controls_enable_and_disable_input(driver, base_url):
    page = DynamicControlsPage(driver=driver, base_url=base_url)
    page.open()

    assert page.input_enabled() is False
    page.enable_input()
    assert page.input_enabled() is True
    assert "It's enabled!" in page.message_text()

    page.disable_input()
    assert page.input_enabled() is False
    assert "It's disabled!" in page.message_text()


def test_add_remove_elements_adds_and_deletes_buttons(driver, base_url):
    page = AddRemoveElementsPage(driver=driver, base_url=base_url)
    page.open()

    page.add_element()
    page.add_element()
    assert page.delete_buttons_count() == 2

    page.delete_one()
    assert page.delete_buttons_count() == 1


def test_context_menu_triggers_alert(driver, base_url):
    page = ContextMenuPage(driver=driver, base_url=base_url)
    page.open()

    ActionChains(driver).context_click(page.hotspot()).perform()
    alert = driver.switch_to.alert
    assert "You selected a context menu" in alert.text
    alert.accept()


def test_multiple_windows_opens_new_window(driver, base_url):
    page = WindowsPage(driver=driver, base_url=base_url)
    page.open()
    original = driver.current_window_handle

    page.click_open_new_window()

    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 2)
    handles = driver.window_handles
    new_handle = next(h for h in handles if h != original)
    driver.switch_to.window(new_handle)
    try:
        assert page.header_text() == "New Window"
    finally:
        driver.close()
        driver.switch_to.window(original)


def test_file_upload(driver, base_url, tmp_path):
    file_path = tmp_path / "upload.txt"
    file_path.write_text("hello", encoding="utf-8")

    page = FileUploadPage(driver=driver, base_url=base_url)
    page.open()
    page.upload(str(file_path))
    assert page.uploaded_filename() == "upload.txt"


def test_iframe_can_type_text(driver, base_url):
    page = IFramePage(driver=driver, base_url=base_url)
    page.open()
    page.type_in_editor("Hello from iframe")
    assert "Hello from iframe" in page.editor_text()


def test_nested_frames_middle_has_content(driver, base_url):
    page = NestedFramesPage(driver=driver, base_url=base_url)
    page.open()

    driver.switch_to.frame("frame-top")
    try:
        driver.switch_to.frame("frame-middle")
        try:
            assert "MIDDLE" in driver.page_source
        finally:
            driver.switch_to.parent_frame()
    finally:
        driver.switch_to.default_content()


def test_horizontal_slider_can_move(driver, base_url):
    page = HorizontalSliderPage(driver=driver, base_url=base_url)
    page.open()

    # Slider starts at 0. Moving right should change the value.
    page.move_right(steps=4)
    assert float(page.value_text()) > 0.0


@pytest.mark.parametrize(
    "key,expected",
    [
        (Keys.TAB, "TAB"),
        ("A", "A"),
    ],
)
def test_key_presses_reports_key(driver, base_url, key, expected):
    page = KeyPressesPage(driver=driver, base_url=base_url)
    page.open()
    page.press(key)
    assert expected in page.wait_result_contains(expected)


@pytest.mark.parametrize("index", [1, 2, 3])
def test_hovers_show_caption(driver, base_url, index):
    page = HoversPage(driver=driver, base_url=base_url)
    page.open()
    page.hover_figure(index)
    text = page.caption_text(index)
    assert f"name: user{index}" in text.lower()


@pytest.mark.parametrize("value", ["123", "-10", "0"])
def test_inputs_accept_value(driver, base_url, value):
    page = InputsPage(driver=driver, base_url=base_url)
    page.open()
    page.set_value(value)
    assert page.value() == value


@pytest.mark.parametrize("code", [200, 301, 404, 500])
def test_status_codes_pages_have_message(driver, base_url, code):
    page = StatusCodesPage(driver=driver, base_url=base_url)
    page.open()
    page.open_code(code)
    text = page.content_text()
    assert str(code) in text

# conftest.py
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
import os

@pytest.fixture
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "emulator-5554"
    options.udid = "emulator-5554"
    options.automation_name = "UiAutomator2"
    options.app = "C:\\Users\\mehme\\Downloads\\ApiDemos-debug.apk"

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    yield driver
    driver.quit()



@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Get the result from pytest
    outcome = yield
    result = outcome.get_result()

    # Run this only on failures
    if result.when == "call" and result.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            filename = f"{item.name}.png"
            filepath = os.path.join(screenshot_dir, filename)
            driver.save_screenshot(filepath)
            print(f"📸 Screenshot saved: {filepath}")

# pytest --html=reports/report.html --self-contained-html -v    To create html report
# pytest tests/test_appium.py::test_alert_dialog                To run a specific function(e.g test_alert_dialog) in test_appium.py:
# pytest tests/test_appium.py                                   To run test_appium.py file into the tests folder
# python -m pytest tests/test_appium.py                         To run pytest as a module (-m → "module").If you get an error like "command not found", use this command.It is safer especially when using virtual environment (venv)
# pytest -k "drag_and_drop"                                     E.G This will only run tests whose name contains "drag_and_drop".
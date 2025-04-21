# test_appium.py
from appium.webdriver.common.appiumby import AppiumBy
import pytest
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Purpose: Select different values from a dropdown (Spinner)
# Parametrized: Runs for "Earth", "Mars", "Venus"
# Verifies: That the correct item is selected
@pytest.mark.parametrize("planet", ["Earth", "Mars", "Venus"])
def test_spinner_dynamic(driver, planet):
    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().description("Views"))'
    ).click()

    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Controls").click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "2. Dark Theme").click()

    spinner = driver.find_element(AppiumBy.ID, "io.appium.android.apis:id/spinner1")
    spinner.click()

    option = driver.find_element(AppiumBy.XPATH, f'//android.widget.CheckedTextView[@text="{planet}"]')
    option.click()

    selected = driver.find_element(AppiumBy.ID, "android:id/text1")
    assert selected.text == planet

# Purpose: Verifies that the "Animation" menu item is visible and clickable
# @pytest.mark.skip(reason="Skipping temporarily")
def test_open_animation(driver):
    views = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Animation")
    assert views.is_displayed()
    views.click()

# Purpose: Scrolls to "Views" and taps it
# Acts as a base test for navigating into the views section
def test_open_views(driver):
    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().description("Views"))'
    ).click()

# Navigates to Views → WebView
# Switches context from native to WebView
# Interacts with HTML content, clicking a link with ID "i am a link"
# Switches back to native (optional)
def test_webview_interaction(driver):
    wait = WebDriverWait(driver, 10)

    # Scroll to "Views" and tap
    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true))'
        '.scrollIntoView(new UiSelector().description("Views"))'
    ).click()

    # Scroll to "WebView" and tap
    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true))'
        '.scrollIntoView(new UiSelector().description("WebView"))'
    ).click()

    # Retrieve all available contexts (NATIVE_APP, WEBVIEW_...)
    contexts = driver.contexts
    print("Available contexts:", contexts)

    # Switch to the WebView context
    switched = False
    for context in contexts:
        if "WEBVIEW" in context:
            driver.switch_to.context(context)
            print("Switched to WebView context:", context)
            switched = True
            break

    assert switched, "Could not switch to WEBVIEW context"

    # Interact with the link inside the WebView
    try:
        link = driver.find_element(AppiumBy.XPATH, "//a[@id='i am a link']")
        link.click()
        print("✅ 'i am a link' was successfully clicked.")
    except Exception as e:
        pytest.fail(f"❌ WebView link could not be clicked: {str(e)}")

    # Optional: switch back to native context
    driver.switch_to.context("NATIVE_APP")

# Navigates to Views → Controls → 2. Dark Theme
# Fills in a text field
# Asserts the input was successful
def test_textbox_input(driver):

    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().description("Views"))'
    ).click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Controls").click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "2. Dark Theme").click()

    textbox = driver.find_element(AppiumBy.ID, "io.appium.android.apis:id/edit")
    textbox.send_keys("Test textbox!")
    assert textbox.text == "Test textbox!"

# Navigates to Views → Controls → 2. Dark Theme
# Enters text
# Toggles checkbox
# Selects radio button
# Verifies each of them was correctly updated
def test_controls_interaction(driver):
    wait = WebDriverWait(driver, 10)

    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().description("Views"))'
    ).click()

    wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Controls"))).click()
    wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "2. Dark Theme"))).click()

    textbox = wait.until(EC.presence_of_element_located((AppiumBy.ID, "io.appium.android.apis:id/edit")))
    textbox.send_keys("Hello Appium")
    assert textbox.text == "Hello Appium"

    # mark checkbox
    checkbox = driver.find_element(AppiumBy.ID, "io.appium.android.apis:id/check1")
    checkbox.click()
    assert checkbox.get_attribute("checked") == "true"

    # select RadioButton
    radio = driver.find_element(AppiumBy.ID, "io.appium.android.apis:id/radio1")
    radio.click()
    assert radio.get_attribute("checked") == "true"

# Navigates to Views → Controls → 2. Dark Theme
# Opens the dropdown (Spinner)
# Selects "Earth"
# Asserts the selection
def test_spinner_selection(driver):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    wait = WebDriverWait(driver, 10)

    # "Views" → "Controls" → "2. Dark Theme"
    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().description("Views"))'
    ).click()

    wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Controls"))).click()
    wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "2. Dark Theme"))).click()

    # Open Spinner'ı
    spinner = wait.until(EC.presence_of_element_located((AppiumBy.ID, "io.appium.android.apis:id/spinner1")))
    spinner.click()

    # Select "Earth" from the options
    driver.find_element(AppiumBy.XPATH, '//android.widget.CheckedTextView[@text="Earth"]').click()

    # Verification
    selected = driver.find_element(AppiumBy.ID, "android:id/text1")
    assert selected.text == "Earth"

# Uses PointerInput and ActionBuilder to simulate drag-and-drop
# Asserts that the action was successful by checking the result text
def test_drag_and_drop(driver):
    wait = WebDriverWait(driver, 10)

    # Scroll to "Views"
    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().description("Views"))'
    ).click()

    wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Drag and Drop"))).click()

    # Source and destination elements
    src = wait.until(EC.presence_of_element_located((AppiumBy.ID, "io.appium.android.apis:id/drag_dot_1")))
    dst = wait.until(EC.presence_of_element_located((AppiumBy.ID, "io.appium.android.apis:id/drag_dot_2")))

    # Prepare pointer input for gesture
    finger = PointerInput("touch", "finger")
    actions = ActionBuilder(driver, mouse=finger)

    # Get coordinates
    src_loc = src.location
    dst_loc = dst.location

    actions.pointer_action.move_to_location(src_loc['x'], src_loc['y'])
    actions.pointer_action.pointer_down()
    actions.pointer_action.pause(0.5)
    actions.pointer_action.move_to_location(dst_loc['x'], dst_loc['y'])
    actions.pointer_action.release()
    actions.perform()

    # Verify result
    result = driver.find_element(AppiumBy.ID, "io.appium.android.apis:id/drag_result_text")
    assert "Dropped" in result.text


# Navigates to a toggle (switch) control
# Captures its initial state (checked or not)
# Toggles the switch
# Verifies that the state has changed
def test_switch_toggle(driver):
    wait = WebDriverWait(driver, 10)

    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().description("Views"))'
    ).click()

    wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Controls"))).click()
    wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "2. Dark Theme"))).click()

    switch = wait.until(EC.presence_of_element_located((AppiumBy.ID, "io.appium.android.apis:id/toggle1")))

    # Initial state
    initial_state = switch.get_attribute("checked")
    print(f"Initital state: {initial_state}")

    # click to Switch (toggle)
    switch.click()

    # Check new state
    new_state = switch.get_attribute("checked")
    print(f"New state: {new_state}")

    # It is expected to be different (on <-> off)
    assert initial_state != new_state

# Opens the alert dialog in App → Alert Dialogs → OK Cancel
# Asserts that the alert is shown with the expected title
# Clicks "OK" to close the dialog
def test_alert_dialog(driver):
    wait = WebDriverWait(driver, 10)

    # Scroll to "App" and tap
    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true))'
        '.scrollIntoView(new UiSelector().description("App"))'
    ).click()

    # Tap "Alert Dialogs"
    wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Alert Dialogs"))).click()

    # Tap on the button that triggers the OK/Cancel alert
    wait.until(EC.presence_of_element_located(
        (AppiumBy.ACCESSIBILITY_ID, "OK Cancel dialog with a message"))).click()

    # Wait for the alert to appear
    alert_title = wait.until(EC.presence_of_element_located(
        (AppiumBy.ID, "android:id/alertTitle")))
    
    assert alert_title.text == "Lorem ipsum dolor sit aie consectetur adipiscing\nPlloaso mako nuto siwuf cakso dodtos anr koop."

    # Tap the "OK" button
    ok_button = driver.find_element(AppiumBy.ID, "android:id/button1")
    ok_button.click()

    print("✅ Alert dialog was displayed and 'OK' button was clicked.")

# Navigates to Views → Date Widgets → 1. Dialog
# Opens the date picker
# Selects a day (e.g., 10)
# Clicks "OK" to confirm
# Confirms the interaction is successful
def test_date_picker_dialog(driver):
    wait = WebDriverWait(driver, 10)

    # Scroll to "Views"
    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true))'
        '.scrollIntoView(new UiSelector().description("Views"))'
    ).click()

    # Tap on "Date Widgets"
    wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Date Widgets"))).click()

    # Tap on "1. Dialog"
    wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "1. Dialog"))).click()

    # Tap the button to open the date picker
    wait.until(EC.presence_of_element_located(
        (AppiumBy.ID, "io.appium.android.apis:id/pickDate"))).click()

    # Select a new date (e.g., 10th of the month)
    day = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, '//android.view.View[@text="10"]')))
    day.click()


    # Confirm with OK
    ok_button = driver.find_element(AppiumBy.ID, "android:id/button1")
    ok_button.click()

    print("✅ Date was selected and confirmed.")


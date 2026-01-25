# Повторно используемые шаги UI

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from tests.settings import BASE_URL
from tests.locators import (
    MainPageLocators,
    RegistrationPageLocators,
    LoginPageLocators,
    ProfileLocators,
)

# Ожидание загрузки главной страницы
def wait_main_ready(driver, timeout: int = 10) -> None:
    wait = WebDriverWait(driver, timeout)
    wait.until(
        EC.any_of(
            EC.visibility_of_element_located(MainPageLocators.ORDER_BUTTON),
            EC.element_to_be_clickable(MainPageLocators.LOGIN_ACCOUNT_BUTTON),
        )
    )

# Регистрация пользователя через UI
def register_user_via_ui(driver, email: str, password: str, timeout: int = 10) -> None:
    wait = WebDriverWait(driver, timeout)
    driver.get(f"{BASE_URL}/register")
    wait.until(EC.visibility_of_element_located(RegistrationPageLocators.NAME_INPUT)).send_keys("David Garguiya")
    wait.until(EC.visibility_of_element_located(RegistrationPageLocators.EMAIL_INPUT)).send_keys(email)
    wait.until(EC.visibility_of_element_located(RegistrationPageLocators.PASSWORD_INPUT)).send_keys(password)
    wait.until(EC.element_to_be_clickable(RegistrationPageLocators.SUBMIT_BUTTON)).click()
    wait.until(EC.visibility_of_element_located(LoginPageLocators.FORM_TITLE))



# Авторизация через форму входа
def login_via_form(driver, email: str, password: str, timeout: int = 10) -> None:
    wait = WebDriverWait(driver, timeout)
    wait.until(EC.visibility_of_element_located(LoginPageLocators.EMAIL_INPUT)).send_keys(email)
    wait.until(EC.visibility_of_element_located(LoginPageLocators.PASSWORD_INPUT)).send_keys(password)
    wait.until(EC.element_to_be_clickable(LoginPageLocators.SUBMIT_BUTTON)).click()
    wait.until(EC.visibility_of_element_located(MainPageLocators.ORDER_BUTTON))

# Регистрация, логин пользователя и открытие профиля
def login_and_open_profile(driver, email: str, password: str, timeout: int = 10) -> None:
    register_user_via_ui(driver, email, password, timeout=timeout)
    login_via_form(driver, email, password, timeout=timeout)
    driver.get(BASE_URL)
    wait_main_ready(driver, timeout=timeout)
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(MainPageLocators.PERSONAL_ACCOUNT_LINK)).click()
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(ProfileLocators.ACCOUNT_CONTAINER))

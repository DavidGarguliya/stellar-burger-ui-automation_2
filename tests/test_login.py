import pytest  # pytest для запуска тестов
from selenium.webdriver.support import expected_conditions as EC  # условия ожидания selenium (сокращённо ec)
from selenium.webdriver.support.wait import WebDriverWait  # явные ожидания selenium

from tests.settings import BASE_URL  # базовый адрес сервиса
from tests.utils.data_generators import build_email, build_password  # генераторы тестовых данных
from tests.utils.ui_flows import (  # общие шаги UI
    wait_main_ready,
    register_user_via_ui,
    login_via_form,
)
from tests.locators import (  # импортируем используемые локаторы
    MainPageLocators,
    RegistrationPageLocators,
    ForgotPasswordLocators,
) 

# Класс с проверками разных точек входа
class TestLogin:  

    # Вход по кнопке «Войти в аккаунт» на главной
    def test_login_from_main_button(self, driver):
        email = build_email()  # генерируем email
        password = build_password()  # генерируем пароль
        register_user_via_ui(driver, email, password)  # регистрируем пользователя через ui

        driver.get(BASE_URL)  # открываем главную страницу
        wait_main_ready(driver)  # ждём, пока главная станет доступной
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(MainPageLocators.LOGIN_ACCOUNT_BUTTON)).click()  # жмём «войти в аккаунт»
        login_via_form(driver, email, password)  # авторизуемся в открывшейся форме
        order_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(MainPageLocators.ORDER_BUTTON))  # ждём кнопку «оформить заказ»
        assert order_btn.is_displayed()  # проверяем, что кнопка видима
        assert driver.current_url.startswith(BASE_URL)  # убеждаемся, что остались на основном домене

    # Вход через «Личный кабинет» в шапке
    def test_login_from_header_personal_account(self, driver):
        email = build_email()  # генерируем email
        password = build_password()  # генерируем пароль
        register_user_via_ui(driver, email, password)  # регистрируем пользователя через ui

        driver.get(BASE_URL)  # открываем главную
        wait_main_ready(driver)  # ждём, пока элементы главной будут доступны
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(MainPageLocators.PERSONAL_ACCOUNT_LINK)).click()  # жмём «личный кабинет»
        login_via_form(driver, email, password)  # заполняем форму входа
        order_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(MainPageLocators.ORDER_BUTTON))  # ожидаем кнопку заказа
        assert order_btn.is_displayed()  # проверяем, что после входа она видима
        assert driver.current_url.startswith(BASE_URL)  # подтверждаем адрес основной страницы
    
    # Вход через ссылку на форме регистрации
    def test_login_from_registration_form_link(self, driver):
        email = build_email()  # генерируем email
        password = build_password()  # генерируем пароль
        register_user_via_ui(driver, email, password)  # регистрируем пользователя

        driver.get(f"{BASE_URL}/register")  # открываем страницу регистрации
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(RegistrationPageLocators.LOGIN_LINK)).click()  # жмём ссылку «войти»
        login_via_form(driver, email, password)  # авторизуемся
        order_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(MainPageLocators.ORDER_BUTTON))  # ждём кнопку заказа
        assert order_btn.is_displayed()  # проверяем, что кнопка отображается
        assert driver.current_url.startswith(BASE_URL)  # убеждаемся, что после входа на основном домене
    
    # Вход через ссылку на форме восстановления
    def test_login_from_forgot_password_form(self, driver):
        email = build_email()  # генерируем email
        password = build_password()  # генерируем пароль
        register_user_via_ui(driver, email, password)  # регистрируем пользователя

        driver.get(f"{BASE_URL}/forgot-password")  # открываем страницу восстановления пароля
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(ForgotPasswordLocators.LOGIN_LINK)).click()  # жмём ссылку «войти»
        login_via_form(driver, email, password)  # авторизуемся
        order_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(MainPageLocators.ORDER_BUTTON))  # ожидаем кнопку заказа
        assert order_btn.is_displayed()  # проверяем, что кнопка видима
        assert driver.current_url.startswith(BASE_URL)  # подтверждаем адрес основной страницы после входа

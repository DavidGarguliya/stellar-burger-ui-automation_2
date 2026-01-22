import pytest  # pytest для маркировки тестов
from selenium.webdriver.support import expected_conditions as EC  # условия ожидания selenium (сокращённо ec)
from selenium.webdriver.support.wait import WebDriverWait  # явные ожидания selenium

from tests.settings import BASE_URL  # базовый адрес сервиса
from tests.utils.data_generators import build_email, build_password  # генераторы тестовых данных
from tests.utils.ui_flows import (  # общие шаги UI
    wait_main_ready,
    register_user_via_ui,
    login_via_form,
    login_and_open_profile,
)
from tests.locators import (  # импортируем нужные локаторы
    MainPageLocators,
    LoginPageLocators,
    ProfileLocators,
)

# Класс с проверками переходов и выхода
class TestNavigation:
    
    # Переход в личный кабинет по клику на «Личный кабинет» после успешного входа
    def test_open_personal_account(self, driver):
        email = build_email()  # генерируем email
        password = build_password()  # генерируем пароль
        register_user_via_ui(driver, email, password)  # регистрируем пользователя
        login_via_form(driver, email, password)  # авторизуемся
        driver.get(BASE_URL)  # обновляем главную страницу после логина
        wait_main_ready(driver)  # ждём, пока она станет доступной
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(MainPageLocators.PERSONAL_ACCOUNT_LINK)).click()  # жмём "личный кабинет"
        profile_block = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(ProfileLocators.ACCOUNT_CONTAINER))  # проверяем, что открылась страница профиля
        assert profile_block.is_displayed()  # блок профиля видим
        assert "/account/profile" in driver.current_url  # в url есть путь профиля

    # Возврат в конструктор из личного кабинета по пункту «Конструктор»
    def test_return_to_constructor_from_profile_via_link(self, driver):
        email = build_email()  # генерируем email
        password = build_password()  # генерируем пароль
        login_and_open_profile(driver, email, password)  # регистрируем, логинимся и открываем профиль

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(MainPageLocators.CONSTRUCTOR_HEADER_LINK)).click()  # жмём "конструктор"
        order_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(MainPageLocators.ORDER_BUTTON))  # проверяем, что вернулись в конструктор
        assert order_btn.is_displayed()  # кнопка заказа доступна
        assert driver.current_url.startswith(BASE_URL)  # подтверждаем возврат на главную

    # Возврат в конструктор из личного кабинета по клику на логотип
    def test_return_to_constructor_from_profile_via_logo(self, driver):
        email = build_email()  # генерируем email
        password = build_password()  # генерируем пароль
        login_and_open_profile(driver, email, password)  # регистрируем, логинимся и открываем профиль

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(MainPageLocators.LOGO_LINK)).click()  # кликаем по логотипу
        order_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(MainPageLocators.ORDER_BUTTON))  # проверяем, что оказались в конструкторе
        assert order_btn.is_displayed()  # кнопка заказа доступна
        assert driver.current_url.startswith(BASE_URL)  # подтверждаем возврат на главную

    # Выход из аккаунта по кнопке «Выйти» в профиле
    def test_logout_from_profile(self, driver):  
        email = build_email()  # генерируем email
        password = build_password()  # генерируем пароль
        login_and_open_profile(driver, email, password)  # регистрируем, логинимся и открываем профиль

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(ProfileLocators.LOGOUT_BUTTON)).click()  # жмём «выход»
        login_title = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(LoginPageLocators.FORM_TITLE))  # ждём форму входа
        assert login_title.text == "Вход"  # проверяем, что отрисовалась форма входа

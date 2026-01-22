import random  # используем для генерации случайных чисел
import string  # нужен для набора символов в email и паролях

import pytest  # pytest для запуска тестов
from selenium.webdriver.support import expected_conditions as EC  # условия ожидания selenium (сокращённо ec)
from selenium.webdriver.support.wait import WebDriverWait  # явные ожидания selenium

from tests.locators import (  # импортируем используемые локаторы
    MainPageLocators,
    LoginPageLocators,
    RegistrationPageLocators,
    ForgotPasswordLocators,
) 

# Класс с проверками разных точек входа
class TestLogin:  
    def _wait_main_ready(self, driver):  # ждём загрузку главной страницы
        wait = WebDriverWait(driver, 10)  # создаём явное ожидание
        wait.until(  # ожидаем либо кнопку заказа, либо кнопку входа
            EC.any_of(
                EC.visibility_of_element_located(MainPageLocators.ORDER_BUTTON),  # кнопка «оформить заказ» для авторизованных
                EC.element_to_be_clickable(MainPageLocators.LOGIN_ACCOUNT_BUTTON),  # кнопка «войти в аккаунт» для неавторизованных
            )
        ) 

    def _build_email(self) -> str:  # локальный генератор email по шаблону задания
        suffix = "".join(random.choices(string.digits, k=5))  # собираем пять случайных цифр для уникальности
        return f"David_Garguliya_3637_{suffix}@yandex.ru"  # формируем адрес в требуемом формате

    def _build_password(self, length: int = 10) -> str:  # локальный генератор пароля
        if length < 6:  # следим за минимальной длиной
            length = 6  # поднимаем длину до 6, если передано меньше
        alphabet = string.ascii_letters + string.digits  # набор допустимых символов
        return "".join(random.choices(alphabet, k=length))  # собираем пароль указанной длины

    def _register_user_via_ui(self, driver, base_url: str, email: str, password: str):  # регистрируем пользователя через ui
        wait = WebDriverWait(driver, 10)  # создаём явное ожидание
        driver.get(f"{base_url}/register")  # открываем страницу регистрации
        wait.until(EC.visibility_of_element_located(RegistrationPageLocators.NAME_INPUT)).send_keys("David Garguiya")  # вводим имя
        wait.until(EC.visibility_of_element_located(RegistrationPageLocators.EMAIL_INPUT)).send_keys(email)  # вводим email
        wait.until(EC.visibility_of_element_located(RegistrationPageLocators.PASSWORD_INPUT)).send_keys(password)  # вводим пароль
        wait.until(EC.element_to_be_clickable(RegistrationPageLocators.SUBMIT_BUTTON)).click()  # отправляем форму регистрации
        wait.until(EC.visibility_of_element_located(LoginPageLocators.FORM_TITLE))  # ждём появления формы входа как подтверждение регистрации

    def _login_via_form(self, driver, email: str, password: str):  # авторизация через форму входа
        wait = WebDriverWait(driver, 10)  # создаём явное ожидание
        wait.until(EC.visibility_of_element_located(LoginPageLocators.EMAIL_INPUT)).send_keys(email)  # вводим email
        wait.until(EC.visibility_of_element_located(LoginPageLocators.PASSWORD_INPUT)).send_keys(password)  # вводим пароль
        wait.until(EC.element_to_be_clickable(LoginPageLocators.SUBMIT_BUTTON)).click()  # жмём «войти»
        wait.until(EC.visibility_of_element_located(MainPageLocators.ORDER_BUTTON))  # ждём кнопку «оформить заказ» как признак успешного входа

    def test_login_from_main_button(self, driver, base_url):  # вход по кнопке «войти в аккаунт» на главной
        email = self._build_email()  # генерируем email
        password = self._build_password()  # генерируем пароль
        self._register_user_via_ui(driver, base_url, email, password)  # регистрируем пользователя через ui

        driver.get(base_url)  # открываем главную страницу
        self._wait_main_ready(driver)  # ждём, пока главная станет доступной
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(MainPageLocators.LOGIN_ACCOUNT_BUTTON)).click()  # жмём «войти в аккаунт»
        self._login_via_form(driver, email, password)  # авторизуемся в открывшейся форме
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(MainPageLocators.ORDER_BUTTON))  # проверяем, что появилась кнопка «оформить заказ»

    def test_login_from_header_personal_account(self, driver, base_url):  # вход через кнопку «личный кабинет»
        email = self._build_email()  # генерируем email
        password = self._build_password()  # генерируем пароль
        self._register_user_via_ui(driver, base_url, email, password)  # регистрируем пользователя через ui

        driver.get(base_url)  # открываем главную
        self._wait_main_ready(driver)  # ждём, пока элементы главной будут доступны
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(MainPageLocators.PERSONAL_ACCOUNT_LINK)).click()  # жмём «личный кабинет»
        self._login_via_form(driver, email, password)  # заполняем форму входа
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(MainPageLocators.ORDER_BUTTON))  # убеждаемся, что авторизация прошла

    def test_login_from_registration_form_link(self, driver, base_url):  # вход через ссылку на форме регистрации
        email = self._build_email()  # генерируем email
        password = self._build_password()  # генерируем пароль
        self._register_user_via_ui(driver, base_url, email, password)  # регистрируем пользователя

        driver.get(f"{base_url}/register")  # открываем страницу регистрации
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(RegistrationPageLocators.LOGIN_LINK)).click()  # жмём ссылку «войти»
        self._login_via_form(driver, email, password)  # авторизуемся
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(MainPageLocators.ORDER_BUTTON))  # проверяем, что вход успешен

    def test_login_from_forgot_password_form(self, driver, base_url):  # вход через ссылку на форме восстановления
        email = self._build_email()  # генерируем email
        password = self._build_password()  # генерируем пароль
        self._register_user_via_ui(driver, base_url, email, password)  # регистрируем пользователя

        driver.get(f"{base_url}/forgot-password")  # открываем страницу восстановления пароля
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(ForgotPasswordLocators.LOGIN_LINK)).click()  # жмём ссылку «войти»
        self._login_via_form(driver, email, password)  # авторизуемся
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(MainPageLocators.ORDER_BUTTON))  # проверяем, что вошли

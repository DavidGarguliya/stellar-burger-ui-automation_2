import random  # используем для генерации случайных чисел
import string  # используем для набора символов в email и паролях

import pytest  # pytest для маркировки тестов
from selenium.webdriver.support import expected_conditions as EC  # условия ожидания selenium (сокращённо ec)
from selenium.webdriver.support.wait import WebDriverWait  # явные ожидания selenium

from tests.locators import (  # импортируем нужные локаторы
    MainPageLocators,
    LoginPageLocators,
    RegistrationPageLocators,
    ProfileLocators,
)

# Класс с проверками переходов и выхода
class TestNavigation:
    def _wait_main_ready(self, driver):  # ждём, пока главная страница прогрузится
        wait = WebDriverWait(driver, 10)  # создаём явное ожидание

        wait.until(  # ожидаем либо кнопку заказа, либо ссылку «личный кабинет»
            EC.any_of(
                EC.visibility_of_element_located(MainPageLocators.ORDER_BUTTON),
                EC.element_to_be_clickable(MainPageLocators.PERSONAL_ACCOUNT_LINK),
            )
        )
  
    # локальный генератор email
    def _build_email(self) -> str:
        suffix = "".join(random.choices(string.digits, k=5))  # пять случайных цифр для уникальности
        return f"David_Garguliya_3637_{suffix}@yandex.ru"  # возвращаем email по шаблону

    # локальный генератор пароля
    def _build_password(self, length: int = 10) -> str:
        if length < 6:  # проверяем минимальную длину
            length = 6  # обеспечиваем минимум 6 символов
        alphabet = string.ascii_letters + string.digits  # набор символов
        return "".join(random.choices(alphabet, k=length))  # возвращаем пароль
    
    # регистрация пользователя через ui
    def _register_user_via_ui(self, driver, base_url: str, email: str, password: str):
        wait = WebDriverWait(driver, 10)  # создаём явное ожидание

        driver.get(f"{base_url}/register")  # открываем страницу регистрации
        wait.until(EC.visibility_of_element_located(RegistrationPageLocators.NAME_INPUT)).send_keys("David Garguliya")  # вводим имя
        wait.until(EC.visibility_of_element_located(RegistrationPageLocators.EMAIL_INPUT)).send_keys(email)  # вводим email
        wait.until(EC.visibility_of_element_located(RegistrationPageLocators.PASSWORD_INPUT)).send_keys(password)  # вводим пароль
        wait.until(EC.element_to_be_clickable(RegistrationPageLocators.SUBMIT_BUTTON)).click()  # отправляем форму
        wait.until(EC.visibility_of_element_located(LoginPageLocators.FORM_TITLE))  # ждём появления формы входа

    # авторизация через ui
    def _login_user(self, driver, email: str, password: str):
        wait = WebDriverWait(driver, 10)  # создаём явное ожидание

        wait.until(EC.visibility_of_element_located(LoginPageLocators.EMAIL_INPUT)).send_keys(email)  # вводим email
        wait.until(EC.visibility_of_element_located(LoginPageLocators.PASSWORD_INPUT)).send_keys(password)  # вводим пароль
        wait.until(EC.element_to_be_clickable(LoginPageLocators.SUBMIT_BUTTON)).click()  # жмём «войти»
        wait.until(EC.visibility_of_element_located(MainPageLocators.ORDER_BUTTON))  # ждём кнопку «оформить заказ» как подтверждение логина

    # регистрация, логин и переход в профиль
    def _login_and_open_profile(self, driver, base_url: str, email: str, password: str):
        self._register_user_via_ui(driver, base_url, email, password)  # регистрируем пользователя через ui
        self._login_user(driver, email, password)  # авторизуемся на странице входа
        driver.get(base_url)  # возвращаемся на главную после логина
        self._wait_main_ready(driver)  # ждём доступности главной
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(MainPageLocators.PERSONAL_ACCOUNT_LINK)).click()  # переходим в личный кабинет
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(ProfileLocators.ACCOUNT_CONTAINER))  # убеждаемся, что профиль открыт
  
    # Переход в личный кабинет по клику на «Личный кабинет» после успешного входа
    def test_open_personal_account(self, driver, base_url):
        email = self._build_email()  # генерируем email
        password = self._build_password()  # генерируем пароль
        self._register_user_via_ui(driver, base_url, email, password)  # регистрируем пользователя
        self._login_user(driver, email, password)  # авторизуемся
        driver.get(base_url)  # обновляем главную страницу после логина
        self._wait_main_ready(driver)  # ждём, пока она станет доступной
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(MainPageLocators.PERSONAL_ACCOUNT_LINK)).click()  # жмём «личный кабинет»
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(ProfileLocators.ACCOUNT_CONTAINER))  # проверяем, что открылась страница профиля

    # Возврат в конструктор из личного кабинета по пункту «Конструктор»
    def test_return_to_constructor_from_profile_via_link(self, driver, base_url):
        email = self._build_email()  # генерируем email
        password = self._build_password()  # генерируем пароль
        self._login_and_open_profile(driver, base_url, email, password)  # регистрируем, логинимся и открываем профиль

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(MainPageLocators.CONSTRUCTOR_HEADER_LINK)).click()  # жмём «конструктор»
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(MainPageLocators.ORDER_BUTTON))  # проверяем, что вернулись в конструктор

    # Возврат в конструктор из личного кабинета по клику на логотип
    def test_return_to_constructor_from_profile_via_logo(self, driver, base_url):
        email = self._build_email()  # генерируем email
        password = self._build_password()  # генерируем пароль
        self._login_and_open_profile(driver, base_url, email, password)  # регистрируем, логинимся и открываем профиль

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(MainPageLocators.LOGO_LINK)).click()  # кликаем по логотипу
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(MainPageLocators.ORDER_BUTTON))  # проверяем, что оказались в конструкторе

    # Выход из аккаунта по кнопке «Выйти» в профиле
    def test_logout_from_profile(self, driver, base_url):  
        email = self._build_email()  # генерируем email
        password = self._build_password()  # генерируем пароль
        self._login_and_open_profile(driver, base_url, email, password)  # регистрируем, логинимся и открываем профиль

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(ProfileLocators.LOGOUT_BUTTON)).click()  # жмём «выход»
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(LoginPageLocators.FORM_TITLE))  # проверяем, что вернулись на форму входа

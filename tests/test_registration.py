import random  # используем для генерации случайных чисел
import string  # используем для набора символов в email и паролях

import pytest  # используем pytest для запуска тестов
from selenium.webdriver.support import expected_conditions as EC  # условия ожидания selenium (сокращённо ec)
from selenium.webdriver.support.wait import WebDriverWait  # явные ожидания selenium

from tests.locators import RegistrationPageLocators, LoginPageLocators  # локаторы элементов форм


# Класс с проверками сценариев регистрации
class TestRegistration:

    # локальный генератор email в требуемом формате
    def _build_email(self) -> str: 
        suffix = "".join(random.choices(string.digits, k=5))  # добавляем пять случайных цифр для уникальности
        return f"David_Garguliya_3637_{suffix}@yandex.ru"  # собираем и возвращаем email по шаблону из задания

    # локальный генератор пароля
    def _build_password(self, length: int = 10) -> str:  
        if length < 6:  # гарантируем минимальную длину
            length = 6  # поднимаем до 6, если меньше
        alphabet = string.ascii_letters + string.digits  # набор допустимых символов
        return "".join(random.choices(alphabet, k=length))  # собираем пароль из случайных символов

    # Валидная регистрация переводит на страницу входа
    def test_successful_registration_redirects_to_login(self, driver, base_url):  
        email = self._build_email()  # генерируем уникальный email
        password = self._build_password()  # генерируем валидный пароль
        wait = WebDriverWait(driver, 10)  # настраиваем явное ожидание на 10 секунд

        driver.get(f"{base_url}/register")  # открываем страницу регистрации
        wait.until(EC.visibility_of_element_located(RegistrationPageLocators.NAME_INPUT)).send_keys("David Garguliya")  # вводим имя
        wait.until(EC.visibility_of_element_located(RegistrationPageLocators.EMAIL_INPUT)).send_keys(email)  # вводим email
        wait.until(EC.visibility_of_element_located(RegistrationPageLocators.PASSWORD_INPUT)).send_keys(password)  # вводим пароль
        wait.until(EC.element_to_be_clickable(RegistrationPageLocators.SUBMIT_BUTTON)).click()  # жмём «зарегистрироваться»

        wait.until(EC.visibility_of_element_located(LoginPageLocators.FORM_TITLE))  # проверяем, что открылась форма входа

    # При пароле короче 6 символов отображается ошибка
    def test_short_password_shows_error(self, driver, base_url):  
        email = self._build_email()  # генерируем уникальный email
        wait = WebDriverWait(driver, 10)  # настраиваем явное ожидание

        driver.get(f"{base_url}/register")  # открываем форму регистрации
        wait.until(EC.visibility_of_element_located(RegistrationPageLocators.NAME_INPUT)).send_keys("Test User")  # вводим имя
        wait.until(EC.visibility_of_element_located(RegistrationPageLocators.EMAIL_INPUT)).send_keys(email)  # вводим email
        wait.until(EC.visibility_of_element_located(RegistrationPageLocators.PASSWORD_INPUT)).send_keys("12345")  # короткий пароль
        wait.until(EC.element_to_be_clickable(RegistrationPageLocators.SUBMIT_BUTTON)).click()  # отправляем форму

        error = wait.until(EC.visibility_of_element_located(RegistrationPageLocators.ERROR_MESSAGE))  # ждём текст ошибки
        assert "парол" in error.text.lower()  # проверяем, что сообщение связано с паролем

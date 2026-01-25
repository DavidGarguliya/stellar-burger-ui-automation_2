import pytest  # используем pytest для запуска тестов
from selenium.webdriver.support import expected_conditions as EC  # условия ожидания selenium (сокращённо ec)
from selenium.webdriver.support.wait import WebDriverWait  # явные ожидания selenium

from tests.settings import BASE_URL  # базовый адрес сервиса
from tests.utils.data_generators import build_email, build_password  # генераторы тестовых данных
from tests.locators import RegistrationPageLocators, LoginPageLocators  # локаторы элементов форм


# Класс с проверками сценариев регистрации
class TestRegistration:
    
    # Валидная регистрация переводит на страницу входа
    def test_successful_registration_redirects_to_login(self, driver):  
        email = build_email()  # генерируем уникальный email
        password = build_password()  # генерируем валидный пароль
        wait = WebDriverWait(driver, 10)  # настраиваем явное ожидание на 10 секунд

        driver.get(f"{BASE_URL}/register")  # открываем страницу регистрации
        wait.until(EC.visibility_of_element_located(RegistrationPageLocators.NAME_INPUT)).send_keys("David Garguliya")  # вводим имя
        wait.until(EC.visibility_of_element_located(RegistrationPageLocators.EMAIL_INPUT)).send_keys(email)  # вводим email
        wait.until(EC.visibility_of_element_located(RegistrationPageLocators.PASSWORD_INPUT)).send_keys(password)  # вводим пароль
        wait.until(EC.element_to_be_clickable(RegistrationPageLocators.SUBMIT_BUTTON)).click()  # жмём «зарегистрироваться»

        wait.until(EC.url_contains("/login"))  # дождались редиректа на логин
        titles = driver.find_elements(*LoginPageLocators.FORM_TITLE)
        assert titles and titles[0].is_displayed()  # подтверждаем, что заголовок найден и видим

    # При пароле короче 6 символов отображается ошибка
    def test_short_password_shows_error(self, driver):  
        email = build_email()  # генерируем уникальный email
        wait = WebDriverWait(driver, 10)  # настраиваем явное ожидание

        driver.get(f"{BASE_URL}/register")  # открываем форму регистрации
        wait.until(EC.visibility_of_element_located(RegistrationPageLocators.NAME_INPUT)).send_keys("Test User")  # вводим имя
        wait.until(EC.visibility_of_element_located(RegistrationPageLocators.EMAIL_INPUT)).send_keys(email)  # вводим email
        wait.until(EC.visibility_of_element_located(RegistrationPageLocators.PASSWORD_INPUT)).send_keys("12345")  # короткий пароль
        wait.until(EC.element_to_be_clickable(RegistrationPageLocators.SUBMIT_BUTTON)).click()  # отправляем форму

        error = wait.until(EC.visibility_of_element_located(RegistrationPageLocators.ERROR_MESSAGE))  # ждём текст ошибки
        expected_text = "Некорректный пароль"
        assert error.text.strip() == expected_text  # проверяем точное сообщение об ошибке по ТЗ

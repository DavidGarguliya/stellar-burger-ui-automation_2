import pytest  # pytest для запуска тестов
from selenium.webdriver.support import expected_conditions as EC  # условия ожидания selenium (сокращённо EC)
from selenium.webdriver.support.wait import WebDriverWait  # явные ожидания selenium

from tests.locators import ConstructorLocators, MainPageLocators  # локаторы конструктора и главной

# Класс с проверками переключения вкладок конструктора
class TestConstructorTabs:  
    
    # Проверяем переход к табу «Соусы»
    def test_switch_to_sauces_tab(self, driver, base_url):  

        driver.get(base_url)  # открываем главную страницу
        wait = WebDriverWait(driver, 3)  # создаём явное ожидание, присваиваем переменной wait
        
        wait.until(EC.element_to_be_clickable(ConstructorLocators.SAUCES_TAB)) # ждём табы конструктора
        wait.until(EC.element_to_be_clickable(ConstructorLocators.SAUCES_TAB)).click()  # кликаем по табу соусы
        active_text = wait.until(EC.visibility_of_element_located(ConstructorLocators.ACTIVE_TAB)).text  # считываем текст активного таба

        assert "Соусы" in active_text  # проверяем что в тексте активного таба содержится Соусы

    # Проверяем переход к табу «Начинки»
    def test_switch_to_fillings_tab(self, driver, base_url):  
        driver.get(base_url)  # открываем главную страницу
        wait = WebDriverWait(driver, 3)  # создаём явное ожидание, присваиваем переменной wait

        wait.until(EC.element_to_be_clickable(ConstructorLocators.FILLINGS_TAB)) # ждём табы конструктора
        wait.until(EC.element_to_be_clickable(ConstructorLocators.FILLINGS_TAB)).click()  # кликаем по табу начинки
        active_text = wait.until(EC.visibility_of_element_located(ConstructorLocators.ACTIVE_TAB)).text  # считываем текст активного таба

        assert "Начинки" in active_text  # проверяем что в тексте активного таба содержится Начинки

    # Проверяем переход к табу «Булки»
    def test_switch_to_buns_tab(self, driver, base_url):
        driver.get(base_url)  # открываем главную страницу
        wait = WebDriverWait(driver, 3)  # создаём явное ожидание, присваиваем переменной wait

        wait.until(EC.element_to_be_clickable(ConstructorLocators.BUNS_TAB)) # ждём табы конструктора
        wait.until(EC.element_to_be_clickable(ConstructorLocators.SAUCES_TAB)).click()  # сначала переключаемся на таб соусы
        wait.until(EC.element_to_be_clickable(ConstructorLocators.BUNS_TAB)).click()  # затем кликаем по табу булки

        active_text = wait.until(EC.visibility_of_element_located(ConstructorLocators.ACTIVE_TAB)).text  # считываем текст активного таба

        assert "Булки" in active_text  # проверяем что в тексте активного таба содержится Булки


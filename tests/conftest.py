import pytest  # импортируем pytest
from selenium import webdriver  # импортируем selenium webdriver

# Фикстура будет создана один раз за сессию
@pytest.fixture(scope="session")  
def base_url() -> str:  # возвращает адрес тестируемого сайта
    return "https://stellarburgers.education-services.ru"  # жёстко задаём базовый url сервиса

# Фикстура создаёт и закрывает браузер для каждого теста
@pytest.fixture  
def driver():  # инициализация и закрытие браузера
    driver = webdriver.Chrome()  # стартуем chrome без дополнительных опций, чтобы видеть окно
    driver.implicitly_wait(3)  # добавляем небольшое неявное ожидание для поиска элементов
    yield driver  # передаём драйвер в тест
    driver.quit()  # закрываем браузер после завершения теста, чтобы не оставлять процессы

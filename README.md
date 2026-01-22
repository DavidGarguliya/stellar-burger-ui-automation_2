# Stellar Burgers UI Autotests

Набор UI-тестов для учебного сервиса Stellar Burgers (https://stellarburgers.education-services.ru/) на Python + Pytest + Selenium.

## Подготовка окружения
- `python3 -m venv .venv && source .venv/bin/activate`
- `pip install -r requirements.txt`
- Установите Google Chrome и подходящий `chromedriver`, добавьте его в `PATH`. Без установленного драйвера браузер не запустится.

## Запуск
- Все тесты: `pytest -v`
- Отдельный файл: `pytest tests/test_registration.py -v`
- Браузер Chrome стартует в видимом режиме из фикстуры `driver`.

## Структура
- `tests/` — тесты и фикстуры.
- `tests/settings.py` — базовые константы (в т.ч. `BASE_URL`).
- `tests/locators.py` — локаторы с комментариями.
- `tests/utils/data_generators.py` — генераторы email/пароля.
- `tests/utils/ui_flows.py` — общие UI-шаги (ожидание главной, регистрация, логин, открытие профиля).
- Все тесты используют общие утилиты, проверки оформлены через явные `assert`.

## Реализованные проверки
### tests/test_registration.py
- `test_successful_registration_redirects_to_login`: валидная регистрация переводит на страницу входа.
- `test_short_password_shows_error`: при пароле короче 6 символов отображается ошибка.

### tests/test_login.py
- `test_login_from_main_button`: вход по кнопке «Войти в аккаунт» на главной.
- `test_login_from_header_personal_account`: вход через «Личный кабинет» в шапке.
- `test_login_from_registration_form_link`: вход через ссылку «Войти» на форме регистрации.
- `test_login_from_forgot_password_form`: вход через ссылку «Войти» на форме восстановления пароля.

### tests/test_navigation.py
- `test_open_personal_account`: переход в личный кабинет по клику на «Личный кабинет» после успешного входа.
- `test_return_to_constructor_from_profile_via_link`: возврат в конструктор из личного кабинета по пункту «Конструктор».
- `test_return_to_constructor_from_profile_via_logo`: возврат в конструктор из личного кабинета по клику на логотип.
- `test_logout_from_profile`: выход из аккаунта по кнопке «Выйти» в профиле.

### tests/test_constructor_tabs.py
- `test_switch_to_sauces_tab`: переход к разделу «Соусы».
- `test_switch_to_fillings_tab`: переход к разделу «Начинки» 
- `test_switch_to_buns_tab`: переход к разделу «Булки»

# Sprint_5

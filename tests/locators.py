from selenium.webdriver.common.by import By  # by даёт типы стратегий поиска элементов


# Локаторы для главной страницы
class MainPageLocators:  # группируем элементы главной
    LOGIN_ACCOUNT_BUTTON = (By.XPATH, "//button[text()='Войти в аккаунт']")  # кнопка входа на главной странице
    PERSONAL_ACCOUNT_LINK = (By.XPATH, "//p[text()='Личный Кабинет']/parent::a")  # ссылка «личный кабинет» в шапке
    CONSTRUCTOR_HEADER_LINK = (By.XPATH, "//p[text()='Конструктор']/parent::a")  # пункт «конструктор» в шапке
    LOGO_LINK = (By.CSS_SELECTOR, "div.AppHeader_header__logo__2D0X2 a")  # логотип stellar burgers
    ORDER_BUTTON = (By.XPATH, "//button[contains(.,'Оформить заказ')]")  # кнопка «оформить заказ» после авторизации


# Локаторы для формы входа
class LoginPageLocators:  # элементы страницы логина
    EMAIL_INPUT = (By.XPATH, "//label[text()='Email']/following::input[1]")  # поле email в форме входа
    PASSWORD_INPUT = (By.XPATH, "//label[text()='Пароль']/following::input[1]")  # поле пароля в форме входа
    SUBMIT_BUTTON = (By.XPATH, "//button[text()='Войти']")  # кнопка «войти» на форме входа
    REGISTER_LINK = (By.LINK_TEXT, "Зарегистрироваться")  # ссылка на форму регистрации
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Восстановить пароль")  # ссылка на восстановление пароля
    FORM_TITLE = (By.XPATH, "//h2[text()='Вход']")  # заголовок страницы «вход»


# Локаторы для формы регистрации
class RegistrationPageLocators:  # элементы формы регистрации
    NAME_INPUT = (By.XPATH, "//label[text()='Имя']/following::input[1]")  # поле имени в форме регистрации
    EMAIL_INPUT = (By.XPATH, "//label[text()='Email']/following::input[1]")  # поле email в форме регистрации
    PASSWORD_INPUT = (By.XPATH, "//label[text()='Пароль']/following::input[1]")  # поле пароля в форме регистрации
    SUBMIT_BUTTON = (By.XPATH, "//button[text()='Зарегистрироваться']")  # кнопка «зарегистрироваться»
    LOGIN_LINK = (By.LINK_TEXT, "Войти")  # ссылка на форму входа из регистрации
    ERROR_MESSAGE = (By.XPATH, "//p[contains(@class,'input__error')]")  # сообщение об ошибке под полем пароля


# Локаторы для страницы восстановления пароля
class ForgotPasswordLocators:  # элементы восстановления пароля
    EMAIL_INPUT = (By.XPATH, "//label[text()='Email']/following::input[1]")  # поле email в восстановлении пароля
    RECOVER_BUTTON = (By.XPATH, "//button[text()='Восстановить']")  # кнопка «восстановить»
    LOGIN_LINK = (By.LINK_TEXT, "Войти")  # ссылка «войти» на странице восстановления
    PAGE_TITLE = (By.XPATH, "//h2[text()='Восстановление пароля']")  # заголовок страницы восстановления


# Локаторы для личного кабинета
class ProfileLocators:  # элементы профиля
    PROFILE_LINK = (By.XPATH, "//a[contains(@href,'/account/profile')]")  # пункт меню «профиль»
    LOGOUT_BUTTON = (By.XPATH, "//button[text()='Выход']")  # кнопка «выход» в личном кабинете
    ACCOUNT_CONTAINER = (By.CLASS_NAME, "Profile_profileList__3vTor")  # блок данных профиля


# Локаторы для вкладок конструктора
class ConstructorLocators:  # элементы переключения вкладок
    BUNS_TAB = (By.XPATH, "//span[text()='Булки']/parent::*")  # таб «булки»
    SAUCES_TAB = (By.XPATH, "//span[text()='Соусы']/parent::*")  # таб «соусы»
    FILLINGS_TAB = (By.XPATH, "//span[text()='Начинки']/parent::*")  # таб «начинки»
    ACTIVE_TAB = (By.CSS_SELECTOR, ".tab_tab_type_current__2BEPc")  # активный таб конструктора

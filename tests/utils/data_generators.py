# Генераторы тестовых данных

import random
import string

# Генерация email
def build_email() -> str:
    suffix = "".join(random.choices(string.digits, k=5))
    return f"David_Garguliya_3637_{suffix}@yandex.ru"

# Генерация пароля
def build_password(length: int = 10) -> str:
    length = max(length, 6)
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choices(alphabet, k=length))

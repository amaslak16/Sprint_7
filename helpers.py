import random
import string
from datetime import date, timedelta

import allure


def random_string(length=12):
    alphabet = string.ascii_lowercase + string.digits
    return "".join(random.choices(alphabet, k=length))


@allure.step("Подготовить данные курьера")
def make_courier_payload():
    suffix = random_string()
    return {
        "login": f"courier_{suffix}",
        "password": f"pass_{random_string(12)}",
        "firstName": f"Test{random_string(6)}",
    }


@allure.step("Подготовить данные заказа")
def make_order_payload():
    return {
        "firstName": "Тест",
        "lastName": "Тестов",
        "address": "Москва, улица Тестовая, 1",
        "metroStation": 4,
        "phone": "+7 800 555-35-35",
        "rentTime": 2,
        "deliveryDate": (date.today() + timedelta(days=7)).isoformat(),
        "comment": "Проверка API",
    }

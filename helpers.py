import random
import string
from datetime import date, timedelta

import requests

from constants import BASE_URL, REQUEST_TIMEOUT


class ApiClient:
    """Тонкая обёртка над запросами к учебному API."""

    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def request(self, method, path, **kwargs):
        kwargs.setdefault("timeout", REQUEST_TIMEOUT)
        return self.session.request(method, f"{self.base_url}{path}", **kwargs)

    def create_courier(self, payload):
        return self.request("POST", "/api/v1/courier", json=payload)

    def login_courier(self, payload):
        return self.request("POST", "/api/v1/courier/login", json=payload)

    def delete_courier(self, courier_id):
        return self.request("DELETE", f"/api/v1/courier/{courier_id}")

    def create_order(self, payload):
        return self.request("POST", "/api/v1/orders", json=payload)

    def list_orders(self, **params):
        return self.request("GET", "/api/v1/orders", params=params)

    def accept_order(self, order_id, courier_id=None):
        params = {} if courier_id is None else {"courierId": courier_id}
        path = "/api/v1/orders/accept"
        if order_id is not None:
            path += f"/{order_id}"
        return self.request(
            "PUT", path, params=params
        )

    def get_order_by_track(self, track=None):
        params = {} if track is None else {"t": track}
        return self.request("GET", "/api/v1/orders/track", params=params)


def random_string(length=12):
    alphabet = string.ascii_lowercase + string.digits
    return "".join(random.choices(alphabet, k=length))


def make_courier_payload():
    suffix = random_string()
    return {
        "login": f"courier_{suffix}",
        "password": f"pass_{random_string(12)}",
        "firstName": f"Test{random_string(6)}",
    }


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
        "color": [],
    }

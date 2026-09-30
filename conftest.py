import pytest

from api_client import ApiClient
from helpers import make_courier_payload, make_order_payload


@pytest.fixture
def api_client():
    client = ApiClient()
    yield client
    client.session.close()


@pytest.fixture
def courier_factory(api_client):
    """Создаёт курьеров по запросу теста и удаляет их после теста."""
    created = []

    def create(payload=None):
        data = make_courier_payload() if payload is None else payload
        response = api_client.create_courier(data)
        if response.status_code == 201:
            created.append(data)
        return data, response

    yield create

    for data in created:
        login_response = api_client.login_courier(
            {"login": data["login"], "password": data["password"]}
        )
        if login_response.status_code == 200:
            api_client.delete_courier(login_response.json()["id"])


@pytest.fixture
def registered_courier(courier_factory):
    data, response = courier_factory()
    if response.status_code != 201:
        raise RuntimeError(f"Не удалось создать курьера для теста: {response.text}")
    return data


@pytest.fixture
def registered_courier_id(api_client, registered_courier):
    response = api_client.login_courier(
        {
            "login": registered_courier["login"],
            "password": registered_courier["password"],
        }
    )
    if response.status_code != 200:
        raise RuntimeError(f"Не удалось получить ID курьера для теста: {response.text}")
    return response.json()["id"]


@pytest.fixture
def created_order_track(api_client):
    response = api_client.create_order(make_order_payload())
    if response.status_code != 201:
        raise RuntimeError(f"Не удалось создать заказ для теста: {response.text}")
    return response.json()["track"]


@pytest.fixture
def created_order_id(api_client, created_order_track):
    response = api_client.get_order_by_track(created_order_track)
    if response.status_code != 200:
        raise RuntimeError(f"Не удалось получить ID заказа для теста: {response.text}")
    return response.json()["order"]["id"]

import pytest

from helpers import ApiClient, make_courier_payload


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
        data = payload or make_courier_payload()
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
    assert response.status_code == 201, response.text
    return data

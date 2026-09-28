import allure

from helpers import make_order_payload


@allure.feature("Заказы")
class TestAcceptOrder:
    @allure.title("Курьер может принять заказ")
    def test_accept_order_success(self, api_client, courier_factory):
        courier, create_courier_response = courier_factory()
        assert create_courier_response.status_code == 201
        courier_id = api_client.login_courier(
            {"login": courier["login"], "password": courier["password"]}
        ).json()["id"]

        order_response = api_client.create_order(make_order_payload())
        assert order_response.status_code == 201
        track = order_response.json()["track"]
        order_response = api_client.get_order_by_track(track)
        order_id = order_response.json()["order"]["id"]

        response = api_client.accept_order(order_id, courier_id)

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Нельзя принять заказ без ID курьера")
    def test_accept_order_without_courier_id_returns_error(self, api_client):
        order_response = api_client.create_order(make_order_payload())
        assert order_response.status_code == 201
        order_id = api_client.get_order_by_track(
            order_response.json()["track"]
        ).json()["order"]["id"]

        response = api_client.accept_order(order_id)

        assert response.status_code >= 400

    @allure.title("Нельзя принять заказ с несуществующим ID курьера")
    def test_accept_order_with_nonexistent_courier_returns_error(self, api_client):
        order_response = api_client.create_order(make_order_payload())
        assert order_response.status_code == 201
        order_id = api_client.get_order_by_track(
            order_response.json()["track"]
        ).json()["order"]["id"]

        response = api_client.accept_order(order_id, -1)

        assert response.status_code >= 400

    @allure.title("Нельзя принять заказ без ID заказа")
    def test_accept_order_without_order_id_returns_error(
        self, api_client, courier_factory
    ):
        courier, create_response = courier_factory()
        assert create_response.status_code == 201
        courier_id = api_client.login_courier(
            {"login": courier["login"], "password": courier["password"]}
        ).json()["id"]

        response = api_client.accept_order(None, courier_id)

        assert response.status_code >= 400

    @allure.title("Нельзя принять заказ с несуществующим ID")
    def test_accept_nonexistent_order_returns_error(
        self, api_client, courier_factory
    ):
        courier, create_response = courier_factory()
        assert create_response.status_code == 201
        courier_id = api_client.login_courier(
            {"login": courier["login"], "password": courier["password"]}
        ).json()["id"]

        response = api_client.accept_order(-1, courier_id)

        assert response.status_code >= 400

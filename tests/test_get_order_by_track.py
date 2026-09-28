import allure

from helpers import make_order_payload


@allure.feature("Заказы")
class TestGetOrderByTrack:
    @allure.title("Заказ можно получить по его номеру")
    def test_get_order_by_track_success(self, api_client):
        create_response = api_client.create_order(make_order_payload())
        assert create_response.status_code == 201
        track = create_response.json()["track"]

        response = api_client.get_order_by_track(track)

        assert response.status_code == 200
        assert isinstance(response.json().get("order"), dict)

    @allure.title("Без номера заказа API возвращает ошибку")
    def test_get_order_without_track_returns_error(self, api_client):
        response = api_client.get_order_by_track()

        assert response.status_code >= 400

    @allure.title("Несуществующий номер заказа возвращает ошибку")
    def test_get_nonexistent_order_returns_error(self, api_client):
        response = api_client.get_order_by_track(-1)

        assert response.status_code >= 400

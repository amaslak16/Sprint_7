import allure


@allure.feature("Заказы")
class TestGetOrderByTrack:
    @allure.title("Заказ можно получить по его номеру")
    def test_get_order_by_track_success(self, api_client, created_order_track):
        response = api_client.get_order_by_track(created_order_track)

        assert response.status_code == 200
        assert response.json()["order"]["track"] == created_order_track

    @allure.title("Без номера заказа API возвращает ошибку")
    def test_get_order_without_track_returns_error(self, api_client):
        response = api_client.get_order_by_track()

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для поиска"

    @allure.title("Несуществующий номер заказа возвращает ошибку")
    def test_get_nonexistent_order_returns_error(self, api_client):
        response = api_client.get_order_by_track(999999999)

        assert response.status_code == 404
        assert response.json()["message"] == "Заказ не найден"

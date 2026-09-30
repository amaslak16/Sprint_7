import allure


@allure.feature("Заказы")
class TestAcceptOrder:
    @allure.title("Курьер может принять заказ")
    def test_accept_order_success(
        self, api_client, registered_courier_id, created_order_id
    ):
        response = api_client.accept_order(created_order_id, registered_courier_id)

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Нельзя принять заказ без ID курьера")
    def test_accept_order_without_courier_id_returns_error(
        self, api_client, created_order_id
    ):
        response = api_client.accept_order(created_order_id)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для поиска"

    @allure.title("Нельзя принять заказ с несуществующим ID курьера")
    def test_accept_order_with_nonexistent_courier_returns_error(
        self, api_client, created_order_id
    ):
        response = api_client.accept_order(created_order_id, -1)

        assert response.status_code == 404
        assert response.json()["message"] == "Курьера с таким id не существует"

    @allure.title("Нельзя принять заказ без ID заказа")
    def test_accept_order_without_order_id_returns_error(
        self, api_client, registered_courier_id
    ):
        response = api_client.accept_order(None, registered_courier_id)

        # Маршрут без ID не совпадает с /orders/accept/:id и возвращает 404.
        assert response.status_code == 404
        assert response.json()["message"] == "Not Found."

    @allure.title("Нельзя принять заказ с несуществующим ID заказа")
    def test_accept_nonexistent_order_returns_error(
        self, api_client, registered_courier_id
    ):
        response = api_client.accept_order(-1, registered_courier_id)

        assert response.status_code == 404
        assert response.json()["message"] == "Заказа с таким id не существует"

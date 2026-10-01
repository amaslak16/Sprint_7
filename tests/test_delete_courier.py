import allure


@allure.feature("Курьер")
class TestDeleteCourier:
    @allure.title("Успешное удаление курьера")
    def test_delete_courier_success(self, api_client, registered_courier_id):
        response = api_client.delete_courier(registered_courier_id)

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Несуществующего курьера нельзя удалить")
    def test_delete_nonexistent_courier_returns_error(self, api_client):
        response = api_client.delete_courier(-1)

        assert response.status_code == 404
        assert response.json()["message"] == "Курьера с таким id нет."

    @allure.title("Без ID курьера запрос на удаление возвращает ошибку")
    def test_delete_courier_without_id_returns_error(self, api_client):
        response = api_client.request("DELETE", "/api/v1/courier")

        # Маршрут без ID не совпадает с /courier/:id и возвращает 404.
        assert response.status_code == 404
        assert response.json()["message"] == "Not Found."

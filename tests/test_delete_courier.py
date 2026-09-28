import allure


@allure.feature("Курьер")
class TestDeleteCourier:
    @allure.title("Успешное удаление курьера")
    def test_delete_courier_success(self, api_client, courier_factory):
        data, create_response = courier_factory()
        assert create_response.status_code == 201
        courier_id = api_client.login_courier(
            {"login": data["login"], "password": data["password"]}
        ).json()["id"]

        response = api_client.delete_courier(courier_id)

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Несуществующего курьера нельзя удалить")
    def test_delete_nonexistent_courier_returns_error(self, api_client):
        response = api_client.delete_courier(-1)

        assert response.status_code >= 400
        assert "message" in response.json()

    @allure.title("Без ID курьера запрос на удаление возвращает ошибку")
    def test_delete_courier_without_id_returns_error(self, api_client):
        response = api_client.request("DELETE", "/api/v1/courier")

        assert response.status_code >= 400

import allure
import pytest


@allure.feature("Курьер")
class TestCreateCourier:
    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, courier_factory):
        _, response = courier_factory()

        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Нельзя создать курьера с уже занятым логином")
    def test_cannot_create_duplicate_courier(
        self, api_client, registered_courier
    ):
        duplicate_response = api_client.create_courier(registered_courier)

        assert duplicate_response.status_code == 409
        assert (
            duplicate_response.json()["message"]
            == "Этот логин уже используется. Попробуйте другой."
        )

    @pytest.mark.parametrize(
        "missing_field", ["login", "password"], ids=["без-логина", "без-пароля"]
    )
    @allure.title("Нельзя создать курьера без обязательного поля")
    def test_create_courier_without_required_field(
        self, api_client, missing_field
    ):
        payload = {"login": "test_login", "password": "test_password"}
        payload.pop(missing_field)

        response = api_client.create_courier(payload)

        assert response.status_code == 400
        assert (
            response.json()["message"]
            == "Недостаточно данных для создания учетной записи"
        )

import allure
import pytest


@allure.feature("Авторизация курьера")
class TestLoginCourier:
    @allure.title("Курьер может войти в систему")
    def test_login_courier_success(self, api_client, registered_courier):
        response = api_client.login_courier(
            {
                "login": registered_courier["login"],
                "password": registered_courier["password"],
            }
        )

        assert response.status_code == 200
        assert isinstance(response.json().get("id"), int)

    @pytest.mark.parametrize(
        "missing_field", ["login", "password"], ids=["без-логина", "без-пароля"]
    )
    @allure.title("Для входа обязательны логин и пароль")
    def test_login_without_required_field(
        self, api_client, registered_courier, missing_field
    ):
        payload = {
            "login": registered_courier["login"],
            "password": registered_courier["password"],
        }
        payload.pop(missing_field)

        response = api_client.login_courier(payload)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Несуществующий курьер не может войти")
    def test_login_with_nonexistent_courier_returns_error(self, api_client):
        response = api_client.login_courier(
            {"login": "missing_user_12345", "password": "wrong_password"}
        )

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Курьер не может войти с неправильным паролем")
    def test_login_with_wrong_password_returns_error(
        self, api_client, registered_courier
    ):
        response = api_client.login_courier(
            {"login": registered_courier["login"], "password": "wrong_password"}
        )

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

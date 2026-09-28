import allure
import pytest

from helpers import make_order_payload


@allure.feature("Заказы")
class TestCreateOrder:
    @pytest.mark.parametrize(
        "colors",
        [["BLACK"], ["GREY"], ["BLACK", "GREY"], []],
        ids=["чёрный", "серый", "оба-цвета", "без-цвета"],
    )
    @allure.title("Заказ создаётся с выбранными цветами самоката")
    def test_create_order_with_colors_returns_track(self, api_client, colors):
        payload = make_order_payload()
        if colors:
            payload["color"] = colors
        else:
            payload.pop("color")

        response = api_client.create_order(payload)

        assert response.status_code == 201
        assert isinstance(response.json().get("track"), int)

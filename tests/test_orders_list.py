import allure


@allure.feature("Заказы")
class TestOrdersList:
    @allure.title("Получение списка заказов")
    def test_list_orders_returns_orders(self, api_client):
        response = api_client.list_orders(limit=10, page=0)

        assert response.status_code == 200
        assert isinstance(response.json().get("orders"), list)

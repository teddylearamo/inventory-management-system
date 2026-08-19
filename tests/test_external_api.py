from unittest.mock import patch

from server.external_api import get_product_by_barcode


def test_get_product_by_barcode():
    mock_response = {
        "status": 1,
        "product": {
            "product_name": "Nutella",
            "brands": "Ferrero"
        }
    }

    with patch("server.external_api.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        product = get_product_by_barcode("3017620422003")

        assert product["product_name"] == "Nutella"
        assert product["brands"] == "Ferrero"


def test_get_product_by_barcode_not_found():
    mock_response = {
        "status": 0
    }

    with patch("server.external_api.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        product = get_product_by_barcode("0000000000000")

        assert product is None
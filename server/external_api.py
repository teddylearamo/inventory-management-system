import requests


BASE_URL = "https://world.openfoodfacts.org/api/v3/product"


def get_product_by_barcode(barcode):
    url = f"{BASE_URL}/{barcode}"

    response = requests.get(
        url,
        headers={
            "User-Agent": "InventoryManagementSystem/1.0"
        },
        timeout=10
    )

    if response.status_code != 200:
        return None

    data = response.json()

    return data.get("product")
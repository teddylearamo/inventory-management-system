import argparse
import requests


BASE_URL = "http://127.0.0.1:5000"


def list_inventory():
    response = requests.get(f"{BASE_URL}/inventory")

    if response.status_code == 200:
        items = response.json()

        if not items:
            print("No inventory items found.")
            return

        for item in items:
            print(
                f"ID: {item['id']} | "
                f"Name: {item['name']} | "
                f"Barcode: {item['barcode']} | "
                f"Quantity: {item['quantity']} | "
                f"Price: {item['price']}"
            )
    else:
        print("Failed to retrieve inventory.")


def get_inventory_item(item_id):
    response = requests.get(
        f"{BASE_URL}/inventory/{item_id}"
    )

    if response.status_code == 200:
        print(response.json())
    else:
        print("Inventory item not found.")


def add_inventory_item(name, barcode, quantity, price):
    data = {
        "name": name,
        "barcode": barcode,
        "quantity": quantity,
        "price": price
    }

    response = requests.post(
        f"{BASE_URL}/inventory",
        json=data
    )

    if response.status_code == 201:
        print("Inventory item added successfully.")
        print(response.json())
    else:
        print(response.json())


def update_inventory_item(item_id, name, barcode, quantity, price):
    data = {}

    if name is not None:
        data["name"] = name

    if barcode is not None:
        data["barcode"] = barcode

    if quantity is not None:
        data["quantity"] = quantity

    if price is not None:
        data["price"] = price

    response = requests.put(
        f"{BASE_URL}/inventory/{item_id}",
        json=data
    )

    if response.status_code == 200:
        print("Inventory item updated successfully.")
        print(response.json())
    else:
        print(response.json())


def delete_inventory_item(item_id):
    response = requests.delete(
        f"{BASE_URL}/inventory/{item_id}"
    )

    if response.status_code == 200:
        print("Inventory item deleted successfully.")
    else:
        print(response.json())


def lookup_product(barcode):
    response = requests.get(
        f"{BASE_URL}/products/{barcode}"
    )

    if response.status_code == 200:
        product = response.json()

        print("Product found:")
        print(f"Name: {product.get('product_name', 'Unknown')}")
        print(f"Brands: {product.get('brands', 'Unknown')}")
        print(f"Categories: {product.get('categories', 'Unknown')}")
    else:
        print("Product not found.")


def main():
    parser = argparse.ArgumentParser(
        description="Inventory Management CLI"
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

    subparsers.add_parser(
        "list",
        help="List all inventory items"
    )

    get_parser = subparsers.add_parser(
        "get",
        help="Get one inventory item"
    )
    get_parser.add_argument(
        "id",
        type=int
    )

    add_parser = subparsers.add_parser(
        "add",
        help="Add an inventory item"
    )
    add_parser.add_argument("name")
    add_parser.add_argument("barcode")
    add_parser.add_argument("quantity", type=int)
    add_parser.add_argument("price", type=float)

    update_parser = subparsers.add_parser(
        "update",
        help="Update an inventory item"
    )
    update_parser.add_argument(
        "id",
        type=int
    )
    update_parser.add_argument("--name")
    update_parser.add_argument("--barcode")
    update_parser.add_argument(
        "--quantity",
        type=int
    )
    update_parser.add_argument(
        "--price",
        type=float
    )

    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete an inventory item"
    )
    delete_parser.add_argument(
        "id",
        type=int
    )

    lookup_parser = subparsers.add_parser(
        "lookup",
        help="Look up a product using OpenFoodFacts"
    )
    lookup_parser.add_argument(
        "barcode"
    )

    args = parser.parse_args()

    if args.command == "list":
        list_inventory()

    elif args.command == "get":
        get_inventory_item(args.id)

    elif args.command == "add":
        add_inventory_item(
            args.name,
            args.barcode,
            args.quantity,
            args.price
        )

    elif args.command == "update":
        update_inventory_item(
            args.id,
            args.name,
            args.barcode,
            args.quantity,
            args.price
        )

    elif args.command == "delete":
        delete_inventory_item(args.id)

    elif args.command == "lookup":
        lookup_product(args.barcode)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
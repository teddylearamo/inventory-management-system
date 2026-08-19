from flask import Flask, jsonify, request

from external_api import get_product_by_barcode

from models import (
    initialize_database,
    get_all_items,
    get_item,
    add_item,
    update_item,
    delete_item
)

app = Flask(__name__)


initialize_database()


@app.route("/")
def home():
    return jsonify({
        "message": "Inventory Management API"
    })


@app.route("/inventory", methods=["GET"])
def get_inventory():
    items = get_all_items()

    return jsonify(items)


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    item = get_item(item_id)

    if item is None:
        return jsonify({
            "error": "Inventory item not found"
        }), 404

    return jsonify(item)


@app.route("/inventory", methods=["POST"])
def add_inventory_item():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    required_fields = [
        "name",
        "barcode",
        "quantity",
        "price"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    item = add_item(
        data["name"],
        data["barcode"],
        data["quantity"],
        data["price"]
    )

    return jsonify(item), 201


@app.route("/inventory/<int:item_id>", methods=["PUT"])
def update_inventory_item(item_id):
    item = get_item(item_id)

    if item is None:
        return jsonify({
            "error": "Inventory item not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    name = data.get("name", item["name"])
    barcode = data.get("barcode", item["barcode"])
    quantity = data.get("quantity", item["quantity"])
    price = data.get("price", item["price"])

    updated_item = update_item(
        item_id,
        name,
        barcode,
        quantity,
        price
    )

    return jsonify(updated_item)


@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    deleted = delete_item(item_id)

    if not deleted:
        return jsonify({
            "error": "Inventory item not found"
        }), 404

    return jsonify({
        "message": "Inventory item deleted successfully"
    })


@app.route("/products/<barcode>", methods=["GET"])
def get_external_product(barcode):
    product = get_product_by_barcode(barcode)

    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify(product)


if __name__ == "__main__":
    app.run(debug=True)
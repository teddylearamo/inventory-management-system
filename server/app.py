from flask import Flask, jsonify, request

from external_api import get_product_by_barcode

app = Flask(__name__)


inventory = [
    {
        "id": 1,
        "name": "Milk",
        "barcode": "123456789",
        "quantity": 20,
        "price": 120.00
    },
    {
        "id": 2,
        "name": "Bread",
        "barcode": "987654321",
        "quantity": 15,
        "price": 80.00
    }
]


@app.route("/")
def home():
    return jsonify({
        "message": "Inventory Management API"
    })


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    item = next(
        (item for item in inventory if item["id"] == item_id),
        None
    )

    if item is None:
        return jsonify({
            "error": "Inventory item not found"
        }), 404

    return jsonify(item)


@app.route("/products/<barcode>", methods=["GET"])
def get_external_product(barcode):
    product = get_product_by_barcode(barcode)

    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify(product)


@app.route("/inventory", methods=["POST"])
def add_inventory_item():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    required_fields = ["name", "barcode", "quantity", "price"]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    new_id = max([item["id"] for item in inventory], default=0) + 1

    new_item = {
        "id": new_id,
        "name": data["name"],
        "barcode": data["barcode"],
        "quantity": data["quantity"],
        "price": data["price"]
    }

    inventory.append(new_item)

    return jsonify(new_item), 201


@app.route("/inventory/<int:item_id>", methods=["PUT"])
def update_inventory_item(item_id):
    item = next(
        (item for item in inventory if item["id"] == item_id),
        None
    )

    if item is None:
        return jsonify({
            "error": "Inventory item not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    allowed_fields = ["name", "barcode", "quantity", "price"]

    for field in allowed_fields:
        if field in data:
            item[field] = data[field]

    return jsonify(item)



if __name__ == "__main__":
    app.run(debug=True)
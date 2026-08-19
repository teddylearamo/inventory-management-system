from flask import Flask, jsonify, request

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


if __name__ == "__main__":
    app.run(debug=True)
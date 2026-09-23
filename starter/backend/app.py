from flask import Flask, request, jsonify, send_from_directory
from backend.order_tracker import OrderTracker
from backend.in_memory_storage import InMemoryStorage

app = Flask(__name__, static_folder='../frontend')
in_memory_storage = InMemoryStorage()
order_tracker = OrderTracker(in_memory_storage)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/api/orders', methods=['POST'])
def add_order_api():
    # Retrieve parsed JSON body from request
    data = request.get_json()

    # Extract the required fields and pass them into add_order
    order_tracker.add_order(data["order_id"], data["item_name"], data["quantity"], data["customer_id"], data.get("status", "pending"))

    # Serialize dictionary back into HTTP JSON response
    return jsonify(data), 201
    

@app.route('/api/orders/<string:order_id>', methods=['GET'])
def get_order_api(order_id):
    data = order_tracker.get_order_by_id(order_id)
    if data:
        return jsonify(data), 200
    elif data == None:
        return jsonify({"error": "Order not found"}), 404

@app.route('/api/orders/<string:order_id>/status', methods=['PUT'])
def update_order_status_api(order_id):
    data = request.get_json()
    order_tracker.update_order_status(order_id, data["new_status"])
    order = order_tracker.get_order_by_id(order_id)
    return jsonify(order), 200

@app.route('/api/orders', methods=['GET'])
def list_orders_api():
    orders = []
    if request.args.get('status'):
        orders = order_tracker.list_orders_by_status(request.args.get("status"))
    else:
        orders = order_tracker.list_all_orders()
    
    return jsonify(orders), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

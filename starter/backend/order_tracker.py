# This module contains the OrderTracker class, which encapsulates the core
# business logic for managing orders.

class OrderTracker:
    """
    Manages customer orders, providing functionalities to add, update,
    and retrieve order information.
    """
    def __init__(self, storage):
        required_methods = ['save_order', 'get_order', 'get_all_orders']
        for method in required_methods:
            if not hasattr(storage, method) or not callable(getattr(storage, method)):
                raise TypeError(f"Storage object must implement a callable '{method}' method.")
        self.storage = storage
        self.VALID_STATUSES = {
            "pending",
            "processing",
            "shipped"
        }

    def add_order(self, order_id: str, item_name: str, quantity: int, customer_id: str, status: str = "pending"):

        # Checks that makes the tests pass
        # Checking inputs first saves an unnecessary storage read operation
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid Status: {status}")

        if not order_id.strip() or not item_name.strip() or not customer_id.strip():
            raise ValueError("Required fields cannot be empty")
        
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantitty must be a positive integer")

        if self.storage.get_order(order_id):
            raise ValueError("Order ID already exists")
        
        

        self.storage.save_order(order_id, {
            "order_id": order_id,
            "item_name": item_name,
            "quantity": quantity,
            "customer_id": customer_id,
            "status": status
        })

    def get_order_by_id(self, order_id: str):

        if not order_id.strip():
            raise ValueError("Order ID cannot be empty")

        # Fetch the order from storage and return it
        return self.storage.get_order(order_id)

    def update_order_status(self, order_id: str, new_status: str):

        if not order_id.strip():
            raise ValueError("Order ID cannot be empty")

        if new_status not in self.VALID_STATUSES:
            raise ValueError("Not a valid status")

        order = self.storage.get_order(order_id)

        if order == None:
            raise ValueError("Order does not exist")

        order["status"] = new_status

        return self.storage.save_order(order_id, order)

    def list_all_orders(self):
        orders_dict = self.storage.get_all_orders()
        orders = list(orders_dict.values())
        
        return orders

    def list_orders_by_status(self, status: str):
        pass

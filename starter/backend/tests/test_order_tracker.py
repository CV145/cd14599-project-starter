import pytest
from unittest.mock import Mock
from ..order_tracker import OrderTracker

# --- Fixtures for Unit Tests ---

@pytest.fixture
def mock_storage():
    """
    Provides a mock storage object for tests.
    This mock will be configured to simulate various storage behaviors.
    """
    mock = Mock()
    # By default, mock get_order to return None (no order found)
    mock.get_order.return_value = None
    # By default, mock get_all_orders to return an empty dict
    mock.get_all_orders.return_value = {}
    return mock

@pytest.fixture
def order_tracker(mock_storage):
    """
    Provides an OrderTracker instance initialized with the mock_storage.
    """
    return OrderTracker(mock_storage)

#
# --- TODO: add test functions below this line ---
#

# pytest automatically passes in an instance of order_tracker and mock_storage
def test_add_order_success(order_tracker, mock_storage):
    """
    This method should add a new order, making sure it has valid fields and that no duplicate IDs are allowed.
    Consider when testing: default vs. explicit status; duplicate IDs; invalid quantity; missing required fields; invalid initial status
    """
    order_tracker.add_order("0RD001", "Laptop", 1, "CUST001")

    # Expects save_order to be called once to pass
    mock_storage.save_order.assert_called_once()


def test_add_order_raises_error_if_exists(order_tracker, mock_storage):

    mock_storage.get_order.return_value = {
        "order_id": "ORD_EXISTING"
    }

    with pytest.raises(ValueError):
        order_tracker.add_order("ORD_EXISTING", "Laptop", 1, "CUST001")

def test_add_order_with_explicit_status(order_tracker, mock_storage):
    order_tracker.add_order("ORD_SHIPPED", "Laptop", 1, "CUST001", "shipped")
    mock_storage.save_order.assert_called_once_with(
    "ORD_SHIPPED",
    {
        "order_id": "ORD_SHIPPED",
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST001",
        "status": "shipped",
    }
)

def test_add_order_invalid_status(order_tracker):
    with pytest.raises(ValueError):
        order_tracker.add_order("ORD_SHIPPED", "Laptop", 1, "CUST001", "bogus")


def test_add_order_invalid_quantity(order_tracker):
    with pytest.raises(ValueError):
        order_tracker.add_order("ORD_SHIPPED", "Laptop", -1, "CUST001", "pending")

def test_add_order_empty_order_id(order_tracker):
    with pytest.raises(ValueError):
        order_tracker.add_order("", "Laptop", 1, "CUST001", "pending")

def test_get_order_by_id_success(order_tracker, mock_storage):
    mock_storage.get_order.return_value = {
        "order_id": "ORD_SHIPPED",
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST001",
        "status": "shipped",
    }

    result = order_tracker.get_order_by_id("ORD001")

    assert result == mock_storage.get_order.return_value

    mock_storage.get_order.assert_called_once_with("ORD001")

def test_get_order_by_id_not_found(order_tracker, mock_storage):
    mock_storage.get_order.return_value = None
    result = order_tracker.get_order_by_id("NONEXISTENT")
    assert result is None
    mock_storage.get_order.assert_called_once_with("NONEXISTENT")


def test_get_order_by_id_empty_id(order_tracker):
    with pytest.raises(ValueError):
        order_tracker.get_order_by_id("")

def test_update_order_status_invalid_status(order_tracker, mock_storage):
    with pytest.raises(ValueError):
        order_tracker.update_order_status("ORD001", "nonexistent_status")
    mock_storage.get_order.assert_not_called()


def test_update_order_status_empty_id(order_tracker, mock_storage):
    with pytest.raises(ValueError):
        order_tracker.update_order_status("", "shipped")
    
    mock_storage.get_order.assert_not_called()

# Validating an order exists
def test_update_order_status_order_not_found(order_tracker, mock_storage):

    mock_storage.get_order.return_value = None

    with pytest.raises(ValueError):
        order_tracker.update_order_status("ORD999", "shipped")

    mock_storage.get_order.assert_called_once_with("ORD999")

    mock_storage.save_order.assert_not_called()

def test_update_order_status_success(order_tracker, mock_storage):
    
    # Arrange
    initial_order = {
    "order_id": "ORD001",
    "item_name": "Laptop",
    "quantity": 1,
    "customer_id": "CUST001",
    "status": "pending"
    }
    mock_storage.get_order.return_value = initial_order

    # Act
    order_tracker.update_order_status("ORD001", "shipped")

    # Assert
    expected_order = initial_order.copy()
    expected_order["status"] = "shipped"
    mock_storage.save_order.assert_called_once_with(initial_order["order_id"], expected_order)


def test_list_all_orders_no_orders(order_tracker, mock_storage):
    # Arrange - clean, empty storage state
    mock_storage.get_all_orders.return_value = {}

    # Act
    orders = order_tracker.list_all_orders()

    # Assert
    mock_storage.get_all_orders.assert_called_once()
    assert orders == []

def test_list_all_orders_multiple_orders(order_tracker, mock_storage):
    # Arrange
    mock_storage.get_all_orders.return_value = {
        "ORD001": {
            "order_id": "ORD001",
            "item_name": "Laptop",
            "quantity": 1,
            "customer_id": "CUST001",
            "status": "pending"
        },
        "ORD002": {
            "order_id": "ORD002",
            "item_name": "Laptop",
            "quantity": 5,
            "customer_id": "CUST001",
            "status": "pending"
        }
    }

    # Act
    orders = order_tracker.list_all_orders()

    # Assert
    mock_storage.get_all_orders.assert_called_once()
    assert len(orders) == len(mock_storage.get_all_orders.return_value)
    for order in orders:
        assert order == mock_storage.get_all_orders.return_value[order["order_id"]]


def test_list_orders_by_status_empty_status(order_tracker):
    with pytest.raises(ValueError):
        order_tracker.list_orders_by_status("")

def test_list_orders_by_status_whitespace_status(order_tracker):
    with pytest.raises(ValueError):
        order_tracker.list_orders_by_status(" ")

def test_list_orders_by_status_invalid_status(order_tracker):
     with pytest.raises(ValueError):
        order_tracker.list_orders_by_status("bogus")

def test_list_orders_by_status_empty_storage(order_tracker, mock_storage):
    # Arrange
    mock_storage.get_all_orders.return_value = {}

    # Act
    orders = order_tracker.list_orders_by_status("pending")

    # Assert
    mock_storage.get_all_orders.assert_called_once()
    assert orders == []


def test_list_orders_by_status_none_match(order_tracker, mock_storage):
    # Arrange - configure the state of the system
    mock_storage.get_all_orders.return_value = {
        "ORD001": {
            "order_id": "ORD001",
            "item_name": "Laptop",
            "quantity": 1,
            "customer_id": "CUST001",
            "status": "shipped"
        },
        "ORD002": {
            "order_id": "ORD002",
            "item_name": "Laptop",
            "quantity": 5,
            "customer_id": "CUST001",
            "status": "shipped"
        }
    }

    # Act - call the function
    orders = order_tracker.list_orders_by_status("pending")

    # Assert - because none match, result should be []
    mock_storage.get_all_orders.assert_called_once()
    assert orders == []



def test_list_orders_by_status_some_match(order_tracker, mock_storage):
    # Arrange - configure the state of the system
    mock_storage.get_all_orders.return_value = {
        "ORD001": {
            "order_id": "ORD001",
            "item_name": "Laptop",
            "quantity": 1,
            "customer_id": "CUST001",
            "status": "shipped"
        },
        "ORD002": {
            "order_id": "ORD002",
            "item_name": "Laptop",
            "quantity": 5,
            "customer_id": "CUST001",
            "status": "shipped"
        },
        "ORD003": {
            "order_id": "ORD003",
            "item_name": "Laptop",
            "quantity": 5,
            "customer_id": "CUST001",
            "status": "pending"
        }
    }

     # Act - call the function
    orders = order_tracker.list_orders_by_status("shipped")

    # Assert
    mock_storage.get_all_orders.assert_called_once()
    assert len(orders) == 2
    for order in orders:
        assert order["status"] == "shipped"
    

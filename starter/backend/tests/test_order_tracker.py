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
    mock.get_order.return_value = {
        "order_id": "ORD_EXISTING"
    }
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


def test_add_order_raises_error_if_exists():
    with pytest.raises(ValueError):
        order_tracker.add_order("0RD001", "Laptop", 1, "CUST001")

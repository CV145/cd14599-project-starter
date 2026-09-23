# Udatracker Starter Code

REFLECTION:
- In list_orders_by_status I called self.list_all_orders() to retrieve the orders before filtering, reusing tested code. In add_order_api, I handled default values with .get() for optional status parameter.
- One failed test revealed that add_order_api did not pass status to OrderTracker resulting in both orders defaulting to "pending". The API test caught a subtle bug that the unit tests couldn't see in isolation.
- I would definitely implement a DELETE endpoint or integrate a schema library.

```
.
├── backend
│   ├── __init__.py
│   ├── app.py
│   ├── in_memory_storage.py
│   ├── order_tracker.py
│   ├── requirements.txt
│   └── tests
│       ├── __init__.py
│       ├── test_api.py
│       └── test_order_tracker.py
├── frontend
│   ├── css
│   │   └── style.css
│   ├── index.html
│   └── js
│       └── script.js
├── pytest.ini
└── README.md
```

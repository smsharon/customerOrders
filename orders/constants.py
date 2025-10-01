"""
Constants used throughout the application.
These define standardized states, actions, and statuses for Orders, Transactions, and Inventory.
"""

# Order states
ORDER_STATES = {
    "DRAFT": "Draft",
    "PLACED": "Placed",
    "FULFILLED": "Fulfilled",
    "CANCELLED": "Cancelled",
}

# Transaction actions
TRANSACTION_ACTIONS = {
    "CREATE_ORDER": "Order created",
    "SUBMIT_ORDER": "Order submitted",
    "FULFILL_ORDER": "Order fulfilled",
    "CANCEL_ORDER": "Order cancelled",
    "UPDATE_ORDER": "Order updated",
    "CUSTOMER_REGISTERED": "Customer registered",
}

# Inventory statuses
INVENTORY_STATUS = {
    "AVAILABLE": "Available",
    "FEW_REMAINING": "Few remaining",
    "OUT_OF_STOCK": "Out of stock",
}

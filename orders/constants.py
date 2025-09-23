"""
Constants used throughout the application.
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
    "AVAILABLE": "AVAILABLE",
    "FEW_REMAINING": "FEW REMAINING",
    "OUT_OF_STOCK": "OUT OF STOCK",
}

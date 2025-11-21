# data.py

# Synthetic Order Data
orders_db = {
    "ORD-101": {"status": "Shipped", "delivery_date": "2025-11-25", "items": ["Wireless Headphones"]},
    "ORD-102": {"status": "Processing", "delivery_date": "TBD", "items": ["Gaming Mouse", "Keyboard"]},
    "ORD-103": {"status": "Delivered", "delivery_date": "2025-11-20", "items": ["Monitor stand"]}
}

# Company Policies
policy_db = """
1. Return Policy: You can return any item within 30 days of receipt for a full refund. Items must be unused.
2. Shipping: We offer free shipping on orders over $50. Standard shipping takes 10 business days.
3. Support Hours: Our human agents are available 9 AM - 5 PM EST, Mon-Fri.
"""

def get_order_info(order_id):
    """Simulates a database lookup"""
    return orders_db.get(order_id.upper())
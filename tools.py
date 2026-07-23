def get_order_status(order_id : str):
    orders = {
        "12345": "Shipped - arriving tomorrow",
        "99999": "Delayed in transit",
        "00000": "Cancelled and refunded"
    }
    if order_id in orders:
        return orders[order_id]
    else:
        return "order not found."
    
def search_kb(query : str):
    database = {
        "router": "Restart the router by unplugging it for 30 seconds.",
        "screen": "Screen replacements cost 500rs and take 2 business days."
    }
    query_lower = query.lower()
    for i in database:
        if i in query_lower:
            return database[i]
    else:
        return "No relevant Documentation found."
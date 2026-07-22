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
    

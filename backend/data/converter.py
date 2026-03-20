# backend/data/converter.py
import csv
import json

def convert_and_split():
    csv_file = 'backend/data/food_delivery.csv'
    orders = []
    items = []

    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Create order object
            order_entry = {
                "order_id": row['order_id'],
                "restaurant_id": int(row['restaurant_id']),
                "customer_id": row['customer_id'],
                "order_time": row['order_time'],
                "delivery_time": row['delivery_time'],
                "delivery_distance": float(row['delivery_distance']),
                "order_value": float(row['order_value']),
                "delivery_method": row['delivery_method'],
                "route_efficiency": float(row['route_efficiency'])
            }
            orders.append(order_entry)

            # Create item object
            item_entry = {
                "order_id": row['order_id'],
                "food_item": row['food_item'],
                "food_temperature": row['food_temperature'],
                "food_freshness": int(row['food_freshness']),
                "packaging_quality": int(row['packaging_quality']),
                "food_condition": row['food_condition']
            }
            items.append(item_entry)
    
    # Save to order.json
    with open('orders.json', 'w') as f:
        json.dump(orders, f, indent=4)
    
    # Save to items.json
    with open('items.json', 'w') as f:
        json.dump(items, f, indent=4)
    
    print("Success")

if __name__ == "__main__":
    convert_and_split()

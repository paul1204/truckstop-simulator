import requests
import random
import time

from app.merchandise.order.inventory_readings import get_bottled_beverages, get_packaged_food
from config import NUM_SALES_SIMULATIONS

def simulate_pos_sales():
    print('----')
    bottled_beverages = get_bottled_beverages()
    packaged_food = get_packaged_food()
    print(f"Inventory Loaded: {len(bottled_beverages)} beverages, {len(packaged_food)} food items.")
    print(bottled_beverages)
    print(packaged_food)
    print('----')

    all_menu_items = bottled_beverages + packaged_food
    if not all_menu_items:
        print("No menu items available.")
        return
    for _ in range(NUM_SALES_SIMULATIONS):
        num_items = random.randint(1, min(5, len(all_menu_items)))
        selected_items = random.sample(all_menu_items, num_items)
        sales_items = [
            {
                "itemName": item["name"],
                "quantity": 1.0,
                "unitPrice": item["costOfGoods"],
                "salesType": item["salesType"],
                "skuCode": item["skuCode"]
            }
            for item in selected_items
        ]
        total_sales_amount = sum(item["quantity"] * item["unitPrice"] for item in sales_items)
        sales_data = {
            "totalSalesAmount": round(total_sales_amount, 2),
            "salesItems": sales_items
        }
        print("Generated sales_data:")
        print(sales_data)

        url = "http://localhost:8080/pos-ingest/sales"
        response = requests.post(url, json=sales_data)
        print(f"Sales ingest response status: {response.status_code}")
        print(response.text)
        time.sleep(1)

#    sales_data = {
#      "totalSalesAmount": 12.85,
#      "salesItems": [
#        {
#          "itemName": "Cola Reserve",
#          "quantity": 2.0,
#          "unitPrice": 4.15,
#          "salesType": "BOTTLED_BEVERAGE",
#          "skuCode": 4000
#        },
#        {
#          "itemName": "Beef Jerky",
#          "quantity": 1.0,
#          "unitPrice": 4.55,
#          "salesType": "PACKAGED_FOOD",
#          "skuCode": 4010
#        }
#      ]
#    }


if __name__ == "__main__":
    simulate_pos_sales()
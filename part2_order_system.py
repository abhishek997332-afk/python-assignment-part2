# ===============================
# Restaurant Order Management System
# ===============================

# ----------- PROVIDED DATA ------------

menu = {
    "Paneer Tikka":   {"category": "Starters",  "price": 180.0, "available": True},
    "Chicken Wings":  {"category": "Starters",  "price": 220.0, "available": False},
    "Veg Soup":       {"category": "Starters",  "price": 120.0, "available": True},
    "Butter Chicken": {"category": "Mains",     "price": 320.0, "available": True},
    "Dal Tadka":      {"category": "Mains",     "price": 180.0, "available": True},
    "Veg Biryani":    {"category": "Mains",     "price": 250.0, "available": True},
    "Garlic Naan":    {"category": "Mains",     "price":  40.0, "available": True},
    "Gulab Jamun":    {"category": "Desserts",  "price":  90.0, "available": True},
    "Rasgulla":       {"category": "Desserts",  "price":  80.0, "available": True},
    "Ice Cream":      {"category": "Desserts",  "price": 110.0, "available": False},
}

inventory = {
    "Paneer Tikka":   {"stock": 10, "reorder_level": 3},
    "Chicken Wings":  {"stock":  8, "reorder_level": 2},
    "Veg Soup":       {"stock": 15, "reorder_level": 5},
    "Butter Chicken": {"stock": 12, "reorder_level": 4},
    "Dal Tadka":      {"stock": 20, "reorder_level": 5},
    "Veg Biryani":    {"stock":  6, "reorder_level": 3},
    "Garlic Naan":    {"stock": 30, "reorder_level": 10},
    "Gulab Jamun":    {"stock":  5, "reorder_level": 2},
    "Rasgulla":       {"stock":  4, "reorder_level": 3},
    "Ice Cream":      {"stock":  7, "reorder_level": 4},
}

sales_log = {
    "2025-01-01": [
        {"order_id": 1,  "items": ["Paneer Tikka", "Garlic Naan"],          "total": 220.0},
        {"order_id": 2,  "items": ["Gulab Jamun", "Veg Soup"],              "total": 210.0},
        {"order_id": 3,  "items": ["Butter Chicken", "Garlic Naan"],        "total": 360.0},
    ],
    "2025-01-02": [
        {"order_id": 4,  "items": ["Dal Tadka", "Garlic Naan"],             "total": 220.0},
        {"order_id": 5,  "items": ["Veg Biryani", "Gulab Jamun"],           "total": 340.0},
    ],
    "2025-01-03": [
        {"order_id": 6,  "items": ["Paneer Tikka", "Rasgulla"],             "total": 260.0},
        {"order_id": 7,  "items": ["Butter Chicken", "Veg Biryani"],        "total": 570.0},
        {"order_id": 8,  "items": ["Garlic Naan", "Gulab Jamun"],           "total": 130.0},
    ],
    "2025-01-04": [
        {"order_id": 9,  "items": ["Dal Tadka", "Garlic Naan", "Rasgulla"], "total": 300.0},
        {"order_id": 10, "items": ["Paneer Tikka", "Gulab Jamun"],          "total": 270.0},
    ],
}

# ----------- TASK 1 ------------

print("\n===== MENU =====\n")

categories = set()
for item in menu:
    categories.add(menu[item]["category"])

for cat in categories:
    print(f"===== {cat} =====")
    for item, details in menu.items():
        if details["category"] == cat:
            status = "Available" if details["available"] else "Unavailable"
            print(f"{item:15} ₹{details['price']:.2f}   [{status}]")
    print()

print("Total items:", len(menu))

avail = sum(1 for item in menu if menu[item]["available"])
print("Available items:", avail)

max_item = max(menu, key=lambda x: menu[x]["price"])
print("Most expensive:", max_item, menu[max_item]["price"])

print("\nItems under ₹150:")
for item in menu:
    if menu[item]["price"] < 150:
        print(item, menu[item]["price"])

# ----------- TASK 2 ------------

print("\n===== CART =====")

cart = []

def add_item(name, qty):
    if name not in menu:
        print("Item not found:", name)
        return
    if not menu[name]["available"]:
        print("Item unavailable:", name)
        return

    for c in cart:
        if c["item"] == name:
            c["quantity"] += qty
            print("Updated quantity for", name)
            return

    cart.append({"item": name, "quantity": qty, "price": menu[name]["price"]})
    print("Added", name)

def remove_item(name):
    for c in cart:
        if c["item"] == name:
            cart.remove(c)
            print("Removed", name)
            return
    print("Item not in cart")

# simulation
add_item("Paneer Tikka", 2)
add_item("Gulab Jamun", 1)
add_item("Paneer Tikka", 1)
add_item("Mystery Burger", 1)
add_item("Chicken Wings", 1)
remove_item("Gulab Jamun")

# summary
print("\n========== Order Summary ==========")
subtotal = 0

for c in cart:
    total = c["quantity"] * c["price"]
    subtotal += total
    print(f"{c['item']:15} x{c['quantity']}   ₹{total:.2f}")

gst = subtotal * 0.05
total_pay = subtotal + gst

print("----------------------------------")
print("Subtotal:", subtotal)
print("GST:", round(gst, 2))
print("Total Payable:", round(total_pay, 2))

# ----------- TASK 3 ------------

import copy

inventory_backup = copy.deepcopy(inventory)

# change to show deep copy
inventory["Paneer Tikka"]["stock"] = 5
print("\nCheck Deep Copy:")
print("Current:", inventory["Paneer Tikka"])
print("Backup :", inventory_backup["Paneer Tikka"])

# restore
inventory["Paneer Tikka"]["stock"] = inventory_backup["Paneer Tikka"]["stock"]

# deduct stock
for c in cart:
    item = c["item"]
    qty = c["quantity"]

    if inventory[item]["stock"] >= qty:
        inventory[item]["stock"] -= qty
    else:
        print("Low stock:", item)
        inventory[item]["stock"] = 0

# reorder alerts
print("\nReorder Alerts:")
for item in inventory:
    if inventory[item]["stock"] <= inventory[item]["reorder_level"]:
        print(f"⚠ {item} — Only {inventory[item]['stock']} left")

# ----------- TASK 4 ------------

print("\n===== SALES =====")

# revenue per day
day_sales = {}

for date in sales_log:
    total = sum(order["total"] for order in sales_log[date])
    day_sales[date] = total
    print(date, "->", total)

best_day = max(day_sales, key=day_sales.get)
print("Best day:", best_day, day_sales[best_day])

# most ordered item
item_count = {}

for date in sales_log:
    for order in sales_log[date]:
        for item in order["items"]:
            item_count[item] = item_count.get(item, 0) + 1

most_item = max(item_count, key=item_count.get)
print("Most ordered item:", most_item)

# add new day
sales_log["2025-01-05"] = [
    {"order_id": 11, "items": ["Butter Chicken", "Gulab Jamun", "Garlic Naan"], "total": 490.0},
    {"order_id": 12, "items": ["Paneer Tikka", "Rasgulla"], "total": 260.0},
]

print("\nUpdated Sales:")
for date in sales_log:
    total = sum(order["total"] for order in sales_log[date])
    print(date, "->", total)

# numbered orders
print("\nAll Orders:\n")

count = 1
for date in sales_log:
    for order in sales_log[date]:
        items = ", ".join(order["items"])
        print(f"{count}. [{date}] Order #{order['order_id']} — ₹{order['total']} — Items: {items}")
        count += 1

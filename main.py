from database import (
    create_tables,
    add_product,
    get_all_products,
    update_product,
    delete_product,
    add_customer,
    create_sale,
    add_sale_item,
    get_product_by_id
)

def add_product_menu():
    name = input("Enter product name: ")
    price = float(input("Enter price: "))
    quantity = int(input("Enter quantity: "))
    add_product(name, price, quantity)
    print("✅ Product added successfully\n")

from datetime import datetime

def billing_menu():
    print("\n--- Create New Bill ---")
    customer_name = input("Customer name: ")
    phone = input("Phone number: ")

    customer_id = add_customer(customer_name, phone)

    total_amount = 0
    sale_items = []

    while True:
        view_products_menu()
        product_id = int(input("Enter product ID (0 to finish): "))

        if product_id == 0:
            break

        product = get_product_by_id(product_id)

        if not product:
            print("❌ Invalid product ID\n")
            continue

        quantity = int(input("Enter quantity: "))

        if quantity > product[3]:
            print("❌ Not enough stock\n")
            continue

        price = product[2]
        total_amount += price * quantity
        sale_items.append((product_id, quantity, price))

    sale_id = create_sale(
        customer_id,
        total_amount,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    for item in sale_items:
        add_sale_item(sale_id, item[0], item[1], item[2])

    print(f"\n✅ Bill created successfully")
    print(f"Total Amount: ₹{total_amount}\n")


def view_products_menu():
    products = get_all_products()
    if not products:
        print("No products found.\n")
        return

    print("\n--- Product List ---")
    for p in products:
        print(f"ID: {p[0]} | Name: {p[1]} | Price: {p[2]} | Qty: {p[3]}")
    print()


def update_product_menu():
    product_id = int(input("Enter product ID to update: "))
    name = input("Enter new name: ")
    price = float(input("Enter new price: "))
    quantity = int(input("Enter new quantity: "))

    update_product(product_id, name, price, quantity)
    print("✅ Product updated successfully\n")


def delete_product_menu():
    product_id = int(input("Enter product ID to delete: "))
    delete_product(product_id)
    print("🗑️ Product deleted successfully\n")


def main():
    create_tables()

    while True:
        print("===== SHOP BILLING SYSTEM =====")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Create Bill")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_product_menu()

        elif choice == "2":
            view_products_menu()

        elif choice == "3":
            update_product_menu()

        elif choice == "4":
            delete_product_menu()

        elif choice == "5":
            billing_menu()

        elif choice == "6":
            print("Exiting... 👋")
            break

        else:
            print("❌ Invalid choice. Try again.\n")
if __name__ == "__main__":
    main()

import mysql.connector
import DataBase_Uti as db

#run this code once to add test data to the data base to check the system functions

def insert_demo_data():
    conn = db.connect_db()
    cursor = conn.cursor()

    try:
        cursor.executemany('''
            INSERT INTO Categories (CName) VALUES (%s)
        ''', [
            ('Drinks',),
            ('Food',),
            ('Electronics',)
        ])

        cursor.executemany('''
            INSERT INTO Suppliers (SName, Phone, CategoryID) VALUES (%s, %s, %s)
        ''', [
            ('Pepsi Co', '0101111111', 1),
            ('Almarai', '0102222222', 2),
            ('Samsung Store', '0103333333', 3)
        ])

        products_data = [
            ('Pepsi Can', 15.00, 10.00, 100, 1, 1),  # ID=1
            ('Mineral Water', 5.00, 2.50, 200, 1, 1),  # ID=2
            ('Family Chips', 25.00, 18.00, 50, 2, 2),  # ID=3
            ('Natural Yogurt', 8.00, 5.00, 30, 2, 2),  # ID=4
            ('Wireless Mouse', 150.00, 90.00, 10, 3, 3),  # ID=5
            ('Flash Drive 64GB', 200.00, 120.00, 15, 3, 3)  # ID=6
        ]
        cursor.executemany('''
            INSERT INTO Products (PName, Price, Cost, Quantity, CategoryID, SupplierID) 
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', products_data)

        cursor.executemany('''
            INSERT INTO Customers (CName, Phone, Address) VALUES (%s, %s, %s)
        ''', [
            ('Ahmed Mohamed', '0123456789', 'Cairo - Downtown'),  # ID=1
            ('Sarah Ali', '0112345678', 'Giza - Dokki'),  # ID=2
            ('Walk-in Customer', '0000000000', 'Unknown')  # ID=3
        ])

        bills_data = [
            ('Cashier1', 1, 45.00, '2023-10-01 10:30:00'),  # BillID=1
            ('Cashier1', 2, 350.00, '2023-10-02 14:00:00')  # BillID=2
        ]
        cursor.executemany('''
            INSERT INTO Bills (CashierName, CustomerID, TotalAmount, BillDateTime) 
            VALUES (%s, %s, %s, %s)
        ''', bills_data)

        bill_items = [
            (1, 1, 3, 15.00),
            (2, 5, 1, 150.00),
            (2, 6, 1, 200.00)
        ]
        cursor.executemany('''
            INSERT INTO Bill_Product (BillID, ProductID, Quantity, PriceAtSale) 
            VALUES (%s, %s, %s, %s)
        ''', bill_items)

        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()
insert_demo_data()
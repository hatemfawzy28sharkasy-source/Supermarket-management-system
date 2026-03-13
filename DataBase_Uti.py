import mysql.connector


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="supermarket"
    )

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Categories
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Categories (
        CategoryID INT AUTO_INCREMENT PRIMARY KEY,
        CName VARCHAR(255) NOT NULL UNIQUE
    )
    ''')

    # Suppliers
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Suppliers (
        SupplierID INT AUTO_INCREMENT PRIMARY KEY,
        SName VARCHAR(255) NOT NULL UNIQUE,
        Phone VARCHAR(15),
        CategoryID INT,
        FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID) ON DELETE CASCADE
    )
    ''')

    # Products
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        ProductID INT AUTO_INCREMENT PRIMARY KEY,
        PName VARCHAR(255) NOT NULL UNIQUE,
        Price DECIMAL(5, 2) NOT NULL,
        Cost DECIMAL(5, 2) NOT NULL,
        Quantity INT NOT NULL,
        CategoryID INT,
        SupplierID INT,
        FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID) ON DELETE CASCADE,
        FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID) ON DELETE CASCADE
    )
    ''')

    # Customers
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        CustomerID INT AUTO_INCREMENT PRIMARY KEY,
        CName VARCHAR(255) NOT NULL UNIQUE,
        Phone VARCHAR(15),
        Address VARCHAR(255)
    )
    ''')

    # Bills
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Bills (
        BillID INT AUTO_INCREMENT PRIMARY KEY,
        CashierName VARCHAR(255) NOT NULL,
        CustomerID INT,
        TotalAmount DECIMAL(10, 2) NOT NULL,
        BillDateTime DATETIME NOT NULL,
        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE CASCADE
    )
    ''')

    # Bill_Product
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Bill_Product (
        BillID INT,
        ProductID INT,
        Quantity INT NOT NULL,
        PriceAtSale DECIMAL(5, 2) NOT NULL,
        PRIMARY KEY (BillID, ProductID),
        FOREIGN KEY (BillID) REFERENCES Bills(BillID) ON DELETE CASCADE, 
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID) ON DELETE CASCADE
    )
    ''')

    conn.commit()
    conn.close()
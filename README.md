# Supermarket Management System

## Overview

The **Supermarket Management System** is a desktop application developed using **Python (Tkinter)** and **MySQL**.
It is designed to help manage supermarket operations such as product inventory, suppliers, customers, and sales billing through a simple graphical user interface.

The system allows users to add products, create bills, manage customers, and track sales while automatically updating product stock.

---

# Features

## 1. Product Management

The system allows users to manage products in the supermarket inventory.

Users can:

* Add new products
* Edit existing products
* Delete products
* View all products in a table

Each product contains:

* Product Name
* Selling Price
* Cost Price
* Quantity
* Category
* Supplier

---

## 2. Category Management

Categories help organize products in the system.

Users can:

* Add new categories
* Edit existing categories
* Delete categories

---

## 3. Supplier Management

Suppliers can be added and linked to specific categories.

Users can:

* Add suppliers
* Edit supplier information
* Delete suppliers
* Assign suppliers to product categories

---

## 4. Customer Management

The system stores customer information used in billing.

Users can:

* Add customers
* Edit customer information
* Delete customers

Customer information includes:

* Name
* Phone Number
* Address

---

## 5. Bill Creation

The system allows the cashier to create sales bills.

Users can:

* Select a customer
* Add multiple products to a bill
* Specify product quantity
* Automatically calculate the total price

---

## 6. Automatic Stock Update

When a bill is completed:

* The system automatically deducts the sold quantity from the product stock.

---

## 7. View All Bills

Users can view a list of all created bills including:

* Bill ID
* Cashier Name
* Customer Name
* Total Amount
* Bill Date and Time

---

## 8. Bill Details and Profit Calculation

Each bill can display detailed information including:

* Products included in the bill
* Quantity of each product
* Price at the time of sale
* Total profit from the bill

---

# Technologies Used

* **Python**
* **Tkinter** (GUI)
* **MySQL**
* **mysql-connector-python**

---

# Database Structure

The system uses the following tables:

* Products
* Categories
* Suppliers
* Customers
* Bills
* Bill_Product

These tables store product information, customer data, and bill transactions.

---

# How to Run the Project

1. Install Python (3.x)

2. Install required library

```bash
pip install mysql-connector-python
```

3. Create a MySQL database.

4. Update database connection settings in the `DataBase_Uti` file.

5. Run the project

```bash
python main.py
```

---

# Main System Modules

The application contains three main modules:

### Product Management

Used to manage products, categories, and suppliers.

### Create New Bill

Used to create customer bills and process sales.

### All Bills

Displays all sales records and bill details.

---

# Project Purpose

This project was developed as a **learning project** to demonstrate:

* Database integration with Python
* GUI development using Tkinter
* CRUD operations
* Inventory and billing system design


import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector
import DataBase_Uti as db


# --- Product Management Window ---
def manage_products_window():
    win = tk.Toplevel(root)
    win.title("Product Management")
    win.geometry("900x500")

    # --- Frame for Adding/Editing a Product ---
    frame_form = tk.LabelFrame(win, text="Product Details", bg="#5B5A64")
    frame_form.pack(pady=10, padx=10, fill="x")

    # Input fields
    tk.Label(frame_form, text="Product Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_name = tk.Entry(frame_form)
    entry_name.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_form, text="Selling Price:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    entry_selling_price = tk.Entry(frame_form)
    entry_selling_price.grid(row=1, column=3, padx=5, pady=5)

    tk.Label(frame_form, text="Cost Price:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_cost_price = tk.Entry(frame_form)
    entry_cost_price.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_form, text="Quantity:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_quantity = tk.Entry(frame_form)
    entry_quantity.grid(row=0, column=3, padx=5, pady=5)

    # Dropdowns for Category and Supplier
    tk.Label(frame_form, text="Category:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
    combo_category = ttk.Combobox(frame_form, state="readonly")
    combo_category.grid(row=0, column=5, padx=5, pady=5)

    tk.Label(frame_form, text="Supplier:").grid(row=1, column=4, padx=5, pady=5, sticky="w")
    combo_supplier = ttk.Combobox(frame_form, state="readonly")
    combo_supplier.grid(row=1, column=5, padx=5, pady=5)


    def populate_comboboxes():
        conn = db.connect_db()
        cursor = conn.cursor()
        # ----------- Categories Combobox -----------
        cursor.execute("SELECT SName FROM Suppliers")
        suppliers = [sup[0] for sup in cursor.fetchall()]
        suppliers.insert(0, "")
        combo_supplier['values'] = suppliers

        cursor.execute("SELECT CName FROM Categories")
        categories = [cat[0] for cat in cursor.fetchall()]
        combo_category['values'] = categories
        conn.close()
        update_cat()
        # ----------- Suppliers Combobox -----------

    def update_cat(event=None):
        Selceted = combo_supplier.get()
        conn = db.connect_db()
        cursor = conn.cursor()

        if Selceted == "":
            cursor.execute("SELECT CName FROM Categories")
            categories = [cat[0] for cat in cursor.fetchall()]
            combo_category['values'] = categories
            conn.close()
            return

        cursor.execute("""
               SELECT C.CName
               FROM Categories C
               JOIN Suppliers S ON S.CategoryID = C.CategoryID
               WHERE S.SName= %s
               """, (Selceted,))

        categories = [cat[0] for cat in cursor.fetchall()]
        combo_category['values'] = categories
        combo_category.set("")

        conn.close()
    combo_supplier.bind("<<ComboboxSelected>>", update_cat)

    def supmanag(act):
        if act == "Edit":
            if combo_supplier.get() == "":
                return

        sup_win = tk.Toplevel(win)
        sup_win.title(f"{act} Supplier")
        sup_win.geometry("300x150")

        supframe = tk.Frame(sup_win)
        supframe.pack(pady=10)

        tk.Label(supframe, text="Supplier Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entrysupadd = tk.Entry(supframe)
        entrysupadd.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(supframe, text="categories:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        comb_supadd = ttk.Combobox(supframe, state="readonly")
        comb_supadd.grid(row=1, column=1, padx=5, pady=5)

        conn = db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT CName FROM Categories")
        cats = [c[0] for c in cursor.fetchall()]
        comb_supadd['values'] = cats

        if act == "Edit":
            current_name = combo_supplier.get()
            cursor.execute("""
                   SELECT c.CName 
                   FROM Categories c
                   JOIN Suppliers s ON c.CategoryID = s.CategoryID 
                   WHERE s.SName = %s
                   """, (current_name,))
            cat_row = cursor.fetchone()
            comb_supadd.set(cat_row[0])
            entrysupadd.insert(0, current_name)

        conn.close()
        supbtn = tk.Button(supframe, text=f"{act} Supplier",
                           command=lambda: sup_add_btn(comb_supadd, entrysupadd, sup_win, act))
        supbtn.grid(row=2, column=0, columnspan=2, pady=15)

    def sup_add_btn(comb_supadd,entrysupadd,window,act):
        cat_select= comb_supadd.get()
        name_select=entrysupadd.get()

        if not cat_select or not name_select:
            return

        conn = db.connect_db()
        cursor = conn.cursor()

        try:
            if act=="Edit":
                old_name = combo_supplier.get()
                cursor.execute("""
                    UPDATE Suppliers
                    SET SName = %s, 
                        CategoryID = (SELECT CategoryID FROM Categories WHERE CName = %s)
                    WHERE SName = %s
                """, (name_select, cat_select, old_name))
            else:
                cursor.execute("""
                    INSERT INTO Suppliers (SName, CategoryID)
                    VALUES (%s , (SELECT CategoryID FROM Categories WHERE CName = %s))
                """, (name_select, cat_select))
        except mysql.connector.Error:
            messagebox.showerror("Error", "Name already exists!",parent=win)
        finally:
            conn.commit()
            conn.close()
            populate_comboboxes()
            populate_treeview()
            combo_supplier.set(name_select)
            window.destroy()

    def add_cat():
        new = simpledialog.askstring("Add", "Enter Category name:")

        if not new:
            return

        conn = db.connect_db()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO Categories (CName) VALUES (%s)", (new,))
        except mysql.connector.Error:
            messagebox.showerror("Error", f"Category '{new}' already exists!",parent=win)
        finally:
            conn.commit()
            conn.close()
            populate_comboboxes()

    def Edit_cat():
        selected = combo_category.get()

        if selected == "":
            return

        new = simpledialog.askstring("Edit", "Enter New Category name:",initialvalue=selected)
        if not new:
            return

        conn = db.connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE Categories SET CName = %s WHERE CName = %s", (new, selected))
        conn.commit()
        conn.close()
        populate_comboboxes()
        combo_category.set(new)

    def delete(Name,Element,Table,combo):
        selected = combo.get()
        if selected=="":
            return

        confirm = messagebox.askyesno("Delete", f"Delete {Name} '{selected}'?",parent=win)
        if not confirm:
            return

        conn = db.connect_db()
        cursor = conn.cursor()
        query = f"DELETE FROM {Table} WHERE {Element} = %s"
        cursor.execute(query, (selected,))
        conn.commit()
        conn.close()

        populate_comboboxes()
        combo.set("")
        messagebox.showinfo("Deleted", f"{Name} removed successfully!",parent=win)


    btn_delete = tk.Button(frame_form, text="Add", command=lambda: add_cat())
    btn_delete.grid(row=0, column=6, padx=5, pady=5)
    btn_delete = tk.Button(frame_form, text="Edit",command=lambda: Edit_cat())
    btn_delete.grid(row=0, column=7, padx=5, pady=5)
    btn_delete = tk.Button(frame_form, text="Delete", command=lambda:delete("Category","CName","Categories",combo_category))
    btn_delete.grid(row=0, column=8, padx=5, pady=5)

    btn_delete = tk.Button(frame_form, text="Add", command=lambda: supmanag("Add"))
    btn_delete.grid(row=1, column=6, padx=5, pady=5)
    btn_delete = tk.Button(frame_form, text="Edit",command=lambda: supmanag("Edit"))
    btn_delete.grid(row=1, column=7, padx=5, pady=5)
    btn_delete = tk.Button(frame_form, text="Delete", command=lambda: delete("Supplier", "SName", "Suppliers", combo_supplier))
    btn_delete.grid(row=1, column=8, padx=5, pady=5)


    # --- Frame for Displaying Products ---
    frame_tree = tk.LabelFrame(win, text="Product List")
    frame_tree.pack(pady=10, padx=10, fill="both", expand=True)
    tree = ttk.Treeview(frame_tree,
                        columns=("ID", "Name", "SellingPrice", "CostPrice", "Quantity", "Category", "Supplier"),
                        show="headings")

    tree.heading("ID", text="ID")
    tree.heading("Name", text="Product Name")
    tree.heading("SellingPrice", text="Selling Price")
    tree.heading("CostPrice", text="Cost Price")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Category", text="Category")
    tree.heading("Supplier", text="Supplier")

    for col in tree["columns"]:
        tree.column(col, width=10, anchor="center")

    tree.pack(fill="both", expand=True)

    # --- CRUD Functions ---
    def populate_treeview():
        for item in tree.get_children():
            tree.delete(item)

        conn = db.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.ProductID, p.PName, p.Price, p.Cost, p.Quantity, c.CName, s.SName 
            FROM Products p
            JOIN Categories c ON p.CategoryID = c.CategoryID
            JOIN Suppliers s ON p.SupplierID = s.SupplierID
        ''')
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    def add_product():
        name = entry_name.get()
        s_price = entry_selling_price.get()
        c_price = entry_cost_price.get()
        quantity = entry_quantity.get()
        category_name = combo_category.get()
        supplier_name = combo_supplier.get()

        if not (name and s_price and c_price and quantity and category_name and supplier_name):
            messagebox.showerror("Error", "Please fill all fields",parent=win)
            return

        try:
            conn = db.connect_db()
            cursor = conn.cursor()

            cursor.execute("SELECT CategoryID FROM Categories WHERE CName = %s", (category_name,))
            cat_id = cursor.fetchone()[0]
            cursor.execute("SELECT SupplierID FROM Suppliers WHERE SName = %s", (supplier_name,))
            sup_id = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO Products (PName, Price, Cost, Quantity, CategoryID, SupplierID) VALUES (%s, %s, %s, %s, %s, %s)",
                (name, float(s_price), float(c_price), int(quantity), cat_id, sup_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Product added successfully",parent=win)
            populate_treeview()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}",parent=win)

    def delete_product():
        if not tree.selection():
            messagebox.showerror("Error", "Please select a product to delete",parent=win)
            return

        selected_item = tree.selection()[0]
        product_id = tree.item(selected_item, 'values')[0]

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this?",parent=win):
            try:
                conn = db.connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Products WHERE ProductID = %s", (product_id,))
                conn.commit()
                conn.close()
                populate_treeview()
                messagebox.showinfo("Success", "Product deleted successfully",parent=win)
            except Exception as e:
                messagebox.showerror("Database Error", f"{e}",parent=win)

    def update_product():
        if not tree.selection():
            messagebox.showerror("Error", "Please select a product to update",parent=win)
            return

        name = entry_name.get()
        s_price = entry_selling_price.get()
        c_price = entry_cost_price.get()
        stock = entry_quantity.get()
        category_name = combo_category.get()
        supplier_name = combo_supplier.get()

        if not(name and s_price and c_price and stock and category_name and supplier_name):
            messagebox.showerror("Error", "Please fill all fields",parent=win)
            return

        selected_item = tree.selection()[0]
        product_id = tree.item(selected_item, 'values')[0]

        try:
            conn = db.connect_db()
            cursor = conn.cursor()

            # جلب الـ IDs
            cursor.execute("SELECT CategoryID FROM Categories WHERE CName = %s", (category_name,))
            cat_id = cursor.fetchone()[0]
            cursor.execute("SELECT SupplierID FROM Suppliers WHERE SName = %s", (supplier_name,))
            sup_id = cursor.fetchone()[0]

            cursor.execute('''
                UPDATE Products 
                SET PName=%s, Price=%s, Cost=%s, Quantity=%s, CategoryID=%s, SupplierID=%s 
                WHERE ProductID=%s
            ''', (name, float(s_price), float(c_price), int(stock), cat_id, sup_id, product_id))

            conn.commit()
            conn.close()
            populate_treeview()
            messagebox.showinfo("Success", "Product updated successfully",parent=win)
        except Exception as e:
            messagebox.showerror("Database Error", f"{e}",parent=win)

    # --- Control Buttons ---
    frame_buttons = tk.Frame(win)
    frame_buttons.pack(pady=10)

    btn_add = tk.Button(frame_buttons, text="Add Product", command=add_product)
    btn_add.pack(side="left", padx=5)
    btn_add = tk.Button(frame_buttons, text="Edit Product", command=update_product)
    btn_add.pack(side="left", padx=5)
    btn_add = tk.Button(frame_buttons, text="Delete Product", command=delete_product)
    btn_add.pack(side="left", padx=5)


    populate_comboboxes()
    populate_treeview()
# --- Create New Bill Window ---
def create_bill_window():
    win = tk.Toplevel(root)
    win.title("Create New Bill")
    win.geometry("750x550")

    current_bill_items = []  # Temporary list to store items for the current bill

    # --- Frame for Bill Details ---
    frame_details = tk.LabelFrame(win, text="Bill Details")
    frame_details.pack(pady=10, padx=10, fill="x")

    tk.Label(frame_details, text="Cashier:").grid(row=0, column=0, padx=5, pady=5)
    entry_cashier = tk.Entry(frame_details)
    entry_cashier.grid(row=0, column=1, padx=5, pady=5)
    entry_cashier.insert(0, "Admin")  # Default value

    tk.Label(frame_details, text="Customer:").grid(row=0, column=2, padx=5, pady=5)
    combo_customer = ttk.Combobox(frame_details, state="readonly")
    combo_customer.grid(row=0, column=3, padx=5, pady=5)
    btn_delete = tk.Button(frame_details, text="Add", command=lambda:cus_manag("Add"))
    btn_delete.grid(row=0, column=4, padx=5, pady=5)
    btn_delete = tk.Button(frame_details, text="Edit", command=lambda:cus_manag("Edit"))
    btn_delete.grid(row=0, column=5, padx=5, pady=5)
    btn_delete = tk.Button(frame_details, text="Delete",command=lambda:delete() )
    btn_delete.grid(row=0, column=6, padx=5, pady=5)


    # --- Frame for Adding Products to Bill ---
    frame_add_product = tk.LabelFrame(win, text="Add Product")
    frame_add_product.pack(pady=10, padx=10, fill="x")

    tk.Label(frame_add_product, text="Select Product:").grid(row=0, column=0, padx=5, pady=5)
    combo_product = ttk.Combobox(frame_add_product, state="readonly")
    combo_product.grid(row=0, column=1, padx=5, pady=5)


    tk.Label(frame_add_product, text="Quantity:").grid(row=0, column=2, padx=5, pady=5)
    entry_quantity = tk.Entry(frame_add_product, width=10)
    entry_quantity.grid(row=0, column=3, padx=5, pady=5)

    def populate_comboboxes():
        conn = db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT CName FROM Customers")
        customers = [c[0] for c in cursor.fetchall()]
        combo_customer['values'] = customers

        cursor.execute("SELECT PName FROM Products WHERE Quantity > 0")
        products = [p[0] for p in cursor.fetchall()]
        combo_product['values'] = products
        conn.close()
        conn.close()

    populate_comboboxes()

    def cus_manag(act):
        if act == "Edit":
            if combo_customer.get() == "":
                return

        sup_win = tk.Toplevel(win)
        sup_win.title(f"{act} Customer")
        sup_win.geometry("300x200")

        supframe = tk.Frame(sup_win)
        supframe.pack(pady=10)

        tk.Label(supframe, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entryN = tk.Entry(supframe)
        entryN.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(supframe, text="Phone Number:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        entryP = tk.Entry(supframe)
        entryP.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(supframe, text="Address:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        entryA = tk.Entry(supframe)
        entryA.grid(row=2, column=1, padx=5, pady=5)

        if act == "Edit":
            conn = db.connect_db()
            cursor = conn.cursor()
            cursor.execute('''
            SELECT CName,Phone,Address FROM Customers WHERE CName= %s;
            ''',(combo_customer.get(),))
            row = cursor.fetchone()
            entryN.insert(0, row[0])
            entryP.insert(0, row[1])
            entryA.insert(0, row[2])
            conn.close()

        supbtn = tk.Button(supframe, text=f"{act} Customer",command=lambda:cus_man_btn(entryN,entryP,entryA,act,sup_win))
        supbtn.grid(row=3, column=0, columnspan=2, pady=15)

    def cus_man_btn(entryN,entryP,entryA,act,window):
        name_select = entryN.get()
        phone_select = entryP.get()
        address_select = entryA.get()
        if not name_select or not address_select or not phone_select:
            return
        conn = db.connect_db()
        cursor = conn.cursor()
        try:
            if act == "Edit":
                cursor.execute("""
                       UPDATE Customers
                       SET CName = %s, Phone = %s,Address = %s
                       WHERE CName = %s
                   """, (name_select, phone_select,address_select,combo_customer.get()))
            else:
                cursor.execute("""
                       INSERT INTO Customers (CName,Phone,Address)
                       VALUES (%s,%s,%s)
                   """, (name_select, phone_select,address_select))
        except mysql.connector.Error:
            messagebox.showerror("Error", "Name already exists!",parent=window)
        finally:
            conn.commit()
            conn.close()

            update_bill_treeview()
            populate_comboboxes()
            combo_customer.set(name_select)
            window.destroy()

    def delete():
        selected = combo_customer.get()
        if selected=="":
            return
        confirm = messagebox.askyesno("Delete", f"Delete {selected} Customer?",parent=win)
        if not confirm:
            return
        conn = db.connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Customers WHERE CName = %s", (selected,))
        conn.commit()
        conn.close()

        update_bill_treeview()
        combo_customer.set("")
        populate_comboboxes()
        messagebox.showinfo("Deleted", f"Customers removed successfully!",parent=win)

    def add_to_bill():
        product_name = combo_product.get()
        quantity_str = entry_quantity.get()
        if not product_name or not quantity_str:
            messagebox.showerror("Error", "Select a product and enter quantity",parent=win)
            return

        for item in current_bill_items:
            if item['name'] == product_name:
                item['quantity'] += int(quantity_str)
                update_bill_treeview()
                return

        try:
            quantity = int(quantity_str)
            conn = db.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT ProductID, PName, Price, Quantity FROM Products WHERE PName = %s",
                           (product_name,))
            product = cursor.fetchone()
            conn.close()

            if not product:
                return
            pid, pname, price, stock = product
            if quantity > stock:
                messagebox.showerror("Error", "Requested quantity is not available in stock",parent=win)
                return

            # Add to temporary list
            current_bill_items.append({'pid': pid, 'name': pname, 'price': price, 'quantity': quantity})
            update_bill_treeview()
            entry_quantity.delete(0, tk.END)
            combo_product.set("")

        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number",parent=win)

    btn_add_to_bill = tk.Button(frame_add_product, text="Add to Bill", command=add_to_bill)
    btn_add_to_bill.grid(row=0, column=4, padx=10, pady=5)

    # --- Frame for Displaying Bill Items ---
    frame_bill_items = tk.LabelFrame(win, text="Bill Items")
    frame_bill_items.pack(pady=10, padx=10, fill="both", expand=True)

    tree_bill = ttk.Treeview(frame_bill_items, columns=("Name", "Price", "Quantity", "Total"), show="headings")
    tree_bill.heading("Name", text="Product Name")
    tree_bill.heading("Price", text="Price")
    tree_bill.heading("Quantity", text="Quantity")
    tree_bill.heading("Total", text="Total")
    for col in tree_bill["columns"]:
        tree_bill.column(col, width=10, anchor="center")
    tree_bill.pack(fill="both", expand=True)

    def update_bill_treeview():
        # Clear the tree
        for item in tree_bill.get_children():
            tree_bill.delete(item)
        total = 0
        # Add items from the temporary list
        for item in current_bill_items:
            item_total = item['price'] * item['quantity']
            tree_bill.insert("", "end",
                             values=(item['name'], f"{item['price']:.2f}", item['quantity'], f"{item_total:.2f}"))
            total += item_total
        label_total.config(text=f"Total: {total:.2f}")

    # --- Bill Total and Control Buttons ---
    frame_total = tk.Frame(win)
    frame_total.pack(pady=10)

    label_total = tk.Label(frame_total, text="Total: 0.00", font=("Arial", 14, "bold"))
    label_total.pack(side="left", padx=20)

    def Submit_Bill():
        if not current_bill_items:
            messagebox.showerror("Error", "There are no items in the bill",parent=win)
            return

        customer_name = combo_customer.get()
        cashier_name = entry_cashier.get()
        if not customer_name or not cashier_name:
            messagebox.showerror("Error", "Select a customer and enter the cashier's name",parent=win)
            return

        try:
            conn = db.connect_db()
            cursor = conn.cursor()

            # 1. Get Customer ID
            cursor.execute("SELECT CustomerID FROM Customers WHERE CName = %s", (customer_name,))
            customer_id = cursor.fetchone()[0]

            # 2. Calculate total amount
            total_amount = sum(item['price'] * item['quantity'] for item in current_bill_items)

            cursor.execute('''
                INSERT INTO Bills (CashierName, CustomerID, TotalAmount, BillDateTime)
                VALUES ( %s, %s, %s, %s)
            ''', (cashier_name, customer_id, total_amount, datetime.now()))

            bill_id = cursor.lastrowid

            for item in current_bill_items:
                cursor.execute('''
                    INSERT INTO Bill_Product (BillID, ProductID, Quantity, PriceAtSale)
                    VALUES (%s, %s, %s, %s)
                ''', (bill_id, item['pid'], item['quantity'], item['price']))

                cursor.execute('''
                    UPDATE Products SET Quantity = Quantity - %s
                    WHERE ProductID = %s
                ''', (item['quantity'], item['pid']))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"Bill #{bill_id} finalized successfully!",parent=win)
            win.destroy()  # Close the bill window

        except Exception as e:
            messagebox.showerror("Database Error", f"Could not finalize bill: {e}",parent=win)

    btn_finalize = tk.Button(frame_total, text="Submit Bill", command=Submit_Bill)
    btn_finalize.pack(side="left", padx=5)

def All_bill():
    win = tk.Toplevel(root)
    win.title("Create New Bill")
    win.geometry("750x350")


    frame_tree = tk.LabelFrame(win, text="Bill List")
    frame_tree.pack(pady=10, padx=10, fill="both", expand=True)

    tree = ttk.Treeview(frame_tree,
                        columns=("ID", "Cashier_Name", "Customer_Name", "TotalAmount", "BillDateTime"),
                        show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Cashier_Name", text="Cashier_Name")
    tree.heading("Customer_Name", text="Customer_Name")
    tree.heading("TotalAmount", text="TotalAmount")
    tree.heading("BillDateTime", text="BillDateTime")
    for col in tree["columns"]:
        tree.column(col, width=10, anchor="center")
    tree.pack(fill="both", expand=True)


    def populate_treeview():
        for item in tree.get_children():
            tree.delete(item)
        conn = db.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
                SELECT b.BillID,b.CashierName,c.CName,b.TotalAmount,b.BillDateTime
                FROM Bills b
                JOIN Customers c ON c.CustomerID = b.CustomerID
            ''')
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    def bill_det():
        if not tree.selection():
            messagebox.showerror("Error", "Please select a Bill to See",parent=win)
            return
        selected_item = tree.selection()[0]
        BillID = tree.item(selected_item, 'values')[0]

        sup_win = tk.Toplevel(win)
        sup_win.title(f"Bill #{BillID} Details")
        sup_win.geometry("400x300")

        billfr = tk.LabelFrame(sup_win, text="Bill Items")
        billfr.pack(pady=10, padx=10, fill="both", expand=True)

        billtree = ttk.Treeview(billfr,
                            columns=("Products_Name", "Quantity", "PriceAtSale"),
                            show="headings")
        billtree.heading("Products_Name", text="Products Name")
        billtree.heading("Quantity", text="Quantity")
        billtree.heading("PriceAtSale", text="Price At Sale")
        for col in billtree["columns"]:
            billtree.column(col, width=10, anchor="center")
        billtree.pack(fill="both", expand=True)

        conn = db.connect_db()
        cursor = conn.cursor()

        cursor.execute('''
                SELECT p.PName, b.Quantity, b.PriceAtSale,((b.PriceAtSale - p.Cost) * b.Quantity)
                FROM Bill_Product b
                JOIN Products p ON p.ProductID = b.ProductID
                WHERE b.BillID = %s
            ''',(BillID,))

        total_profit = 0
        records = cursor.fetchall()
        for row in records:
            total_profit += row[3]
            billtree.insert("", "end", values=row[:3])
        conn.close()

        label_total = tk.Label(billfr,
                               text=f"Total Bill Profit: {total_profit:,.2f}",
                               fg="green",
                               font=("Arial", 14, "bold"),
                               )
        label_total.pack(side="right",padx=10,pady=10)

    def delete_bill():
        if not tree.selection():
            messagebox.showerror("Error", "Please select a Bill to delete",parent=win)
            return

        selected_item = tree.selection()[0]
        bill_id = tree.item(selected_item, 'values')[0]

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this?",parent=win):
            try:
                conn = db.connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Bills WHERE BillID = %s", (bill_id,))
                conn.commit()
                conn.close()
                populate_treeview()
                messagebox.showinfo("Success", f"Bill No.{bill_id} successfully deleted",parent=win)
            except Exception as e:
                messagebox.showerror("Database Error", f"{e}",parent=win)

    populate_treeview()

    frame_buttons = tk.Frame(win)
    frame_buttons.pack(pady=10)

    btn_details = tk.Button(frame_buttons, text="See Details", command=bill_det)
    btn_details.pack(side="left", padx=5)
    btn_delete = tk.Button(frame_buttons, text="Delete bill", command=delete_bill)
    btn_delete.pack(side="left", padx=5)
# --- Main Application Window ---
root = tk.Tk()
root.title("Supermarket Management System")
root.geometry("400x300")

db.create_tables()

label_title = tk.Label(root, text="Supermarket Management System", font=("Arial", 16, "bold"))
label_title.pack(pady=20)

btn_manage_products = tk.Button(root, text="Product Management", width=20, command=manage_products_window)
btn_manage_products.pack(pady=10)

btn_create_bill = tk.Button(root, text="Create New Bill", width=20, command=create_bill_window)
btn_create_bill.pack(pady=10)

btn_All_bill = tk.Button(root, text="All Bill", width=20, command=All_bill)
btn_All_bill.pack(pady=10)

root.mainloop()

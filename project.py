from tkinter import *
from tkinter.font import Font
from tkinter import messagebox, filedialog
from tkinter.ttk import Treeview, Style
from PIL import Image, ImageTk
import sqlite3
import random
from barcode import Code128
from barcode.writer import ImageWriter
from pyzbar.pyzbar import decode
from fpdf import FPDF
from datetime import datetime
import os
import webbrowser


def create_tbl(c):
    c.execute(
        """CREATE TABLE IF NOT EXISTS inventory (
            item_name TEXT,
            item_description TEXT,
            item_quantity INT,
            item_id TEXT UNIQUE
        )"""
    )
    c.connection.commit()


def exit_program(conn, root):
    conn.close()
    root.destroy()


def check_item(c, name, desc, qty, item_id, add_top):

    c.execute("SELECT item_id FROM inventory WHERE item_id = ?", (item_id,))
    result = c.fetchone()

    if name and qty and item_id:
        if len(item_id) != 10 or not item_id.isdigit():
            messagebox.showerror(
                "Item ID Invalid",
                "Item ID must be 10 characters long and contain only digits.",
                parent=add_top,
            )
            return False

        if not desc:
            desc = "N/A"

        if not qty.isdigit() or int(qty) < 0:
            messagebox.showerror(
                "Quantity Invalid",
                "Quantity must be a non-negative integer.",
                parent=add_top,
            )
            return False

        if result:
            messagebox.showerror(
                "Duplicate ID",
                "Item ID already exists. Please use a different ID.",
                parent=add_top,
            )
            return False

    else:
        messagebox.showerror(
            "Missing Input", "Please fill out all fields.", parent=add_top
        )
        return False

    return True


def save_item(
    name,
    desc,
    qty,
    item_id,
    c,
    conn,
    add_top,
    itm_name_entry,
    itm_desc_entry,
    itm_qty_entry,
    itm_id_entry,
):
    if check_item(c, name, desc, qty, item_id, add_top):
        if not desc:
            desc = "N/A"

        c.execute(
            """INSERT INTO inventory (
                  item_name, item_description, item_quantity, item_id
            ) VALUES (?, ?, ?, ?)""",
            (name, desc, qty, item_id),
        )
        conn.commit()
        messagebox.showinfo("Success", "Item added successfully.", parent=add_top)

        itm_name_entry.delete(0, END)
        itm_desc_entry.delete(0, END)
        itm_qty_entry.delete(0, END)
        itm_id_entry.delete(0, END)
        itm_name_entry.focus()


def back():
    if "add_top" in globals() and add_top.winfo_exists():
        add_top.destroy()
    if "view_top" in globals() and view_top.winfo_exists():
        view_top.destroy()
    if "edit_menu_top" in globals() and edit_menu_top.winfo_exists():
        edit_menu_top.destroy()


def generate_random_id(cursor):
    while True:
        random_id = "".join(random.choices("0123456789", k=10))
        cursor.execute("SELECT item_id FROM inventory WHERE item_id = ?", (random_id,))
        if not cursor.fetchone():
            return random_id


def confirm_generate_id():
    if messagebox.askyesno(
        "Confirm ID Generation",
        "Are you sure you want to generate a new random 10-digit ID?",
        parent=add_top,
    ):
        new_id = generate_random_id(cursor=c)
        itm_id.set(new_id)


def add_item():
    global add_top
    global itm_name
    global itm_name_entry
    global itm_desc
    global itm_desc_entry
    global itm_qty
    global itm_qty_entry
    global itm_id
    global itm_id_entry

    add_top = Toplevel(root)
    add_top.title("Add An Item")
    icon = PhotoImage(file=r"PyVentory.png")
    root.iconphoto(True, icon)
    add_top.geometry("400x500")

    x = round(root.winfo_x() + root.winfo_width() // 7) - add_top.winfo_width() // 2
    y = round(root.winfo_y() + root.winfo_height() // 4) - add_top.winfo_height() // 2
    add_top.geometry(f"+{x}+{y}")

    form_frame = Frame(add_top)
    form_frame.pack(pady=20, padx=20, fill="both", expand=True)

    itm_name_lbl_font = Font(family="Helvetica", size=12)
    itm_name_lbl = Label(form_frame, text="Item Name:", font=itm_name_lbl_font)
    itm_name_lbl.grid(row=0, column=0, sticky="w", pady=5)

    itm_name = StringVar()
    itm_name_entry = Entry(form_frame, textvariable=itm_name)
    itm_name_entry.grid(row=0, column=1, pady=5, sticky="ew")

    itm_name_entry.focus()

    itm_desc_lbl_font = Font(family="Helvetica", size=12)
    itm_desc_lbl = Label(form_frame, text="Item Description:", font=itm_desc_lbl_font)
    itm_desc_lbl.grid(row=1, column=0, sticky="w", pady=5)

    itm_desc = StringVar()
    itm_desc_entry = Entry(form_frame, textvariable=itm_desc)
    itm_desc_entry.grid(row=1, column=1, pady=5, sticky="ew")

    itm_qty_lbl_font = Font(family="Helvetica", size=12)
    itm_qty_lbl = Label(form_frame, text="Item Quantity:", font=itm_qty_lbl_font)
    itm_qty_lbl.grid(row=2, column=0, sticky="w", pady=5)

    itm_qty = StringVar()
    itm_qty_entry = Entry(form_frame, textvariable=itm_qty)
    itm_qty_entry.grid(row=2, column=1, pady=5, sticky="ew")

    itm_id_lbl_font = Font(family="Helvetica", size=12)
    itm_id_lbl = Label(form_frame, text="Item ID (10-Digits):", font=itm_id_lbl_font)
    itm_id_lbl.grid(row=3, column=0, sticky="w", pady=5)

    itm_id = StringVar()
    itm_id_entry = Entry(form_frame, textvariable=itm_id)
    itm_id_entry.grid(row=3, column=1, pady=5, sticky="ew")

    btn_frame = Frame(add_top)
    btn_frame.pack(pady=10, padx=20, fill="x")

    generate_id_btn_font = Font(family="Helvetica", size=12)
    generate_id_btn = Button(
        btn_frame,
        text="Generate Random ID",
        font=generate_id_btn_font,
        command=confirm_generate_id,
        bg="#2196F3",
        fg="white",
        relief="flat",
    )
    generate_id_btn.pack(side="left", padx=5)

    save_btn_font = Font(family="Helvetica", size=12)
    save_btn = Button(
        btn_frame,
        text="Save Item",
        font=save_btn_font,
        command=lambda: save_item(
            name=itm_name_entry.get(),
            desc=itm_desc_entry.get(),
            qty=itm_qty_entry.get(),
            item_id=itm_id_entry.get(),
            itm_name_entry=itm_name_entry,
            itm_desc_entry=itm_desc_entry,
            itm_qty_entry=itm_qty_entry,
            itm_id_entry=itm_id_entry,
            c=c,
            conn=conn,
            add_top=add_top,
        ),
        bg="#4CAF50",
        fg="white",
        relief="flat",
    )

    save_btn.pack(side="left", padx=5)

    back_btn_font = Font(family="Helvetica", size=12)
    back_btn = Button(
        btn_frame,
        text="Back",
        font=back_btn_font,
        command=back,
        bg="#f44336",
        fg="white",
        relief="flat",
    )
    back_btn.pack(side="left", padx=5)

    form_frame.columnconfigure(1, weight=1)


def view_items():
    global view_top
    global tree
    global search_entry

    view_top = Toplevel(root)
    view_top.title("View Inventory")
    icon = PhotoImage(file=r"PyVentory.png")
    root.iconphoto(True, icon)

    view_top.attributes("-fullscreen", True)

    search_lbl_font = Font(family="Helvetica", size=16, weight="bold")
    search_lbl = Label(
        view_top, text="Search by Name or Item ID:", font=search_lbl_font
    )
    search_lbl.pack(pady=20)

    search_frame = Frame(
        view_top, borderwidth=2, relief="groove", background="dark gray"
    )
    search_frame.pack(pady=10, padx=20, fill="x")

    search_entry = Entry(search_frame, width=60, font=("Helvetica", 14))
    search_entry.pack(side="left", padx=10, pady=5)

    clear_search_btn = Button(
        search_frame,
        text="Clear",
        font=("Helvetica", 12, "bold"),
        command=clear_search,
        borderwidth=2,
        relief="raised",
    )
    clear_search_btn.pack(side="right", padx=10, pady=5)

    search_btn_frame = Frame(view_top, background="dark gray")
    search_btn_frame.pack(pady=10)

    search_btn = Button(
        search_btn_frame,
        text="Search",
        font=("Helvetica", 14, "bold"),
        command=lambda: search_items(search_entry.get()),
        borderwidth=2,
        relief="raised",
    )
    search_btn.pack(pady=7, padx=7)

    tree_frame = Frame(view_top, background="dark gray")
    tree_frame.pack(pady=10, padx=20, fill="both", expand=True)

    style = Style()
    style.configure("Treeview.Heading", font=(None, 15))

    tree = Treeview(
        tree_frame,
        columns=("Item Name", "Description", "Quantity", "Item ID"),
        show="headings",
    )
    tree.column("Item Name", anchor=W, width=250)
    tree.column("Description", anchor=W, width=1000)
    tree.column("Quantity", anchor=CENTER, width=20)
    tree.column("Item ID", anchor=CENTER, width=30)

    tree.heading("Item Name", text="Item Name", anchor=W)
    tree.heading("Description", text="Description", anchor=W)
    tree.heading("Quantity", text="Quantity", anchor=CENTER)
    tree.heading("Item ID", text="Item ID", anchor=CENTER)

    tree.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    display_items(tree=tree, cursor=c)

    barcode_frame = Frame(view_top, background="dark gray")
    barcode_frame.pack(pady=10, padx=20)

    generate_barcode_btn = Button(
        barcode_frame,
        text="Generate Barcode for Selected Item",
        font=("Helvetica", 14),
        borderwidth=2,
        relief="raised",
        command=lambda: (
            generate_barcode(tree.selection()[0])
            if tree.selection()
            else messagebox.showerror(
                "No Selection", "No Item Has Been Selected", parent=view_top
            )
        ),
    )
    generate_barcode_btn.pack(pady=10, padx=7)

    search_barcode_frame = Frame(view_top, background="dark gray")
    search_barcode_frame.pack(pady=10, padx=20)

    search_barcode_btn = Button(
        search_barcode_frame,
        text="Search Item by Barcode",
        font=("Helvetica", 14),
        borderwidth=2,
        relief="raised",
        command=search_barcode,
    )
    search_barcode_btn.pack(pady=10, padx=7)

    save_inventory_frame = Frame(view_top, background="dark gray")
    save_inventory_frame.pack(pady=10, padx=20)

    save_inventory_btn = Button(
        save_inventory_frame,
        text="Save Inventory as PDF",
        font=("Helvetica", 14),
        borderwidth=2,
        relief="raised",
        command=save_inventory,
    )
    save_inventory_btn.pack(pady=10, padx=7)

    back_frame = Frame(view_top, background="dark gray")
    back_frame.pack(pady=20, padx=20)

    back_btn = Button(
        back_frame,
        text="Back",
        font=("Helvetica", 14),
        borderwidth=2,
        relief="raised",
        command=back,
    )
    back_btn.pack(pady=10, padx=7)


def display_items(query="", cursor=None, tree=None):
    if tree is None or cursor is None:
        raise ValueError("Tree and cursor must be provided")

    children = tree.get_children()
    for child in children:
        tree.delete(child)

    if query:
        cursor.execute(
            "SELECT * FROM inventory WHERE item_name LIKE ? OR item_id LIKE ? ORDER BY item_name",
            ("%" + query + "%", "%" + query + "%"),
        )
    else:
        cursor.execute("SELECT * FROM inventory ORDER BY item_name")

    items = cursor.fetchall()
    for iid_num, item in enumerate(items):
        tree.insert(
            parent="",
            index="end",
            iid=iid_num,
            text="",
            values=(item[0], item[1], item[2], item[3]),
        )


def search_items(query=""):
    display_items(query, tree=tree, cursor=c)


def clear_search():
    search_entry.delete(0, "end")
    search_items()


def generate_barcode(selected_item):
    if selected_item:
        item = tree.item(selected_item)
        item_values = item["values"]

        if item_values:
            item_id = str(item_values[3])
            item_name = str(item_values[0])
            item_name = item_name.replace(", ", "_").replace(" ", "_").replace("-", "_")

            filename = f"{item_name}_id_{item_id}"

            code128_barcode = Code128(item_id, writer=ImageWriter())

            new_folder = "Barcodes"
            if not os.path.exists(new_folder):
                os.makedirs(new_folder)

            new_file_path = os.path.join(new_folder, filename)
            code128_barcode.save(new_file_path)

            messagebox.showinfo(
                "Success", f"Barcode saved as {filename}.png", parent=view_top
            )
            try:
                barcode = Image.open(f"{new_file_path}.png")
                barcode.show(title=f"{new_file_path}.png")
                barcode.close()
            except Exception as e:
                print(e)
                messagebox.showerror(
                    "Error",
                    f"An error occurred while opening the barcode: {e}",
                    parent=view_top,
                )
        else:
            messagebox.showerror(
                "Error", "Failed to parse selected item details.", parent=view_top
            )
    else:
        messagebox.showerror(
            "No Selection", "No Item Has Been Selected", parent=view_top
        )


def search_barcode():
    try:
        filename = filedialog.askopenfilename(
            parent=view_top, title="Select a File", filetypes=[("PNG files", "*.png")]
        )
        if filename:
            image = Image.open(filename)
            barcodes = decode(image)
            image.close()

            for barcode in barcodes:
                search_entry.insert(0, f"{barcode.data.decode("utf-8")}")
            search_items(query=f"{barcode.data.decode("utf-8")}")
        else:
            return
    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror(
            title="Error", message=f"An Error Occured: {e}", parent=view_top
        )


def edit_items():
    global edit_menu_top
    global tree
    global search_entry

    edit_menu_top = Toplevel(root)
    edit_menu_top.title("View Inventory")
    icon = PhotoImage(file=r"PyVentory.png")
    root.iconphoto(True, icon)

    edit_menu_top.attributes("-fullscreen", True)

    search_lbl_font = Font(family="Helvetica", size=16, weight="bold")
    search_lbl = Label(
        edit_menu_top, text="Search by Name or Item ID:", font=search_lbl_font
    )
    search_lbl.pack(pady=20)

    search_frame = Frame(
        edit_menu_top, borderwidth=2, relief="groove", background="dark gray"
    )
    search_frame.pack(pady=10, padx=20, fill="x")

    search_entry = Entry(search_frame, width=60, font=("Helvetica", 14))
    search_entry.pack(side="left", padx=10, pady=5)

    clear_search_btn = Button(
        search_frame,
        text="Clear",
        font=("Helvetica", 12, "bold"),
        command=clear_search,
        borderwidth=2,
        relief="raised",
    )
    clear_search_btn.pack(side="right", padx=10, pady=5)

    search_btn_frame = Frame(edit_menu_top, background="dark gray")
    search_btn_frame.pack(pady=10)

    search_btn = Button(
        search_btn_frame,
        text="Search",
        font=("Helvetica", 14, "bold"),
        command=lambda: search_items(search_entry.get()),
        borderwidth=2,
        relief="raised",
    )
    search_btn.pack(pady=7, padx=7)

    tree_frame = Frame(edit_menu_top, background="dark gray")
    tree_frame.pack(pady=10, padx=20, fill="both", expand=True)

    style = Style()
    style.configure("Treeview.Heading", font=(None, 15))

    tree = Treeview(
        tree_frame,
        columns=("Item Name", "Description", "Quantity", "Item ID"),
        show="headings",
    )
    tree.column("Item Name", anchor=W, width=250)
    tree.column("Description", anchor=W, width=1000)
    tree.column("Quantity", anchor=CENTER, width=20)
    tree.column("Item ID", anchor=CENTER, width=30)

    tree.heading("Item Name", text="Item Name", anchor=W)
    tree.heading("Description", text="Description", anchor=W)
    tree.heading("Quantity", text="Quantity", anchor=CENTER)
    tree.heading("Item ID", text="Item ID", anchor=CENTER)

    tree.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    display_items(tree=tree, cursor=c)

    edit_frame = Frame(edit_menu_top, borderwidth=1, background="dark gray")
    edit_frame.pack(pady=5, ipadx=7)

    edit_btn_font = Font(family="Helvetica", size=15)
    edit_btn = Button(
        edit_frame,
        text="Edit Selected Item",
        font=edit_btn_font,
        command=edit_selected_item,
        borderwidth=4,
    )
    edit_btn.pack(pady=5)

    delete_frame = Frame(edit_menu_top, borderwidth=1, background="dark gray")
    delete_frame.pack(pady=5, ipadx=7)

    delete_btn_font = Font(family="Helvetica", size=15)
    delete_btn = Button(
        delete_frame,
        text="Delete Selected Item",
        font=delete_btn_font,
        command=delete_selected_item,
        borderwidth=4,
    )
    delete_btn.pack(pady=5)

    back_frame = Frame(edit_menu_top, borderwidth=1, background="dark gray")
    back_frame.pack(pady=20, ipadx=5)

    back_btn_font = Font(family="Helvetica", size=15)
    back_btn = Button(back_frame, text="Back", font=back_btn_font, command=back)
    back_btn.pack(pady=5)


def delete_selected_item():
    selected_item = tree.selection()
    if selected_item:
        item_id = tree.item(selected_item[0], "values")[3]
        if messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete item with ID {item_id}?",
            parent=edit_menu_top,
        ):
            try:
                c.execute("DELETE FROM inventory WHERE item_id = ?", (item_id,))
                conn.commit()
                messagebox.showinfo(
                    "Success", "Item deleted successfully.", parent=edit_menu_top
                )
                display_items(tree=tree, cursor=c)
            except Exception as e:
                messagebox.showerror(
                    "Error", f"An error occurred: {e}", parent=edit_menu_top
                )
    else:
        messagebox.showerror(
            "No Selection", "No item has been selected", parent=edit_menu_top
        )


def edit_selected_item():
    selected_item = tree.selection()
    if selected_item:
        item_id = tree.item(selected_item[0], "values")[3]
        c.execute("SELECT * FROM inventory WHERE item_id = ?", (item_id,))
        item = c.fetchone()
        if item:
            edit_item(item)
    else:
        messagebox.showerror(
            "No Selection", "No item has been selected", parent=edit_menu_top
        )


def edit_item(item):
    global edit_top
    global edit_name_entry
    global edit_desc_entry
    global edit_qty_entry
    global edit_id_entry

    edit_top = Toplevel(root)
    edit_top.title("Edit Item")
    icon = PhotoImage(file=r"PyVentory.png")
    root.iconphoto(True, icon)
    edit_top.geometry("400x500")
    x = round(root.winfo_x() + root.winfo_width() // 6) - edit_top.winfo_width()
    y = round(root.winfo_y() + root.winfo_height() // 2) - edit_top.winfo_height()
    edit_top.geometry(f"+{x}+{y}")
    edit_top.config(bg="#f9f9f9")

    lbl_font = Font(family="Helvetica", size=14)
    entry_font = Font(family="Helvetica", size=12)
    btn_font = Font(family="Helvetica", size=14)

    frame_name = Frame(edit_top, bg="#f9f9f9")
    frame_name.pack(pady=5, padx=20, fill="x")

    lbl_name = Label(frame_name, text="Item Name:", font=lbl_font, bg="#f9f9f9")
    lbl_name.pack(side="left", padx=10)

    edit_name_entry = Entry(frame_name, font=entry_font)
    edit_name_entry.insert(0, item[0])
    edit_name_entry.pack(side="right", fill="x", expand=True)

    frame_desc = Frame(edit_top, bg="#f9f9f9")
    frame_desc.pack(pady=5, padx=20, fill="x")

    lbl_desc = Label(frame_desc, text="Item Description:", font=lbl_font, bg="#f9f9f9")
    lbl_desc.pack(side="left", padx=10)

    edit_desc_entry = Entry(frame_desc, font=entry_font)
    edit_desc_entry.insert(0, item[1])
    edit_desc_entry.pack(side="right", fill="x", expand=True)

    frame_qty = Frame(edit_top, bg="#f9f9f9")
    frame_qty.pack(pady=5, padx=20, fill="x")

    lbl_qty = Label(frame_qty, text="Item Quantity:", font=lbl_font, bg="#f9f9f9")
    lbl_qty.pack(side="left", padx=10)

    edit_qty_entry = Entry(frame_qty, font=entry_font)
    edit_qty_entry.insert(0, item[2])
    edit_qty_entry.pack(side="right", fill="x", expand=True)

    frame_id = Frame(edit_top, bg="#f9f9f9")
    frame_id.pack(pady=5, padx=20, fill="x")

    lbl_id = Label(frame_id, text="Item ID (10-Digits):", font=lbl_font, bg="#f9f9f9")
    lbl_id.pack(side="left", padx=10)

    edit_id_entry = Entry(frame_id, font=entry_font)
    edit_id_entry.insert(0, item[3])
    edit_id_entry.pack(side="right", fill="x", expand=True)
    edit_id_entry.config(state="readonly")

    save_btn = Button(
        edit_top,
        text="Save Changes",
        font=btn_font,
        command=confirm_edits,
        bg="#4CAF50",
        fg="white",
        relief="flat",
    )
    save_btn.pack(pady=15)

    back_btn = Button(
        edit_top,
        text="Back",
        font=btn_font,
        command=edit_top.destroy,
        bg="#f44336",
        fg="white",
        relief="flat",
    )
    back_btn.pack(pady=15)

    edit_top.mainloop()


def confirm_edits():
    if messagebox.askyesno(
        "Confirm Edits", "Are you sure you want to save these changes?", parent=edit_top
    ):
        save_edits()
    else:
        messagebox.showinfo("Cancelled", "Item edits cancelled.", parent=edit_top)


def save_edits():
    name = edit_name_entry.get()
    desc = edit_desc_entry.get()
    qty = edit_qty_entry.get()
    item_id = edit_id_entry.get()

    if not desc:
        desc = "N/A"

    if not qty.isdigit() or int(qty) < 0:
        messagebox.showerror(
            "Quantity Invalid",
            "Quantity must be a non-negative integer.",
            parent=edit_top,
        )
        return

    c.execute(
        """UPDATE inventory
           SET item_name = ?, item_description = ?, item_quantity = ?
           WHERE item_id = ?""",
        (name, desc, int(qty), item_id),
    )
    conn.commit()
    messagebox.showinfo(
        title="Success", message="Item updated successfully.", parent=edit_top
    )
    display_items(tree=tree, cursor=c)
    edit_top.destroy()


def fetch_data_from_db():
    c.execute("SELECT * FROM inventory")
    data = c.fetchall()

    return data


def save_inventory(viewtop=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.image(r"PyVentory.png", 170, 10, 30)

    pdf.set_xy(0, 10)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, text="PyVentory Export", align="C")
    pdf.ln(10)

    pdf.set_font("Helvetica", "B", 12)
    headers = ["Name", "Description", "Quantity", "ID"]
    col_width = 40
    for header in headers:
        pdf.cell(col_width, 10, header, 1, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", size=12)
    data = fetch_data_from_db()
    for row in data:
        for item in row:
            pdf.cell(col_width, 10, str(item), 1, align="C")
        pdf.ln()

    today = datetime.today().strftime("%Y-%m-%d")
    pdf_file = f"inventory_{today}.pdf"
    pdf.output(pdf_file)

    response = messagebox.askquestion(
        "Success",
        f"PDF has been created successfully: {pdf_file}. Would you like to open it?",
        icon="info",
    )

    if response == "yes":
        webbrowser.open_new(pdf_file)

    if viewtop:
        viewtop.mainloop()


def main():
    global root
    global conn
    global c

    conn = sqlite3.connect("PyVentory.db")
    c = conn.cursor()

    create_tbl(c)

    root = Tk()
    root.title("PyVentory")

    icon = PhotoImage(file=r"C:\Users\oreog\Desktop\Dev\Python\Final Project\PyVentory.png")
    root.iconphoto(True, icon)
    root.config(bg="#e0e0e0")
    root.geometry(
        "{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight())
    )
    root.attributes("-fullscreen", True)

    try:
        original_image = Image.open(r"PyVentory.png")
        new_size = (400, 400)
        resized_image = original_image.resize(new_size, Image.LANCZOS)
        logo = ImageTk.PhotoImage(resized_image)
        logo_lbl = Label(root, image=logo, bg="#e0e0e0")
        logo_lbl.image = logo
        logo_lbl.pack(pady=20)
    except Exception as e:
        print(f"Error loading image: {e}")

    button_font = Font(family="Helvetica", size=18, weight="normal")

    view_item_btn = Button(
        root,
        text="View Inventory",
        font=button_font,
        command=view_items,
        bg="#b0b0b0",
        fg="black",
        relief="flat",
    )
    view_item_btn.pack(pady=10, padx=20)

    add_item_btn = Button(
        root,
        text="Add Item To Inventory",
        font=button_font,
        command=add_item,
        bg="#b0b0b0",
        fg="black",
        relief="flat",
    )
    add_item_btn.pack(pady=10, padx=20)

    edits_items_btn = Button(
        root,
        text="Edit or Delete Item",
        font=button_font,
        command=edit_items,
        bg="#b0b0b0",
        fg="black",
        relief="flat",
    )
    edits_items_btn.pack(pady=10, padx=20)

    exit_btn = Button(
        root,
        text="Exit Program",
        command=lambda: exit_program(conn=conn, root=root),
        font=button_font,
        bg="#a0a0a0",
        fg="black",
        relief="flat",
    )
    exit_btn.pack(pady=20, padx=20)


if __name__ == "__main__":
    main()
    root.mainloop()

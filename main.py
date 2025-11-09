"""
Library Management System (Tkinter + MySQL)
DB connection defaults set from your provided details.

To run:
1) Ensure MySQL server is running and you've executed library.sql to create the DB and tables.
2) Install dependencies:
   pip install mysql-connector-python pandas
3) python main.py
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# ---- Configuration (change if needed) ----
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "Komal&860",
    "database": "library_db"
}
# -----------------------------------------

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        messagebox.showerror("DB Connection Error", str(e))
        return None

# ---- Database helper functions ----
def add_book_to_db(title, author, genre, qty):
    conn = get_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Books (Title, Author, Genre, Quantity) VALUES (%s,%s,%s,%s)",
                   (title, author, genre, qty))
    conn.commit()
    cursor.close()
    conn.close()

def add_member_to_db(name, email):
    conn = get_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Members (Name, Email) VALUES (%s,%s)", (name, email))
    conn.commit()
    cursor.close()
    conn.close()

def borrow_book_db(book_id, member_id):
    conn = get_connection()
    if not conn: return False, "DB Error"
    cursor = conn.cursor()
    # check quantity
    cursor.execute("SELECT Quantity FROM Books WHERE BookID=%s", (book_id,))
    r = cursor.fetchone()
    if not r:
        cursor.close(); conn.close()
        return False, "Book not found"
    if r[0] <= 0:
        cursor.close(); conn.close()
        return False, "No copies available"
    issue = datetime.now().date()
    due = issue + timedelta(days=14)
    cursor.execute("INSERT INTO Borrow (BookID, MemberID, IssueDate, DueDate, Fine) VALUES (%s,%s,%s,%s,%s)",
                   (book_id, member_id, issue, due, 0))
    cursor.execute("UPDATE Books SET Quantity = Quantity - 1 WHERE BookID=%s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return True, "Book borrowed successfully"

def return_book_db(borrow_id):
    conn = get_connection()
    if not conn: return False, "DB Error"
    cursor = conn.cursor()
    cursor.execute("SELECT BookID, DueDate FROM Borrow WHERE BorrowID=%s AND ReturnDate IS NULL", (borrow_id,))
    r = cursor.fetchone()
    if not r:
        cursor.close(); conn.close()
        return False, "Active borrow record not found"
    book_id, due = r
    today = datetime.now().date()
    fine_amt = 0
    if today > due:
        days = (today - due).days
        fine_amt = days * 5  # ₹5 per day
    cursor.execute("UPDATE Borrow SET ReturnDate=%s, Fine=%s WHERE BorrowID=%s", (today, fine_amt, borrow_id))
    cursor.execute("UPDATE Books SET Quantity = Quantity + 1 WHERE BookID=%s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return True, f"Book returned. Fine = {fine_amt}"

def fetch_table(query, params=()):
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    cols = [d[0] for d in cursor.description] if cursor.description else []
    cursor.close()
    conn.close()
    df = pd.DataFrame(rows, columns=cols) if rows else pd.DataFrame(columns=cols)
    return df

# ---- GUI ----
root = tk.Tk()
root.title("Library Management System")

nb = ttk.Notebook(root)
nb.pack(fill='both', expand=True, padx=10, pady=10)

# --- Books Tab ---
frame_books = ttk.Frame(nb)
nb.add(frame_books, text="Books")

def refresh_books():
    df = fetch_table("SELECT * FROM Books")
    for i in tree_books.get_children(): tree_books.delete(i)
    for _, row in df.iterrows():
        tree_books.insert("", "end", values=list(row))

tree_books = ttk.Treeview(frame_books, columns=("BookID","Title","Author","Genre","Quantity"), show='headings')
for c in tree_books["columns"]:
    tree_books.heading(c, text=c)
tree_books.pack(fill='both', expand=True)

def open_add_book():
    w = tk.Toplevel(root)
    w.title("Add Book")
    tk.Label(w, text="Title").grid(row=0,column=0)
    e1 = tk.Entry(w); e1.grid(row=0,column=1)
    tk.Label(w, text="Author").grid(row=1,column=0)
    e2 = tk.Entry(w); e2.grid(row=1,column=1)
    tk.Label(w, text="Genre").grid(row=2,column=0)
    e3 = tk.Entry(w); e3.grid(row=2,column=1)
    tk.Label(w, text="Quantity").grid(row=3,column=0)
    e4 = tk.Entry(w); e4.grid(row=3,column=1)
    def submit():
        try:
            qty = int(e4.get())
        except:
            messagebox.showerror("Error","Quantity must be integer"); return
        add_book_to_db(e1.get(), e2.get(), e3.get(), qty)
        messagebox.showinfo("Success","Book added")
        w.destroy(); refresh_books()
    tk.Button(w, text="Add", command=submit).grid(row=4,column=0,columnspan=2)

tk.Button(frame_books, text="Refresh", command=refresh_books).pack(side='left', padx=5, pady=5)
tk.Button(frame_books, text="Add Book", command=open_add_book).pack(side='left', padx=5, pady=5)

# --- Members Tab ---
frame_members = ttk.Frame(nb)
nb.add(frame_members, text="Members")

def refresh_members():
    df = fetch_table("SELECT * FROM Members")
    for i in tree_mem.get_children(): tree_mem.delete(i)
    for _, row in df.iterrows():
        tree_mem.insert("", "end", values=list(row))

tree_mem = ttk.Treeview(frame_members, columns=("MemberID","Name","Email","JoinDate"), show='headings')
for c in tree_mem["columns"]:
    tree_mem.heading(c, text=c)
tree_mem.pack(fill='both', expand=True)

def open_add_member():
    w = tk.Toplevel(root); w.title("Add Member")
    tk.Label(w, text="Name").grid(row=0,column=0)
    e1 = tk.Entry(w); e1.grid(row=0,column=1)
    tk.Label(w, text="Email").grid(row=1,column=0)
    e2 = tk.Entry(w); e2.grid(row=1,column=1)
    def submit():
        add_member_to_db(e1.get(), e2.get())
        messagebox.showinfo("Success","Member added")
        w.destroy(); refresh_members()
    tk.Button(w, text="Add", command=submit).grid(row=2,column=0,columnspan=2)

tk.Button(frame_members, text="Refresh", command=refresh_members).pack(side='left', padx=5, pady=5)
tk.Button(frame_members, text="Add Member", command=open_add_member).pack(side='left', padx=5, pady=5)

# --- Borrow/Return Tab ---
frame_borrow = ttk.Frame(nb)
nb.add(frame_borrow, text="Borrow/Return")

def refresh_borrows():
    df = fetch_table("SELECT BorrowID, BookID, MemberID, IssueDate, DueDate, ReturnDate, Fine FROM Borrow")
    for i in tree_bor.get_children(): tree_bor.delete(i)
    for _, row in df.iterrows():
        tree_bor.insert("", "end", values=list(row))

tree_bor = ttk.Treeview(frame_borrow, columns=("BorrowID","BookID","MemberID","IssueDate","DueDate","ReturnDate","Fine"), show='headings')
for c in tree_bor["columns"]:
    tree_bor.heading(c, text=c)
tree_bor.pack(fill='both', expand=True)

def open_borrow():
    w = tk.Toplevel(root); w.title("Borrow Book")
    tk.Label(w, text="BookID").grid(row=0,column=0); b1 = tk.Entry(w); b1.grid(row=0,column=1)
    tk.Label(w, text="MemberID").grid(row=1,column=0); m1 = tk.Entry(w); m1.grid(row=1,column=1)
    def submit():
        ok,msg = borrow_book_db(int(b1.get()), int(m1.get()))
        if ok: messagebox.showinfo("Success",msg); w.destroy(); refresh_borrows(); refresh_books()
        else: messagebox.showerror("Error",msg)
    tk.Button(w, text="Borrow", command=submit).grid(row=2,column=0,columnspan=2)

def open_return():
    w = tk.Toplevel(root); w.title("Return Book")
    tk.Label(w, text="BorrowID").grid(row=0,column=0); bid = tk.Entry(w); bid.grid(row=0,column=1)
    def submit():
        ok,msg = return_book_db(int(bid.get()))
        if ok: messagebox.showinfo("Success",msg); w.destroy(); refresh_borrows(); refresh_books()
        else: messagebox.showerror("Error",msg)
    tk.Button(w, text="Return", command=submit).grid(row=1,column=0,columnspan=2)

tk.Button(frame_borrow, text="Refresh", command=refresh_borrows).pack(side='left', padx=5, pady=5)
tk.Button(frame_borrow, text="Borrow", command=open_borrow).pack(side='left', padx=5, pady=5)
tk.Button(frame_borrow, text="Return", command=open_return).pack(side='left', padx=5, pady=5)

# --- Reports Tab ---
frame_reports = ttk.Frame(nb)
nb.add(frame_reports, text="Reports")

def show_top_books():
    df = fetch_table("""SELECT b.Title, COUNT(br.BookID) AS TimesBorrowed
                         FROM Books b
                         JOIN Borrow br ON b.BookID = br.BookID
                         GROUP BY b.Title
                         ORDER BY TimesBorrowed DESC
                         LIMIT 10""")
    w = tk.Toplevel(root); w.title("Top Borrowed Books")
    txt = tk.Text(w, width=60, height=20)
    txt.pack()
    if df.empty:
        txt.insert("end","No data")
    else:
        txt.insert("end", df.to_string(index=False))

tk.Button(frame_reports, text="Top Borrowed Books", command=show_top_books).pack(padx=10, pady=10)

# initial load
refresh_books(); refresh_members(); refresh_borrows()
root.mainloop()

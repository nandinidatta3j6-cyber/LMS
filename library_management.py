"""
Library Management System
Beginner-friendly desktop project using Tkinter and SQLite.

Run:
    python library_management.py

No external packages are required. Tkinter and sqlite3 are included
with most standard Python installations.
"""

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


DB_NAME = "library.db"


def connect_db():
    """Create a database connection and return it."""
    return sqlite3.connect(DB_NAME)


def create_tables():
    """Create the required tables if they do not already exist."""
    with connect_db() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                category TEXT,
                quantity INTEGER NOT NULL DEFAULT 1
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS issued_books (
                issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                student_name TEXT NOT NULL,
                issue_date TEXT NOT NULL,
                return_date TEXT,
                status TEXT NOT NULL DEFAULT 'Issued',
                FOREIGN KEY (book_id) REFERENCES books(book_id)
            )
        """)

        connection.commit()


class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1050x650")
        self.root.minsize(900, 550)

        self.selected_book_id = None

        self.create_widgets()
        self.show_books()

    def create_widgets(self):
        # Main heading
        heading = tk.Label(
            self.root,
            text="LIBRARY MANAGEMENT SYSTEM",
            font=("Arial", 20, "bold"),
            bg="#263238",
            fg="white",
            pady=15
        )
        heading.pack(fill=tk.X)

        # Book details section
        details_frame = tk.LabelFrame(
            self.root,
            text="Book Details",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        details_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(details_frame, text="Book Title:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.title_entry = tk.Entry(details_frame, width=25)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(details_frame, text="Author:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.author_entry = tk.Entry(details_frame, width=25)
        self.author_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(details_frame, text="Category:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.category_entry = tk.Entry(details_frame, width=25)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(details_frame, text="Quantity:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.quantity_entry = tk.Entry(details_frame, width=25)
        self.quantity_entry.grid(row=1, column=3, padx=5, pady=5)
        self.quantity_entry.insert(0, "1")

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=15, pady=5)

        tk.Button(button_frame, text="Add Book", width=13, command=self.add_book).pack(side=tk.LEFT, padx=4)
        tk.Button(button_frame, text="Update Book", width=13, command=self.update_book).pack(side=tk.LEFT, padx=4)
        tk.Button(button_frame, text="Delete Book", width=13, command=self.delete_book).pack(side=tk.LEFT, padx=4)
        tk.Button(button_frame, text="Clear Fields", width=13, command=self.clear_fields).pack(side=tk.LEFT, padx=4)
        tk.Button(button_frame, text="Show All Books", width=13, command=self.show_books).pack(side=tk.LEFT, padx=4)

        # Search section
        search_frame = tk.Frame(self.root)
        search_frame.pack(fill=tk.X, padx=15, pady=8)

        tk.Label(search_frame, text="Search by title or author:").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_books).pack(side=tk.LEFT, padx=4)
        tk.Button(search_frame, text="Reset", command=self.reset_search).pack(side=tk.LEFT, padx=4)

        # Book list
        table_frame = tk.LabelFrame(
            self.root,
            text="Book Records (select a row to edit or delete)",
            font=("Arial", 11, "bold"),
            padx=8,
            pady=8
        )
        table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)

        columns = ("book_id", "title", "author", "category", "quantity")
        self.book_table = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.book_table.heading("book_id", text="Book ID")
        self.book_table.heading("title", text="Title")
        self.book_table.heading("author", text="Author")
        self.book_table.heading("category", text="Category")
        self.book_table.heading("quantity", text="Quantity")

        self.book_table.column("book_id", width=70, anchor=tk.CENTER)
        self.book_table.column("title", width=250)
        self.book_table.column("author", width=200)
        self.book_table.column("category", width=150)
        self.book_table.column("quantity", width=90, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.book_table.yview)
        self.book_table.configure(yscrollcommand=scrollbar.set)

        self.book_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.book_table.bind("<<TreeviewSelect>>", self.select_book)

        # Issue and return section
        issue_frame = tk.LabelFrame(
            self.root,
            text="Issue / Return Book",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=8
        )
        issue_frame.pack(fill=tk.X, padx=15, pady=8)

        tk.Label(issue_frame, text="Student Name:").grid(row=0, column=0, padx=5, pady=5)
        self.student_entry = tk.Entry(issue_frame, width=25)
        self.student_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(issue_frame, text="Issue Date (YYYY-MM-DD):").grid(row=0, column=2, padx=5, pady=5)
        self.date_entry = tk.Entry(issue_frame, width=18)
        self.date_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Button(issue_frame, text="Issue Selected Book", command=self.issue_book).grid(row=0, column=4, padx=5)
        tk.Button(issue_frame, text="Return Selected Book", command=self.return_book).grid(row=0, column=5, padx=5)

        tk.Label(
            self.root,
            text="Tip: Select a book row before updating, deleting, issuing or returning it.",
            fg="#455a64"
        ).pack(pady=(0, 8))

    def get_book_values(self):
        """Read and validate the book form."""
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        category = self.category_entry.get().strip()
        quantity_text = self.quantity_entry.get().strip()

        if not title or not author:
            messagebox.showwarning("Missing Details", "Please enter the book title and author.")
            return None

        try:
            quantity = int(quantity_text)
            if quantity < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid Quantity", "Quantity must be a whole number (0 or more).")
            return None

        return title, author, category, quantity

    def add_book(self):
        values = self.get_book_values()
        if values is None:
            return

        with connect_db() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO books (title, author, category, quantity) VALUES (?, ?, ?, ?)",
                values
            )
            connection.commit()

        messagebox.showinfo("Success", "Book added successfully.")
        self.clear_fields()
        self.show_books()

    def show_books(self):
        # Remove old rows from the table first.
        for row in self.book_table.get_children():
            self.book_table.delete(row)

        with connect_db() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT book_id, title, author, category, quantity FROM books ORDER BY book_id")
            records = cursor.fetchall()

        for record in records:
            self.book_table.insert("", tk.END, values=record)

    def select_book(self, event):
        selected_rows = self.book_table.selection()
        if not selected_rows:
            return

        row_values = self.book_table.item(selected_rows[0], "values")
        self.selected_book_id = int(row_values[0])

        self.clear_form_only()
        self.title_entry.insert(0, row_values[1])
        self.author_entry.insert(0, row_values[2])
        self.category_entry.insert(0, row_values[3])
        self.quantity_entry.insert(0, row_values[4])

    def update_book(self):
        if self.selected_book_id is None:
            messagebox.showwarning("Select Book", "Please select a book from the table first.")
            return

        values = self.get_book_values()
        if values is None:
            return

        with connect_db() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """UPDATE books
                   SET title = ?, author = ?, category = ?, quantity = ?
                   WHERE book_id = ?""",
                values + (self.selected_book_id,)
            )
            connection.commit()

        messagebox.showinfo("Success", "Book details updated.")
        self.clear_fields()
        self.show_books()

    def delete_book(self):
        if self.selected_book_id is None:
            messagebox.showwarning("Select Book", "Please select a book from the table first.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this book?")
        if not confirm:
            return

        with connect_db() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM issued_books WHERE book_id = ? AND status = 'Issued'",
                (self.selected_book_id,)
            )
            active_issues = cursor.fetchone()[0]

            if active_issues > 0:
                messagebox.showwarning(
                    "Book Is Issued",
                    "This book has an active issue record. Return it before deleting."
                )
                return

            cursor.execute("DELETE FROM issued_books WHERE book_id = ?", (self.selected_book_id,))
            cursor.execute("DELETE FROM books WHERE book_id = ?", (self.selected_book_id,))
            connection.commit()

        messagebox.showinfo("Success", "Book deleted successfully.")
        self.clear_fields()
        self.show_books()

    def search_books(self):
        search_text = self.search_entry.get().strip()

        for row in self.book_table.get_children():
            self.book_table.delete(row)

        with connect_db() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """SELECT book_id, title, author, category, quantity
                   FROM books
                   WHERE title LIKE ? OR author LIKE ?
                   ORDER BY book_id""",
                (f"%{search_text}%", f"%{search_text}%")
            )
            records = cursor.fetchall()

        for record in records:
            self.book_table.insert("", tk.END, values=record)

    def reset_search(self):
        self.search_entry.delete(0, tk.END)
        self.show_books()

    def issue_book(self):
        if self.selected_book_id is None:
            messagebox.showwarning("Select Book", "Please select a book to issue.")
            return

        student_name = self.student_entry.get().strip()
        issue_date = self.date_entry.get().strip()

        if not student_name or not issue_date:
            messagebox.showwarning("Missing Details", "Enter the student name and issue date.")
            return

        with connect_db() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT quantity FROM books WHERE book_id = ?", (self.selected_book_id,))
            result = cursor.fetchone()

            if result is None:
                messagebox.showerror("Not Found", "The selected book no longer exists.")
                return

            if result[0] <= 0:
                messagebox.showwarning("Not Available", "No copies of this book are currently available.")
                return

            cursor.execute(
                """INSERT INTO issued_books (book_id, student_name, issue_date, status)
                   VALUES (?, ?, ?, 'Issued')""",
                (self.selected_book_id, student_name, issue_date)
            )
            cursor.execute(
                "UPDATE books SET quantity = quantity - 1 WHERE book_id = ?",
                (self.selected_book_id,)
            )
            connection.commit()

        messagebox.showinfo("Success", "Book issued successfully.")
        self.student_entry.delete(0, tk.END)
        self.show_books()

    def return_book(self):
        if self.selected_book_id is None:
            messagebox.showwarning("Select Book", "Please select a book to return.")
            return

        student_name = self.student_entry.get().strip()
        if not student_name:
            messagebox.showwarning("Missing Details", "Enter the student name who borrowed the book.")
            return

        with connect_db() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """SELECT issue_id FROM issued_books
                   WHERE book_id = ? AND student_name = ? AND status = 'Issued'
                   ORDER BY issue_id LIMIT 1""",
                (self.selected_book_id, student_name)
            )
            issue_record = cursor.fetchone()

            if issue_record is None:
                messagebox.showwarning("Record Not Found", "No active issue record found for this student and book.")
                return

            cursor.execute(
                """UPDATE issued_books
                   SET status = 'Returned', return_date = DATE('now')
                   WHERE issue_id = ?""",
                (issue_record[0],)
            )
            cursor.execute(
                "UPDATE books SET quantity = quantity + 1 WHERE book_id = ?",
                (self.selected_book_id,)
            )
            connection.commit()

        messagebox.showinfo("Success", "Book returned successfully.")
        self.student_entry.delete(0, tk.END)
        self.show_books()

    def clear_form_only(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)

    def clear_fields(self):
        self.selected_book_id = None
        self.clear_form_only()
        self.quantity_entry.insert(0, "1")
        for selected in self.book_table.selection():
            self.book_table.selection_remove(selected)


if __name__ == "__main__":
    create_tables()
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()

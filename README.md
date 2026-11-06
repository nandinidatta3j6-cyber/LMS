# 📚 Library Management System

A simple and beginner-friendly **Library Management System** developed using Python. This project uses **Tkinter** to create a graphical user interface (GUI) and **SQLite3** to store and manage library records.

The system helps users manage books, search records, update book details, and handle book issuing and returning.

## 🚀 Features

- Add new books to the library.
- View all available books.
- Search books by title or author.
- Update existing book details.
- Delete books from the database.
- Issue books to students.
- Return issued books.
- Automatically update available book quantity.
- Store all records permanently using SQLite3.
- Display messages and warnings using Tkinter message boxes.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Tkinter | Graphical User Interface (GUI) |
| SQLite3 | Database management |
| ttk.Treeview | Display book records in table format |
| Messagebox | Display alerts and notifications |

## 📂 Project Structure

```text
Library-Management-System/
│
├── library_management.py
├── README.md
└── library.db
```

**Note:** The `library.db` database file is created automatically when the application runs for the first time.

## ⚙️ Requirements

- Python 3.8 or above.
- Tkinter.
- SQLite3.

Tkinter and SQLite3 are included with most standard Python installations. No additional pip installation is normally required.

## ▶️ How to Run the Project

**Step 1:** Download or clone this repository.

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

**Step 2:** Open the project folder in VS Code.

**Step 3:** Open the terminal.

**Step 4:** Run the Python file.

```bash
python library_management.py
```

On some systems, use:

```bash
python3 library_management.py
```

**Step 5:** The Library Management System window will open.

## 📖 How to Use

1. **Add Book:** Enter book details and click Add Book.
2. **View Books:** View all book records in the table.
3. **Search Book:** Search books using the title or author's name.
4. **Update Book:** Select a book and modify its details.
5. **Delete Book:** Select a book and delete its record.
6. **Issue Book:** Select a book and enter the student's name and issue date.
7. **Return Book:** Select the book and enter the student's name to return it.

## 🗄️ Database Information

This project uses SQLite3 to store library information.

### Books Table

Stores information about books.

| Column | Description |
|---|---|
| book_id | Unique book ID |
| title | Name of the book |
| author | Name of the author |
| category | Book category |
| quantity | Available book quantity |

### Issued Books Table

Stores information about issued and returned books.

| Column | Description |
|---|---|
| issue_id | Unique issue ID |
| book_id | ID of the book |
| student_name | Student's name |
| issue_date | Book issue date |
| return_date | Book return date |
| status | Issued or Returned |

## 💡 Concepts Used

- Python Functions
- Tkinter GUI Programming
- SQLite3 Database Connectivity
- SQL Queries (INSERT, SELECT, UPDATE, DELETE)
- Event Handling
- Exception Handling
- Treeview Table
- Messagebox

## 🎯 Project Objective

The main objective of this project is to develop a simple digital library management system that reduces manual record-keeping and makes book management easier and faster.

## 🔮 Future Improvements

- Login and registration system.
- Admin and student accounts.
- Book due-date reminders.
- Fine calculation system.
- Better user interface.
##Output:


<img width="1919" height="1031" alt="Screenshot 2026-11-05 045930" src="https://github.com/user-attachments/assets/b9d285be-2818-4209-9cc0-7c8f5d8dd92f" />

## 👨‍💻 Author

**Developed by:** Nandini Datta
                  Aashutosh Kumar


**Project:** Library Management System

**Language:** Python

---

⭐ If you find this project useful, feel free to explore the code and learn from it.

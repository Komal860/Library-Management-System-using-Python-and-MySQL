#  Library Management System (Python + MySQL + Tkinter)



---

##  Overview

The **Library Management System** is a desktop application built using **Python**, **Tkinter**, and **MySQL** that helps manage books, members, and borrowing/return transactions.  
It features an easy-to-use graphical interface for librarians to efficiently organize and track library operations.

---

##  Features

- 📘 **Book Management:** Add, update, view, and delete book records  
- 👩‍🎓 **Member Management:** Maintain member details and history  
- 🔁 **Borrow / Return System:** Track issued and returned books  
- 📊 **Reports:** Display top borrowed books and system insights  
- 🔐 **Database Integration:** Securely connected to MySQL  
- 🪟 **Tkinter GUI:** Simple and responsive user interface  

---

##  Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend (GUI)** | Tkinter |
| **Backend (Logic)** | Python |
| **Database** | MySQL |
| **Libraries Used** | `mysql-connector-python`, `pandas` |

---

##  Installation & Setup

 Step 1 — Clone the Repository
```bash
git clone https://github.com/KomalMalekar/Library_Management_System.git
cd Library_Management_System


 Step 2 — Install Dependencies
pip install mysql-connector-python pandas

 Step 3 — Import Database
mysql -u root -p -h localhost  < library.sql
When prompted, enter your MySQL password 

 Step 4 — Run the Application
python main.py
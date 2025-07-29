# ✅ To-Do Task Manager App

A full-stack Task Manager web app built using **Flask**, **MySQL**, and **HTML/CSS/JS**.

Users can register, log in, create tasks, update status, mark favorites (daily tasks), and delete their account. Data is securely stored and fetched from a MySQL database.

---

## 🚀 Features

- 🔐 User Authentication (Signup/Login)
- 📝 Add/Delete Tasks
- ✅ Task Status (Complete / Incomplete)
- ⭐ Mark Favorite (Daily) Tasks
- 📋 Filter & View Daily Tasks
- 🔐 Session-Based Login
- 🔁 Auto status/icon update using DB
- 🧼 Account Deletion with Task Cleanup

---

## 🛠️ Technologies Used

- Python (Flask)
- MySQL (with `mysql-connector-python`)
- HTML5, CSS3, JavaScript
- Jinja2 Templates
- dotenv for config management

---

## 🗃️ Database Schema

### `login` table

| Column    | Type         |
|-----------|--------------|
| email     | VARCHAR      |
| username  | VARCHAR      |
| password  | VARCHAR (hashed recommended) |

### `tasks` table

| Column     | Type         |
|------------|--------------|
| username   | VARCHAR      |
| description| TEXT         |
| status     | VARCHAR (Default: 'Incomplete') |
| fav        | BOOLEAN (0 or 1 Default : 0) |

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/AtharvaManale/To-Do-Task-Manager
cd To-Do-Task-Manager
```
### 2. Create & Configure .env file

DB_HOST=localhost
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=your_db_name
DB_PORT=3306
key=your_secret_flask_key

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
Requirements:
Flask
python-dotenv
mysql-connector-python

### 4. Start the App
``` bash
python app.py
```

🙌 Contribution
Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

📄 License
This project is open-source and available under the MIT License.

✨ Author
Atharv

Crafted with ❤️ using Flask & MySQL
GitHub

---
Let me know if you'd like a `requirements.txt` and sample `.env` file too, or want to add deployment instructions (e.g., PythonAnywhere or Railway).




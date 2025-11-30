# ✅ To-Do Task Manager App

A full-stack Task Manager web app built using **Flask**, **MySQL**, **Redis**and **HTML/CSS/JS**.

Users can register(Verified Registrations only), log in, create tasks, update status, mark favorites (daily tasks), and delete their account. Data is securely stored and fetched from a MySQL database. Also used rate limiters(flask-limiter, Redis) to avoid server overloads.

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

Let me know if you'd like a `requirements.txt` and sample `.env` file too, or want to add deployment instructions (e.g., PythonAnywhere or Railway).

---
## Advancements

As I said I would be making advancements in this project and surely I made some new features Like:
1.Email verification system using OTP(One Time Passwords).
2.Made responsive web design for all devices(I hate doing css for long time but results always fascinates me).
3.Integrated flask-mail for OTP delivery.
4.Integrated flask-limiter with Redis cache to avoid api call abuse and to prevent server overloads and will be preventing from bot attacks

---

## Learning Path

If anyone reads, I just made this project to implement my knowledge and understanding and wanted to see how it works in real applications and I realy like how these things work I understood the syntax of flask-mail and flask-limiter and redis but also my curiosity made me dig deep into its workings and this led to new terms like smtp servers, ttl, redis cache, redis servers sync with all available flask-servers to maintain integrety(Ya I know what are smtp servers, ttl as I am persuing an Engineering degree but didn't knew how they are actually used and how can they be helpful to me). I just want to say just start working on anything you like, you will face problems and while solving those problems you will definetly learn new things and automatically you will be cautious about these things in future.

---

✨ Author
Atharva Manale

Created with ❤️ using Flask & MySQL & Redis & Github
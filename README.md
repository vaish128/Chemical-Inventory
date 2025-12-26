# 🧪 Chemical Inventory System

This is a professional Flask-based management system designed for laboratory chemical tracking. It allows administrators to monitor stock levels, manage unique CAS identifiers, and maintain a digital log of all inventory movements.

---

### 🔗 Live Deployment
**App URL:** [https://vaish128.pythonanywhere.com/](https://vaish128.pythonanywhere.com/)

---

### ✨ Key Features
* **Inventory Tracking:** Real-time dashboard for chemical names, CAS numbers, and units.
* **Stock Alerts:** Automatic "Low Stock" visual badges for items below 10 units.
* **Movement Logs:** Tracks "IN" (restock) and "OUT" (usage) actions with timestamps.
* **Secure Admin Access:** Login-protected routes for inventory management.
* **Search Engine:** Filter chemicals instantly by name or CAS number.

---

### 🛠️ Local Setup Instructions
To run this project on your machine:

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/vaish128/Chemical-Inventory.git](https://github.com/vaish128/Chemical-Inventory.git)
    cd Chemical-Inventory
    ```

2.  **Install Dependencies**
    ```bash
    pip install flask
    ```

3.  **Run the App**
    ```bash
    python app.py
    ```

**Admin Credentials:**
* **Email:** `admin@gmail.com`
* **Password:** `admin@123`

---

### 📋 Database Architecture
The system uses **SQLite** for a lightweight, serverless data experience.

#### **1. Inventory Table**
* **Name:** Product name.
* **CAS Number:** Unique chemical identifier (Unique constraint).
* **Unit:** Measurement (KG, ML, Litre, MT).
* **Stock:** Current quantity.
---

### 🚀 Deployment Info
* **Hosting:** PythonAnywhere
* **Backend:** Flask (Python 3.10)
* **Database:** SQLite3

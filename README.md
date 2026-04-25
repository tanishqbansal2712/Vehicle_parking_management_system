# 🚗 Vehicle Parking Management System
 
A web-based multi-user vehicle parking application built with **Flask** and **SQLite**. The system supports two roles — **Admin** and **User** — enabling complete management of parking lots and real-time 4-wheeler spot booking.
 
---
 
## ✨ Features
 
### 👤 User
- Register and log in securely
- Browse available parking lots
- Reserve a 4-wheeler parking spot
- Release a reserved parking spot
- View personal booking summary
### 🛠️ Admin
- Log in with a pre-seeded admin account
- Create, edit, and delete parking lots
- View all registered users
- View overall parking and booking summaries
---
 
## 🛠 Tech Stack
 
| Layer        | Technology                      |
|--------------|---------------------------------|
| Backend      | Python, Flask                   |
| Database     | SQLite via Flask-SQLAlchemy     |
| Auth         | Flask-Login, Werkzeug           |
| Frontend     | HTML, Jinja2 Templates          |
| Architecture | MVC with Flask Blueprints       |
 
---
 
## 📁 Project Structure
 
```
Vehicle_parking_management_system/
│
├── app.py                   # App entry point, blueprint registration, DB init
│
├── models/
│   └── models.py            # SQLAlchemy models (User, ParkingLot, ParkingSpot, Reservation)
│
├── controllers/
│   ├── auth.py              # Authentication routes (register, login, logout)
│   ├── admin.py             # Admin routes (manage lots, view summaries)
│   └── user.py              # User routes (book and release spots)
│
├── templates/
│   ├── index.html           # Landing/home page
│   ├── auth/                # Login & registration templates
│   ├── admin/               # Admin dashboard templates
│   └── user/                # User dashboard templates
│
├── static/                  # CSS, JS, images
│
└── parking.db               # SQLite database (auto-generated on first run)
```
 
---
 
## 🚀 Getting Started
 
1. **Clone the repository**
   ```bash
   git clone https://github.com/tanishqbansal2712/Vehicle_parking_management_system.git
   cd Vehicle_parking_management_system
   ```
 
2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
 
   # On Windows
   venv\Scripts\activate
 
   # On macOS/Linux
   source venv/bin/activate
   ```
 
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
 
4. **Run the application**
   ```bash
   python app.py
   ```
 
5. **Open in your browser**
   ```
   http://127.0.0.1:5000
   ```
 
> The SQLite database (`parking.db`) and a default admin account are created automatically on first run.
 
---
 
## 🔐 Default Admin Credentials
 
| Field    | Value               |
|----------|---------------------|
| Username | `admin`             |
| Email    | `admin@parking.com` |
| Password | `admin123`          |
 
> ⚠️ Change the default admin password and the `app.secret_key` in `app.py` before deploying to production.
 
---
 
## 📖 Usage
 
**As an Admin** — log in with the default credentials, create parking lots with a name, address, pincode, price per hour, and number of spots. Edit or delete lots anytime, and monitor all users and their bookings from the dashboard.
 
**As a User** — register an account, log in, browse available parking lots, and reserve a spot. When done, release the spot and the system automatically calculates the total cost based on duration and the lot's hourly rate.
 
---
 
## 🗄️ Database Models
 
### `User`
| Field      | Type    | Description                                |
|------------|---------|--------------------------------------------|
| `id`       | Integer | Primary key                                |
| `username` | String  | Unique username                            |
| `email`    | String  | Unique email address                       |
| `password` | String  | Hashed password (Werkzeug)                 |
| `role`     | String  | `'admin'` or `'user'` (default: `'user'`)  |
 
### `ParkingLot`
| Field            | Type    | Description                     |
|------------------|---------|---------------------------------|
| `id`             | Integer | Primary key                     |
| `name`           | String  | Name of the parking lot         |
| `address`        | String  | Street address                  |
| `pincode`        | String  | 6-digit PIN code                |
| `price_per_hour` | Float   | Hourly parking rate             |
| `max_spots`      | Integer | Total capacity of the lot       |
 
### `ParkingSpot`
| Field    | Type    | Description                                 |
|----------|---------|---------------------------------------------|
| `id`     | Integer | Primary key                                 |
| `lot_id` | FK      | References `ParkingLot`                     |
| `status` | String  | `'A'` = Available, `'O'` = Occupied         |
 
### `Reservation`
| Field        | Type     | Description                                    |
|--------------|----------|------------------------------------------------|
| `id`         | Integer  | Primary key                                    |
| `spot_id`    | FK       | References `ParkingSpot`                       |
| `user_id`    | FK       | References `User`                              |
| `start_time` | DateTime | Booking start (auto-set to UTC now)            |
| `end_time`   | DateTime | Booking end (set on release)                   |
| `total_cost` | Float    | Calculated as `(end - start) in hours × price_per_hour` |
 
---
 
## 🤝 Contributing
 
1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request
---
 
<p align="center">Made with ❤️ by <a href="https://github.com/tanishqbansal2712">Tanishq Bansal</a></p>



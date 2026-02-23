# 💊 PharmaFlow — Pharmacy Management System

A minimal, modern Django 5 + PostgreSQL pharmacy management system with a polished Bootstrap 5 frontend.

---

## 📁 Project Structure

```
pharmaflow/                          ← Project root
├── manage.py
├── requirements.txt
├── .env.example                     ← Copy to .env and fill in your values
│
├── pharmaflow/                      ← Django project package
│   ├── __init__.py
│   ├── settings.py                  ← All config (reads from .env)
│   ├── urls.py                      ← Root URL routing
│   └── wsgi.py
│
└── pharmacy/                        ← Main application
    ├── __init__.py
    ├── apps.py
    ├── models.py                    ← All 6 models
    ├── views.py                     ← All views + business logic
    ├── forms.py                     ← ModelForms with Bootstrap widgets
    ├── admin.py                     ← Admin panel configuration
    ├── urls.py                      ← App URL patterns
    ├── migrations/
    │   └── __init__.py
    ├── management/
    │   └── commands/
    │       └── seed.py              ← Example data seeder
    ├── static/
    │   └── pharmacy/
    │       ├── css/style.css        ← Full design system
    │       └── js/main.js           ← Sidebar, alerts, auto-price
    └── templates/
        └── pharmacy/
            ├── base.html            ← Master layout (sidebar + header)
            ├── login.html           ← Auth page
            ├── home.html            ← Dashboard
            ├── medicine_list.html
            ├── medicine_detail.html
            ├── medicine_form.html
            ├── supplier_list.html
            ├── supplier_form.html
            ├── customer_list.html
            ├── customer_form.html
            ├── purchase_list.html
            ├── purchase_form.html
            ├── sale_list.html
            ├── sale_form.html
            ├── contact.html
            └── confirm_delete.html
```

---

## 🗄️ Step 1 — Create PostgreSQL Database

Open **pgAdmin 4** and run or create:

```sql
CREATE DATABASE pharmaflow_db;
```

Or via pgAdmin UI:
1. Right-click **Databases → Create → Database**
2. Name: `pharmaflow_db`
3. Owner: `postgres`
4. Click Save

---

## 🐍 Step 2 — Python Virtual Environment

```bash
# Navigate to project root
cd pharmaflow

# Create virtual environment
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

---

## 📦 Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt includes:**
- `Django>=5.0` — Web framework
- `psycopg2-binary` — PostgreSQL driver
- `python-decouple` — .env file management

---

## ⚙️ Step 4 — Configure Environment

```bash
# Copy the example env file
cp .env.example .env
```

Edit `.env`:
```env
SECRET_KEY=your-random-secret-key-here
DEBUG=True

DB_NAME=pharmaflow_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

> **Tip:** Generate a secret key with:
> `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

---

## 🗃️ Step 5 — Run Migrations

```bash
# Create migration files from models
python manage.py makemigrations

# Apply migrations to PostgreSQL
python manage.py migrate
```

This creates tables for:
- `pharmacy_medicine`
- `pharmacy_supplier`
- `pharmacy_customer`
- `pharmacy_purchase`
- `pharmacy_sale`
- `pharmacy_contactsubmission`

---

## 👤 Step 6 — Create Superuser

```bash
python manage.py createsuperuser
```

Enter username, email, and password when prompted.

---

## 🌱 Step 7 — Seed Example Data (Optional)

```bash
python manage.py seed
```

This adds:
- 4 suppliers (MedLine Global, PharmaDirect, etc.)
- 12 medicines (including expired, low-stock, and out-of-stock examples)
- 6 customers

---

## 🚀 Step 8 — Run the Server

```bash
python manage.py runserver
```

Open: **http://127.0.0.1:8000**

You'll be redirected to the login page. Use your superuser credentials.

---

## 🌐 URL Reference

| URL | Page |
|-----|------|
| `/` | Dashboard |
| `/login/` | Login |
| `/logout/` | Logout |
| `/medicines/` | Medicine list (with search & filter) |
| `/medicines/add/` | Add medicine |
| `/medicines/<id>/` | Medicine detail |
| `/medicines/<id>/edit/` | Edit medicine |
| `/medicines/<id>/delete/` | Delete medicine |
| `/suppliers/` | Supplier list |
| `/suppliers/add/` | Add supplier |
| `/customers/` | Customer list |
| `/customers/add/` | Add customer |
| `/purchases/` | Purchase list |
| `/purchases/add/` | Record purchase (stock in) |
| `/sales/` | Sales list |
| `/sales/add/` | Record sale (stock out) |
| `/contact/` | Contact form |
| `/admin/` | Django admin panel |

---

## 🔄 Data Flow

```
User fills HTML form (Django Template)
       ↓
POST request sent to Django View
       ↓
ModelForm validates data (forms.py)
       ↓
Business logic checked (stock availability, etc.)
       ↓
Django ORM executes SQL via psycopg2
       ↓
PostgreSQL saves data (pharmaflow_db on port 5432)
       ↓
model.save() triggers stock update (Purchase/Sale)
       ↓
Redirect + Django messages flash success/error
       ↓
Template renders updated state to user
```

### Stock Logic
- **Purchase saved** → `medicine.stock += quantity` (atomic, via model.save override)
- **Sale saved** → `medicine.stock -= quantity` (blocked if insufficient)
- **Purchase deleted** → stock is reversed
- **Sale deleted** → stock is restored

---

## ✅ Feature Checklist

- [x] Login / logout authentication
- [x] Dashboard with KPI cards + alert panels
- [x] Medicine CRUD with category + expiry + stock tracking
- [x] Supplier CRUD
- [x] Customer CRUD
- [x] Purchase management (auto stock increase)
- [x] Sales management (auto stock decrease + validation)
- [x] Contact form saved to database
- [x] Admin panel for all models
- [x] Search & filter on medicine list
- [x] Expired medicines highlighted (red rows)
- [x] Low stock / out of stock badges
- [x] Auto price calculation on purchase/sale forms
- [x] Responsive sidebar layout (mobile-friendly)
- [x] Confirmation page before delete
- [x] Django messages for success/error feedback
- [x] Seed command for example data

---

## 🛠️ Troubleshooting

**`FATAL: password authentication failed`**
→ Check `DB_PASSWORD` in your `.env` matches your PostgreSQL password

**`No module named 'psycopg2'`**
→ Run `pip install psycopg2-binary` inside your activated venv

**`No such table` errors**
→ Run `python manage.py migrate`

**Static files not loading**
→ In development, Django serves them automatically. Make sure `DEBUG=True`

**Port 8000 already in use**
→ `python manage.py runserver 8080`

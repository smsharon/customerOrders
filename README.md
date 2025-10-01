```markdown
<div align="center">

# 🛍️ Customer Orders – Backend Challenge Application

[![Django](https://img.shields.io/badge/Django-4.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![DRF](https://img.shields.io/badge/Django_REST-Framework-red?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![JWT](https://img.shields.io/badge/JWT-Authentication-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**A powerful Django-based backend application for seamless customer, inventory, and order management**

[Features](#-features) • [Installation](#-setup-instructions) • [API Docs](#-api-endpoints) • [Testing](#-running-tests)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔐 **Authentication & Security**
- JWT token-based authentication
- OpenID Connect integration
- Secure API access control
- Protected endpoints

</td>
<td width="50%">

### 📦 **Inventory Management**
- Real-time stock tracking
- Stock level indicators (in-stock, low, out-of-stock)
- Automated inventory updates
- CRUD operations

</td>
</tr>
<tr>
<td width="50%">

### 📱 **Order Processing**
- Create and approve orders
- SMS notifications via Africa's Talking
- Transaction audit logs
- Order status tracking

</td>
<td width="50%">

### 🛠️ **Developer Experience**
- Comprehensive unit tests with pytest
- CI/CD with GitHub Actions
- Signal-based automation
- RESTful API design

</td>
</tr>
</table>

---

## 🗄️ Database Architecture

The application uses a robust relational database schema with four core models working together seamlessly:

<div align="center">

![ER Diagram](docs/ER-DIAGRAM.png)

*Entity Relationship Diagram showing Customer, Order, Inventory, and TransactionLog models*

</div>

---

## 📋 Requirements

```yaml
Runtime:
  - Python: 3.10+
  - Django: 4.x
  - Django REST Framework

Database:
  - SQLite (default)
  - PostgreSQL (production-ready)

External Services:
  - Africa's Talking API (SMS notifications)
  - OpenID Connect Provider (authentication)
```

---

## 🚀 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/smsharon/customerOrders.git
cd customerOrders
```

### 2️⃣ Create Virtual Environment

<table>
<tr>
<th>Linux/Mac</th>
<th>Windows</th>
</tr>
<tr>
<td>

```bash
python -m venv .venv
source .venv/bin/activate
```

</td>
<td>

```cmd
python -m venv .venv
.venv\Scripts\activate
```

</td>
</tr>
</table>

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Africa's Talking API
AFRICASTALKING_USERNAME=your-username
AFRICASTALKING_API_KEY=your-api-key

# OpenID Connect
OIDC_CLIENT_ID=your-client-id
OIDC_CLIENT_SECRET=your-client-secret
OIDC_PROVIDER_URL=https://your-provider.com
```

### 5️⃣ Run Migrations

```bash
python manage.py migrate
```

### 6️⃣ Start Development Server

```bash
python manage.py runserver
```

🎉 **Your application is now running at** `http://127.0.0.1:8000/`

---

## 🧪 Running Tests

### Full Test Suite with Coverage

```bash
pytest --cov=orders
```

### Detailed Coverage Report

```bash
pytest --cov=orders --cov-report=term-missing
```

### Generate HTML Coverage Report

```bash
pytest --cov=orders --cov-report=html
```

---

## 📡 API Endpoints

### 🔑 Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/login/` | User login via OpenID, returns JWT | ❌ |

### 👥 Customers

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/customers/` | Create a new customer | ✅ |
| `GET` | `/api/customers/` | List all customers | ✅ |

### 📦 Inventory

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/inventory/` | Add new inventory item | ✅ |
| `GET` | `/api/inventory/` | List all inventory items | ✅ |

### 🛒 Orders

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/orders/` | Create order & send SMS notification | ✅ |
| `PUT` | `/api/orders/{id}/approve/` | Approve an order | ✅ |
| `GET` | `/api/orders/` | List user's orders | ✅ |

> 💡 **Note:** All protected endpoints require a valid JWT token in the Authorization header:
> ```
> Authorization: Bearer <your-jwt-token>
> ```

---

## 🏗️ Project Structure

```
customerOrders/
├── 📁 orders/              # Main application
│   ├── 📁 migrations/      # Database migrations
│   ├── 📄 models.py        # Data models
│   ├── 📄 views.py         # API views
│   ├── 📄 serializers.py   # DRF serializers
│   ├── 📄 signals.py       # Django signals
│   └── 📄 tests.py         # Unit tests
├── 📁 docs/                # Documentation assets
│   └── 🖼️ ER-DIAGRAM.png   # Database schema diagram
├── 📄 manage.py            # Django management script
├── 📄 requirements.txt     # Python dependencies
└── 📄 README.md            # You are here!
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ using Django**

[⬆ Back to Top](#-customer-orders--backend-challenge-application)

</div>
```

Just copy everything above (including the triple backticks at the start and end) and paste it directly into your README.md file! 📋✨

# Coderr Backend API

A Django REST Framework backend for a freelance marketplace platform connecting business users with customers. This API provides comprehensive functionality for user authentication, profile management, service offers, order processing, and review systems.

## Coderr Frontend
 
You can find the corresponding frontend here: [https://github.com/RobbyRunge/coderr-frontend](https://github.com/RobbyRunge/coderr-frontend)

## 📑 Table of Contents

- [Prerequisites](#-prerequisites)
- [Installation](#️-installation)
- [Features](#-features)
- [Technology Stack](#️-technology-stack)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Testing](#-testing)
- [Authentication](#-authentication)
- [Models](#-models)
- [Development](#-development)
- [License](#-license)
- [Contributing](#-contributing)
- [Support](#-support)

## 📋 Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd modul-9.2-coderr-backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

   **Generate a SECRET_KEY:**
   
   You can generate a secure SECRET_KEY using Python:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   
   Or use this one-liner in PowerShell:
   ```powershell
   python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```
   
   Copy the generated key and paste it into your `.env` file.

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

## 🚀 Features

- **User Authentication & Authorization**
  - Token-based authentication
  - Custom user model with customer/business user types
  - Registration and login endpoints

- **Profile Management**
  - Separate profiles for business and customer users
  - Profile creation, retrieval, and updates
  - File upload support for profile images

- **Offers System**
  - Create, read, update, and delete service offers
  - Multiple offer details with different pricing tiers (basic, standard, premium)
  - Image upload for offers
  - Filtering, searching, and ordering capabilities
  - Dynamic pagination

- **Orders Management**
  - Order creation from offer details
  - Order status tracking (in_progress, completed, cancelled)
  - Order history for customers and business users
  - Order count statistics

- **Reviews & Ratings**
  - Customer reviews for business users
  - 1-5 star rating system
  - Review filtering by business user or reviewer
  - Update and delete review functionality

- **Platform Statistics**
  - Base information endpoint with platform-wide metrics
  - Review count and average ratings
  - Business profile and offer counts

## 🛠️ Technology Stack

- **Framework:** Django 5.2.7
- **API:** Django REST Framework 3.16.1
- **Authentication:** Token-based authentication
- **Database:** SQLite (development)

## 📁 Project Structure

```
coderr-backend/
├── auth_app/              # User authentication & authorization
│   ├── api/
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── models.py          # CustomUser model
│   └── tests/
├── profiles_app/          # User profile management
│   ├── api/
│   ├── models.py          # Profile model
│   └── tests/
├── offers_app/            # Service offers
│   ├── api/
│   ├── models.py          # Offer & OfferDetail models
│   └── tests/
├── orders_app/            # Order processing
│   ├── api/
│   ├── models.py          # Order model
│   └── tests/
├── reviews_app/           # Reviews & ratings
│   ├── api/
│   ├── models.py          # Review model
│   └── tests/
├── base_info_app/         # Platform statistics
│   ├── api/
│   └── tests/
├── core/                  # Project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/                 # User uploaded files
├── manage.py
├── requirements.txt
└── README.md
```

## 🔌 API Endpoints

### Authentication
- `POST /api/registration/` - Register new user (customer or business)
- `POST /api/login/` - User login

### Profiles
- `GET /api/profile/{id}/` - Get profile details
- `PATCH /api/profile/{id}/` - Update profile
- `GET /api/profiles/business/` - List all business profiles
- `GET /api/profiles/customer/` - List all customer profiles

### Offers
- `GET /api/offers/` - List all offers (with filtering & pagination)
- `POST /api/offers/` - Create new offer (business users only)
- `GET /api/offers/{id}/` - Get offer details
- `PATCH /api/offers/{id}/` - Update offer
- `DELETE /api/offers/{id}/` - Delete offer
- `GET /api/offerdetails/{id}/` - Get offer detail full information

### Orders
- `GET /api/orders/` - List user's orders
- `POST /api/orders/` - Create new order
- `GET /api/orders/{id}/` - Get order details
- `PATCH /api/orders/{id}/` - Update order status
- `DELETE /api/orders/{id}/` - Delete order
- `GET /api/order-count/{user_id}/` - Get user's total order count
- `GET /api/completed-order-count/{user_id}/` - Get completed order count

### Reviews
- `GET /api/reviews/` - List reviews (with filtering)
- `POST /api/reviews/` - Create review (customers only)
- `PATCH /api/reviews/{id}/` - Update review (owner only)
- `DELETE /api/reviews/{id}/` - Delete review (owner only)

### Platform Info
- `GET /api/base-info/` - Get platform statistics (no auth required)

## 🧪 Testing

The project includes comprehensive test coverage for all apps.

**Run all tests:**
```bash
python manage.py test
```

**Run tests for specific app:**
```bash
python manage.py test auth_app.tests
python manage.py test profiles_app.tests
python manage.py test offers_app.tests
python manage.py test orders_app.tests
python manage.py test reviews_app.tests
python manage.py test base_info_app.tests
```

**Using VS Code tasks:**
The project includes pre-configured VS Code tasks for running tests. Use `Ctrl+Shift+P` → `Tasks: Run Task` and select the desired test suite.

## 🔐 Authentication

This API uses token-based authentication. After successful registration or login, include the token in the Authorization header:

```
Authorization: Token <your-token-here>
```

## 📝 Models

### CustomUser
- Extends Django's AbstractUser
- Fields: `username`, `email`, `password`, `user_type` (customer/business)

### Profile
- One-to-one relationship with User
- Fields: `username`, `first_name`, `last_name`, `file`, `location`, `tel`, `description`, `working_hours`, `type`, `email`

### Offer
- Created by business users
- Fields: `user`, `title`, `image`, `description`, `created_at`, `updated_at`

### OfferDetail
- Multiple pricing tiers per offer
- Fields: `offer`, `title`, `revisions`, `delivery_time_in_days`, `price`, `features`, `offer_type`

### Order
- Links customers with business users
- Fields: `customer_user`, `business_user`, `title`, `revisions`, `delivery_time_in_days`, `price`, `features`, `offer_type`, `status`, `created_at`, `updated_at`

### Review
- Customer feedback for business users
- Fields: `business_user`, `reviewer`, `rating` (1-5), `description`, `created_at`, `updated_at`

## 🔧 Development

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Include docstrings for classes and methods

### Adding New Features
1. Create models in `models.py`
2. Create serializers in `api/serializers.py`
3. Create views in `api/views.py`
4. Add URL patterns in `api/urls.py`
5. Write tests in `tests/`
6. Run migrations: `python manage.py makemigrations` and `python manage.py migrate`

## 📄 License

This project is part of a developer academy module.

## 👥 Contributing

This is an educational project. For contributions or questions, please contact the repository owner.

## 📞 Support

For issues or questions, please create an issue in the repository.

---

**Note:** This is a development version. For production deployment, ensure to:
- Set `DEBUG=False`
- Use a production-grade database (PostgreSQL, MySQL)
- Configure proper `ALLOWED_HOSTS`
- Set up secure `SECRET_KEY`
- Configure HTTPS
- Set up proper media and static file serving
- Implement rate limiting
- Add comprehensive logging

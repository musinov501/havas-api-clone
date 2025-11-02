# 🛒 Havas Market

**Havas Market** is a modern web platform built with **Django Rest Framework (DRF)** that allows users to explore available meals and products, view detailed information, and create personal “meal lists.”  
Unlike a traditional e-commerce website, **Havas Market** focuses on **product discovery** — not payments or checkout — providing users with an organized and multilingual browsing experience.

---

## ✨ Overview

Havas Market is designed for users who want to:

- Browse a list of available meals and products.
- Read detailed descriptions, including images and multilingual content.
- Add products to a personal **Meal List** (similar to a cart, but not for direct purchases).
- Experience a clean, scalable API built for developers and future front-end integration.

The project follows clean architecture principles and leverages DRF’s modular capabilities to ensure flexibility, readability, and easy testing.

---

## 🧩 Features

### 🥗 Product System
- View products with multilingual titles and descriptions.
- Each product includes fields such as `price`, `discount`, `category`, and `measurement_type`.
- Product translation support using **Django ModelTranslation**.

### 🧺 Meal List (Cart)
- Authenticated users can add meals/products to their personal cart.
- Each cart item stores `quantity`, `notes`, and `estimated_price`.
- Items can be updated or removed at any time.
- The cart acts as a “meal planning list,” not a purchasing cart.

### 👤 Authentication
- Secure user authentication with **JWT** or session tokens.
- Access restrictions for non-authenticated users.
- Users can view only their own meal lists.

### 🧮 Backend Design
- Built with **Django Rest Framework (DRF)** using serializers, viewsets, and mixins.
- Separation of concerns: reusable logic through mixins and utility modules.
- Comprehensive test coverage for all key features.

### 🌍 Multilingual Support
- All translatable fields are handled via `modeltranslation`.
- API responses include language-specific data automatically.

---

## 🧰 Tech Stack

| Category | Technology |
|-----------|-------------|
| **Backend Framework** | Django, Django Rest Framework |
| **Database** | MySQL / PostgreSQL / SQLite |
| **Auth** | JWT / Session Authentication |
| **Internationalization** | Django ModelTranslation |
| **Testing** | DRF `APITestCase` |
| **Styling (optional)** | Bootstrap for front-end integration |
| **Version Control** | Git & GitHub |

---

## 🗂️ Project Structure

havas/
├── apps/
│ ├── products/ # Product models, serializers, and translations
│ ├── cart/ # Cart (Meal List) models, serializers, and views
│ ├── shared/ # Common utilities, mixins, and pagination logic
│ └── users/ # Authentication and profile management
├── core/ # Main Django settings and configurations
└── manage.py



---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/havas-market.git
cd havas-market

2️⃣ Create a virtual environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run migrations
python manage.py migrate

5️⃣ Start the development server
python manage.py runserver


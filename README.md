# Coderr – Backend API

Coderr is a freelance marketplace platform where **business users** can offer services and **customers** can browse, order and review them. This repository contains the Django REST Framework backend.

---

## Tech Stack

- **Python** 3.13
- **Django** 6.0
- **Django REST Framework** 3.16
- **SQLite** (development)
- **django-cors-headers**, **django-filter**, **python-decouple**

---

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the environment file

Create a `.env` file in the `backend/` directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
```

> Generate a secret key with:
>
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create demo data

Populates the database with demo users, offers and reviews so the frontend works out of the box:

```bash
python manage.py create_demo_data
```

**Demo accounts created:**

| Username | Password | Type     |
| -------- | -------- | -------- |
| kevin    | asdasd24 | business |
| anna     | asdasd24 | business |
| andrey   | asdasd   | customer |
| lisa     | asdasd24 | customer |

### 7. Start the development server

```bash
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/api/`.

### 8. (Optional) Create a superuser for the admin panel

```bash
python manage.py createsuperuser
```

Admin panel: `http://127.0.0.1:8000/admin/`

---

## Running Tests

```bash
pytest
```

With coverage report:

```bash
pytest --cov
```

---

## API Endpoints

### Authentication

#### `POST /api/registration/`

Creates a new user account.

**Request Body:**

```json
{
  "username": "exampleUsername",
  "email": "example@mail.de",
  "password": "examplePassword",
  "repeated_password": "examplePassword",
  "type": "customer"
}
```

**Response `201`:**

```json
{
  "token": "...",
  "username": "exampleUsername",
  "email": "example@mail.de",
  "user_id": 123
}
```

**Status Codes:** `201` Created · `400` Bad Request

---

#### `POST /api/login/`

Authenticates a user and returns an auth token.

**Request Body:**

```json
{
  "username": "exampleUsername",
  "password": "examplePassword"
}
```

**Response `200`:**

```json
{
  "token": "...",
  "username": "exampleUsername",
  "email": "example@mail.de",
  "user_id": 123
}
```

**Status Codes:** `200` OK · `400` Bad Request

---

### Profiles

#### `GET /api/profile/{pk}/`

Returns the full profile of a user.

**Permissions:** Authenticated  
**Status Codes:** `200` OK · `401` Unauthorized · `404` Not Found

---

#### `PATCH /api/profile/{pk}/`

Updates profile fields of the authenticated user.

**Permissions:** Owner only  
**Request Body** (all fields optional):

```json
{
  "first_name": "Max",
  "last_name": "Mustermann",
  "location": "Berlin",
  "tel": "987654321",
  "description": "Updated description",
  "working_hours": "10-18",
  "email": "new@example.de",
  "file": "<image file>"
}
```

**Status Codes:** `200` OK · `401` Unauthorized · `403` Forbidden · `404` Not Found

---

#### `GET /api/profiles/business/`

Returns a list of all business user profiles.

**Permissions:** Authenticated  
**Status Codes:** `200` OK · `401` Unauthorized

---

#### `GET /api/profiles/customer/`

Returns a list of all customer profiles.

**Permissions:** Authenticated  
**Status Codes:** `200` OK · `401` Unauthorized

---

### Offers

#### `GET /api/offers/`

Returns a paginated list of offers.

**Query Parameters:**

| Parameter           | Type    | Description                        |
| ------------------- | ------- | ---------------------------------- |
| `creator_id`        | integer | Filter by creator                  |
| `min_price`         | float   | Minimum price filter               |
| `max_delivery_time` | integer | Maximum delivery time in days      |
| `ordering`          | string  | `updated_at` or `min_price`        |
| `search`            | string  | Searches `title` and `description` |
| `page_size`         | integer | Results per page                   |

**Permissions:** None required  
**Status Codes:** `200` OK · `400` Bad Request

---

#### `POST /api/offers/`

Creates a new offer. Must include exactly 3 details (basic, standard, premium).

**Permissions:** Business users only

**Request Body:**

```json
{
  "title": "Grafikdesign-Paket",
  "description": "A complete graphic design package.",
  "details": [
    {
      "title": "Basic",
      "revisions": 2,
      "delivery_time_in_days": 5,
      "price": 100,
      "features": ["Logo"],
      "offer_type": "basic"
    },
    {
      "title": "Standard",
      "revisions": 5,
      "delivery_time_in_days": 7,
      "price": 200,
      "features": ["Logo", "Card"],
      "offer_type": "standard"
    },
    {
      "title": "Premium",
      "revisions": 10,
      "delivery_time_in_days": 10,
      "price": 500,
      "features": ["Logo", "Card", "Flyer"],
      "offer_type": "premium"
    }
  ]
}
```

**Status Codes:** `201` Created · `400` Bad Request · `401` Unauthorized · `403` Forbidden

---

#### `GET /api/offers/{id}/`

Returns the details of a specific offer.

**Permissions:** Authenticated  
**Status Codes:** `200` OK · `401` Unauthorized · `404` Not Found

---

#### `PATCH /api/offers/{id}/`

Updates fields of a specific offer. Details are matched by `offer_type`.

**Permissions:** Owner only  
**Status Codes:** `200` OK · `400` Bad Request · `401` Unauthorized · `403` Forbidden · `404` Not Found

---

#### `DELETE /api/offers/{id}/`

Deletes a specific offer.

**Permissions:** Owner only  
**Status Codes:** `204` No Content · `401` Unauthorized · `403` Forbidden · `404` Not Found

---

#### `GET /api/offerdetails/{id}/`

Returns a single offer detail object.

**Permissions:** Authenticated  
**Status Codes:** `200` OK · `401` Unauthorized · `404` Not Found

---

### Orders

#### `GET /api/orders/`

Returns all orders where the authenticated user is either the customer or the business user.

**Permissions:** Authenticated  
**Status Codes:** `200` OK · `401` Unauthorized

---

#### `POST /api/orders/`

Creates a new order based on an offer detail.

**Permissions:** Customer users only

**Request Body:**

```json
{ "offer_detail_id": 1 }
```

**Status Codes:** `201` Created · `400` Bad Request · `401` Unauthorized · `403` Forbidden · `404` Not Found

---

#### `PATCH /api/orders/{id}/`

Updates the status of an order.

**Permissions:** Business user of the order only

**Request Body:**

```json
{ "status": "completed" }
```

Allowed values: `in_progress`, `completed`, `cancelled`

**Status Codes:** `200` OK · `400` Bad Request · `401` Unauthorized · `403` Forbidden · `404` Not Found

---

#### `DELETE /api/orders/{id}/`

Deletes an order.

**Permissions:** Admin (staff) only  
**Status Codes:** `204` No Content · `401` Unauthorized · `403` Forbidden · `404` Not Found

---

#### `GET /api/order-count/{business_user_id}/`

Returns the number of in-progress orders for a business user.

**Permissions:** Authenticated  
**Response:** `{ "order_count": 5 }`  
**Status Codes:** `200` OK · `401` Unauthorized · `404` Not Found

---

#### `GET /api/completed-order-count/{business_user_id}/`

Returns the number of completed orders for a business user.

**Permissions:** Authenticated  
**Response:** `{ "completed_order_count": 10 }`  
**Status Codes:** `200` OK · `401` Unauthorized · `404` Not Found

---

### Reviews

#### `GET /api/reviews/`

Returns a list of all reviews, with optional filtering and ordering.

**Query Parameters:**

| Parameter          | Type    | Description              |
| ------------------ | ------- | ------------------------ |
| `business_user_id` | integer | Filter by business user  |
| `reviewer_id`      | integer | Filter by reviewer       |
| `ordering`         | string  | `updated_at` or `rating` |

**Permissions:** Authenticated  
**Status Codes:** `200` OK · `401` Unauthorized

---

#### `POST /api/reviews/`

Creates a new review. One review per business user per customer.

**Permissions:** Customer users only

**Request Body:**

```json
{
  "business_user": 2,
  "rating": 4,
  "description": "Great service!"
}
```

**Status Codes:** `201` Created · `400` Bad Request · `401` Unauthorized · `403` Forbidden

---

#### `PATCH /api/reviews/{id}/`

Updates `rating` and/or `description` of an existing review.

**Permissions:** Review author only  
**Status Codes:** `200` OK · `400` Bad Request · `401` Unauthorized · `403` Forbidden · `404` Not Found

---

#### `DELETE /api/reviews/{id}/`

Deletes a review.

**Permissions:** Review author only  
**Status Codes:** `204` No Content · `401` Unauthorized · `403` Forbidden · `404` Not Found

---

### Platform Info

#### `GET /api/base-info/`

Returns aggregated platform statistics.

**Permissions:** None required

**Response:**

```json
{
  "review_count": 10,
  "average_rating": 4.6,
  "business_profile_count": 45,
  "offer_count": 150
}
```

**Status Codes:** `200` OK

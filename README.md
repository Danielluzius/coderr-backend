# Coderr – Backend API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.16-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

Coderr is a freelance marketplace platform where **business users** can offer services and **customers** can browse, order and review them.

This repository contains the **Django REST Framework backend API**. It is designed to work together with the [coderr-frontend](https://github.com/Danielluzius/coderr-frontend) – the matching HTML/CSS/JS frontend.

---

## Tech Stack

- **Python** 3.13
- **Django** 6.0
- **Django REST Framework** 3.16
- **SQLite** (development)
- **django-cors-headers**, **django-filter**, **python-decouple**

---

## Setup

### Prerequisites

Before you start, make sure the following are installed on your machine:

- **Python 3.10+** → [python.org/downloads](https://www.python.org/downloads/)
- **Git** → [git-scm.com](https://git-scm.com/)

Verify your installation by running:

```bash
python --version
git --version
```

Both commands should print a version number. If you see an error, install the missing tool first.

---

### 1. Clone the repository

Open a terminal, navigate to the folder where you want to save the project, then run:

```bash
git clone <repository-url>
```

Afterwards navigate into the **backend** folder – all following commands must be run from here:

```bash
cd <repository-name>/backend
```

> **Tip:** You can confirm you are in the right folder when you see `manage.py` listed after running `ls` (macOS/Linux) or `dir` (Windows).

---

### 2. Create a virtual environment

A virtual environment keeps the project's dependencies isolated from the rest of your system.

```bash
python -m venv .venv
```

Then **activate** it:

```bash
# Windows (PowerShell)
.venv\Scripts\activate

# Windows (Command Prompt)
.venv\Scripts\activate.bat

# macOS / Linux
source .venv/bin/activate
```

> **How to tell it worked:** Your terminal prompt should now start with `(.venv)`.

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

This installs Django, Django REST Framework and all other required packages.

---

### 4. Create the environment file

A `.env.example` file is included in the repository. Copy it to create your own `.env`:

**Windows (PowerShell):**

```powershell
Copy-Item .env.example .env
```

**macOS / Linux:**

```bash
cp .env.example .env
```

Open the newly created `.env` with any text editor. It looks like this:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
```

Now replace `your-secret-key-here` with a real secret key. To generate one, run Python interactively:

```bash
python
```

Then inside the Python shell:

```python
import secrets
print(secrets.token_urlsafe(50))
exit()
```

Copy the printed string and paste it as the value for `SECRET_KEY` in your `.env` file. The result should look something like:

```env
SECRET_KEY=3xAmPl3K3y_abc123xyz...
DEBUG=True
```

---

### 5. Run migrations

This creates the database tables:

```bash
python manage.py migrate
```

> If you see an error like `No module named django`, make sure your virtual environment is activated (step 2).

---

### 6. (Optional) Load demo data

This populates the database with demo users, offers and reviews. Without this step the API works fine, but the frontend will show an empty state.

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

> The command is safe to run multiple times – it will not create duplicate data.

> **Note:** To see the full application, you also need the frontend running. See [Related Projects](#related-projects).

---

### 7. Start the development server

```bash
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/api/`.

Leave this terminal running while you work. Stop the server at any time with `Ctrl + C`.

---

### 8. (Optional) Create an admin account

If you want access to the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username and password. Then open `http://127.0.0.1:8000/admin/` in your browser.

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

<details>
<summary><code>POST /api/registration/</code> – Create a new user account</summary>

**Permissions:** None required

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

</details>

<details>
<summary><code>POST /api/login/</code> – Authenticate and receive a token</summary>

**Permissions:** None required

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

</details>

---

### Profiles

<details>
<summary><code>GET /api/profile/{pk}/</code> – Get a user profile</summary>

**Permissions:** Authenticated

**Status Codes:** `200` OK · `401` Unauthorized · `404` Not Found

</details>

<details>
<summary><code>PATCH /api/profile/{pk}/</code> – Update own profile</summary>

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

</details>

<details>
<summary><code>GET /api/profiles/business/</code> – List all business profiles</summary>

**Permissions:** Authenticated

**Status Codes:** `200` OK · `401` Unauthorized

</details>

<details>
<summary><code>GET /api/profiles/customer/</code> – List all customer profiles</summary>

**Permissions:** Authenticated

**Status Codes:** `200` OK · `401` Unauthorized

</details>

---

### Offers

<details>
<summary><code>GET /api/offers/</code> – List offers (paginated)</summary>

**Permissions:** None required

**Query Parameters:**

| Parameter           | Type    | Description                        |
| ------------------- | ------- | ---------------------------------- |
| `creator_id`        | integer | Filter by creator                  |
| `min_price`         | float   | Minimum price filter               |
| `max_delivery_time` | integer | Maximum delivery time in days      |
| `ordering`          | string  | `updated_at` or `min_price`        |
| `search`            | string  | Searches `title` and `description` |
| `page_size`         | integer | Results per page                   |

**Status Codes:** `200` OK · `400` Bad Request

</details>

<details>
<summary><code>POST /api/offers/</code> – Create a new offer</summary>

**Permissions:** Business users only

Must include exactly 3 details (`basic`, `standard`, `premium`).

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

</details>

<details>
<summary><code>GET /api/offers/{id}/</code> – Get a specific offer</summary>

**Permissions:** Authenticated

**Status Codes:** `200` OK · `401` Unauthorized · `404` Not Found

</details>

<details>
<summary><code>PATCH /api/offers/{id}/</code> – Update an offer</summary>

**Permissions:** Owner only

Details are matched by `offer_type`. Only provided fields are updated.

**Status Codes:** `200` OK · `400` Bad Request · `401` Unauthorized · `403` Forbidden · `404` Not Found

</details>

<details>
<summary><code>DELETE /api/offers/{id}/</code> – Delete an offer</summary>

**Permissions:** Owner only

**Status Codes:** `204` No Content · `401` Unauthorized · `403` Forbidden · `404` Not Found

</details>

<details>
<summary><code>GET /api/offerdetails/{id}/</code> – Get a single offer detail</summary>

**Permissions:** Authenticated

**Status Codes:** `200` OK · `401` Unauthorized · `404` Not Found

</details>

---

### Orders

<details>
<summary><code>GET /api/orders/</code> – List orders for the current user</summary>

**Permissions:** Authenticated

Returns orders where the authenticated user is either the customer or the business user.

**Status Codes:** `200` OK · `401` Unauthorized

</details>

<details>
<summary><code>POST /api/orders/</code> – Create a new order</summary>

**Permissions:** Customer users only

**Request Body:**

```json
{ "offer_detail_id": 1 }
```

**Status Codes:** `201` Created · `400` Bad Request · `401` Unauthorized · `403` Forbidden · `404` Not Found

</details>

<details>
<summary><code>PATCH /api/orders/{id}/</code> – Update order status</summary>

**Permissions:** Business user of the order only

**Request Body:**

```json
{ "status": "completed" }
```

Allowed values: `in_progress`, `completed`, `cancelled`

**Status Codes:** `200` OK · `400` Bad Request · `401` Unauthorized · `403` Forbidden · `404` Not Found

</details>

<details>
<summary><code>DELETE /api/orders/{id}/</code> – Delete an order</summary>

**Permissions:** Admin (staff) only

**Status Codes:** `204` No Content · `401` Unauthorized · `403` Forbidden · `404` Not Found

</details>

<details>
<summary><code>GET /api/order-count/{business_user_id}/</code> – Count in-progress orders</summary>

**Permissions:** Authenticated

**Response:** `{ "order_count": 5 }`

**Status Codes:** `200` OK · `401` Unauthorized · `404` Not Found

</details>

<details>
<summary><code>GET /api/completed-order-count/{business_user_id}/</code> – Count completed orders</summary>

**Permissions:** Authenticated

**Response:** `{ "completed_order_count": 10 }`

**Status Codes:** `200` OK · `401` Unauthorized · `404` Not Found

</details>

---

### Reviews

<details>
<summary><code>GET /api/reviews/</code> – List all reviews</summary>

**Permissions:** Authenticated

**Query Parameters:**

| Parameter          | Type    | Description              |
| ------------------ | ------- | ------------------------ |
| `business_user_id` | integer | Filter by business user  |
| `reviewer_id`      | integer | Filter by reviewer       |
| `ordering`         | string  | `updated_at` or `rating` |

**Status Codes:** `200` OK · `401` Unauthorized

</details>

<details>
<summary><code>POST /api/reviews/</code> – Create a review</summary>

**Permissions:** Customer users only. One review per business user.

**Request Body:**

```json
{
  "business_user": 2,
  "rating": 4,
  "description": "Great service!"
}
```

**Status Codes:** `201` Created · `400` Bad Request · `401` Unauthorized · `403` Forbidden

</details>

<details>
<summary><code>PATCH /api/reviews/{id}/</code> – Update a review</summary>

**Permissions:** Review author only

Editable fields: `rating`, `description`

**Status Codes:** `200` OK · `400` Bad Request · `401` Unauthorized · `403` Forbidden · `404` Not Found

</details>

<details>
<summary><code>DELETE /api/reviews/{id}/</code> – Delete a review</summary>

**Permissions:** Review author only

**Status Codes:** `204` No Content · `401` Unauthorized · `403` Forbidden · `404` Not Found

</details>

---

### Platform Info

<details>
<summary><code>GET /api/base-info/</code> – Platform statistics</summary>

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

</details>

---

## Related Projects

- **Frontend:** [coderr-frontend](https://github.com/Danielluzius/coderr-frontend) – The matching HTML/CSS/JS frontend for this API.

---

## License

MIT

# Coderr – Backend API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.16-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

🌐 **Deutsch** · [English](README.md)

</div>

Coderr ist eine Freelance-Marktplatz-Plattform, auf der **Geschäftsnutzer** Dienstleistungen anbieten können und **Kunden** diese durchsuchen, bestellen und bewerten können.

Dieses Repository enthält die **Django REST Framework Backend-API**. Sie ist dafür ausgelegt, zusammen mit dem [coderr-frontend](https://github.com/Danielluzius/coderr-frontend) zu funktionieren – dem passenden HTML/CSS/JS-Frontend.

---

## Tech Stack

- **Python** 3.13
- **Django** 6.0
- **Django REST Framework** 3.16
- **SQLite** (Entwicklung)
- **django-cors-headers**, **django-filter**, **python-decouple**

---

## Setup

### Voraussetzungen

Stelle sicher, dass folgendes auf deinem Rechner installiert ist:

- **Python 3.10+** → [python.org/downloads](https://www.python.org/downloads/)
- **Git** → [git-scm.com](https://git-scm.com/)

Überprüfe die Installation mit:

```bash
python --version
git --version
```

Beide Befehle sollten eine Versionsnummer ausgeben. Falls eine Fehlermeldung erscheint, installiere das fehlende Tool zuerst.

---

### 1. Repository klonen

Öffne ein Terminal, navigiere zum gewünschten Ordner und führe aus:

```bash
git clone <repository-url>
```

Wechsle danach in den **backend**-Ordner – alle folgenden Befehle müssen von hier ausgeführt werden:

```bash
cd <repository-name>/backend
```

> **Tipp:** Du bist im richtigen Ordner, wenn du `manage.py` nach dem Ausführen von `ls` (macOS/Linux) bzw. `dir` (Windows) siehst.

---

### 2. Virtuelle Umgebung erstellen

Eine virtuelle Umgebung hält die Abhängigkeiten des Projekts vom Rest des Systems getrennt.

```bash
python -m venv .venv
```

Danach **aktivieren**:

```bash
# Windows (PowerShell)
.venv\Scripts\activate

# Windows (Command Prompt)
.venv\Scripts\activate.bat

# macOS / Linux
source .venv/bin/activate
```

> **Erkennungsmerkmal:** Dein Terminal-Prompt beginnt jetzt mit `(.venv)`.

---

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

Hiermit werden Django, Django REST Framework und alle weiteren Pakete installiert.

---

### 4. Umgebungsdatei erstellen

Im Repository liegt eine `.env.example`-Datei. Kopiere sie, um deine eigene `.env` zu erstellen:

**Windows (PowerShell):**

```powershell
Copy-Item .env.example .env
```

**macOS / Linux:**

```bash
cp .env.example .env
```

Öffne die neu erstellte `.env` mit einem Texteditor. Sie sieht so aus:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
```

Ersetze `your-secret-key-here` durch einen echten Secret Key. Um einen zu generieren, starte Python interaktiv:

```bash
python
```

Dann im Python-Shell:

```python
import secrets
print(secrets.token_urlsafe(50))
exit()
```

Kopiere den ausgegebenen String und füge ihn als Wert für `SECRET_KEY` in deine `.env`-Datei ein. Das Ergebnis sollte etwa so aussehen:

```env
SECRET_KEY=3xAmPl3K3y_abc123xyz...
DEBUG=True
```

---

### 5. Migrationen ausführen

Erstellt die Datenbanktabellen:

```bash
python manage.py migrate
```

> Falls eine Fehlermeldung wie `No module named django` erscheint, stelle sicher dass die virtuelle Umgebung aktiviert ist (Schritt 2).

---

### 6. (Optional) Demo-Daten laden

Befüllt die Datenbank mit Demo-Nutzern, Angeboten und Bewertungen. Ohne diesen Schritt funktioniert die API problemlos, das Frontend zeigt jedoch einen leeren Zustand.

```bash
python manage.py create_demo_data
```

**Erstellte Demo-Accounts:**

| Benutzername | Passwort | Typ      |
| ------------ | -------- | -------- |
| kevin        | asdasd24 | business |
| anna         | asdasd24 | business |
| andrey       | asdasd   | customer |
| lisa         | asdasd24 | customer |

> Der Befehl kann mehrfach ausgeführt werden – es werden keine doppelten Daten erstellt.

> **Hinweis:** Um die vollständige Anwendung zu sehen, muss auch das Frontend laufen. Siehe [Verwandte Projekte](#verwandte-projekte).

---

### 7. Entwicklungsserver starten

```bash
python manage.py runserver
```

Die API ist jetzt erreichbar unter `http://127.0.0.1:8000/api/`.

Lass dieses Terminal geöffnet während du arbeitest. Stoppe den Server jederzeit mit `Ctrl + C`.

---

### 8. (Optional) Admin-Account erstellen

Für den Zugang zum Django Admin-Panel:

```bash
python manage.py createsuperuser
```

Folge den Anweisungen zur Eingabe von Benutzername und Passwort. Danach öffne `http://127.0.0.1:8000/admin/` im Browser.

---

## Tests ausführen

```bash
pytest
```

Mit Coverage-Bericht:

```bash
pytest --cov
```

---

## API-Endpunkte

### Authentifizierung

<details>
<summary><code>POST /api/registration/</code> – Neuen Benutzer registrieren</summary>

**Berechtigung:** Keine erforderlich

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
<summary><code>POST /api/login/</code> – Anmelden und Token erhalten</summary>

**Berechtigung:** Keine erforderlich

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

### Profile

<details>
<summary><code>GET /api/profile/{pk}/</code> – Benutzerprofil abrufen</summary>

**Berechtigung:** Angemeldet

**Status Codes:** `200` OK · `401` Unauthorized · `404` Not Found

</details>

<details>
<summary><code>PATCH /api/profile/{pk}/</code> – Eigenes Profil aktualisieren</summary>

**Berechtigung:** Nur Eigentümer

**Request Body** (alle Felder optional):

```json
{
  "first_name": "Max",
  "last_name": "Mustermann",
  "location": "Berlin",
  "tel": "987654321",
  "description": "Aktualisierte Beschreibung",
  "working_hours": "10-18",
  "email": "neu@example.de",
  "file": "<Bilddatei>"
}
```

**Status Codes:** `200` OK · `401` Unauthorized · `403` Forbidden · `404` Not Found

</details>

<details>
<summary><code>GET /api/profiles/business/</code> – Alle Geschäftsprofile auflisten</summary>

**Berechtigung:** Angemeldet

**Status Codes:** `200` OK · `401` Unauthorized

</details>

<details>
<summary><code>GET /api/profiles/customer/</code> – Alle Kundenprofile auflisten</summary>

**Berechtigung:** Angemeldet

**Status Codes:** `200` OK · `401` Unauthorized

</details>

---

### Angebote

<details>
<summary><code>GET /api/offers/</code> – Angebote auflisten (paginiert)</summary>

**Berechtigung:** Keine erforderlich

**Query-Parameter:**

| Parameter           | Typ     | Beschreibung                       |
| ------------------- | ------- | ---------------------------------- |
| `creator_id`        | integer | Nach Ersteller filtern             |
| `min_price`         | float   | Mindestpreis-Filter                |
| `max_delivery_time` | integer | Maximale Lieferzeit in Tagen       |
| `ordering`          | string  | `updated_at` oder `min_price`      |
| `search`            | string  | Sucht in `title` und `description` |
| `page_size`         | integer | Ergebnisse pro Seite               |

**Status Codes:** `200` OK · `400` Bad Request

</details>

<details>
<summary><code>POST /api/offers/</code> – Neues Angebot erstellen</summary>

**Berechtigung:** Nur Geschäftsnutzer

Muss genau 3 Details enthalten (`basic`, `standard`, `premium`).

**Request Body:**

```json
{
  "title": "Grafikdesign-Paket",
  "description": "Ein vollständiges Grafikdesign-Paket.",
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
      "features": ["Logo", "Visitenkarte"],
      "offer_type": "standard"
    },
    {
      "title": "Premium",
      "revisions": 10,
      "delivery_time_in_days": 10,
      "price": 500,
      "features": ["Logo", "Visitenkarte", "Flyer"],
      "offer_type": "premium"
    }
  ]
}
```

**Status Codes:** `201` Created · `400` Bad Request · `401` Unauthorized · `403` Forbidden

</details>

<details>
<summary><code>GET /api/offers/{id}/</code> – Einzelnes Angebot abrufen</summary>

**Berechtigung:** Angemeldet

**Status Codes:** `200` OK · `401` Unauthorized · `404` Not Found

</details>

<details>
<summary><code>PATCH /api/offers/{id}/</code> – Angebot aktualisieren</summary>

**Berechtigung:** Nur Eigentümer

Details werden per `offer_type` zugeordnet. Nur angegebene Felder werden aktualisiert.

**Status Codes:** `200` OK · `400` Bad Request · `401` Unauthorized · `403` Forbidden · `404` Not Found

</details>

<details>
<summary><code>DELETE /api/offers/{id}/</code> – Angebot löschen</summary>

**Berechtigung:** Nur Eigentümer

**Status Codes:** `204` No Content · `401` Unauthorized · `403` Forbidden · `404` Not Found

</details>

<details>
<summary><code>GET /api/offerdetails/{id}/</code> – Einzelnes Angebotsdetail abrufen</summary>

**Berechtigung:** Angemeldet

**Status Codes:** `200` OK · `401` Unauthorized · `404` Not Found

</details>

---

### Bestellungen

<details>
<summary><code>GET /api/orders/</code> – Bestellungen des aktuellen Nutzers auflisten</summary>

**Berechtigung:** Angemeldet

Gibt Bestellungen zurück, bei denen der Nutzer Kunde oder Geschäftsnutzer ist.

**Status Codes:** `200` OK · `401` Unauthorized

</details>

<details>
<summary><code>POST /api/orders/</code> – Neue Bestellung erstellen</summary>

**Berechtigung:** Nur Kunden

**Request Body:**

```json
{ "offer_detail_id": 1 }
```

**Status Codes:** `201` Created · `400` Bad Request · `401` Unauthorized · `403` Forbidden · `404` Not Found

</details>

<details>
<summary><code>PATCH /api/orders/{id}/</code> – Bestellstatus aktualisieren</summary>

**Berechtigung:** Nur Geschäftsnutzer der Bestellung

**Request Body:**

```json
{ "status": "completed" }
```

Erlaubte Werte: `in_progress`, `completed`, `cancelled`

**Status Codes:** `200` OK · `400` Bad Request · `401` Unauthorized · `403` Forbidden · `404` Not Found

</details>

<details>
<summary><code>DELETE /api/orders/{id}/</code> – Bestellung löschen</summary>

**Berechtigung:** Nur Admins (Staff)

**Status Codes:** `204` No Content · `401` Unauthorized · `403` Forbidden · `404` Not Found

</details>

<details>
<summary><code>GET /api/order-count/{business_user_id}/</code> – Aktive Bestellungen zählen</summary>

**Berechtigung:** Angemeldet

**Response:** `{ "order_count": 5 }`

**Status Codes:** `200` OK · `401` Unauthorized · `404` Not Found

</details>

<details>
<summary><code>GET /api/completed-order-count/{business_user_id}/</code> – Abgeschlossene Bestellungen zählen</summary>

**Berechtigung:** Angemeldet

**Response:** `{ "completed_order_count": 10 }`

**Status Codes:** `200` OK · `401` Unauthorized · `404` Not Found

</details>

---

### Bewertungen

<details>
<summary><code>GET /api/reviews/</code> – Alle Bewertungen auflisten</summary>

**Berechtigung:** Angemeldet

**Query-Parameter:**

| Parameter          | Typ     | Beschreibung                 |
| ------------------ | ------- | ---------------------------- |
| `business_user_id` | integer | Nach Geschäftsnutzer filtern |
| `reviewer_id`      | integer | Nach Bewerter filtern        |
| `ordering`         | string  | `updated_at` oder `rating`   |

**Status Codes:** `200` OK · `401` Unauthorized

</details>

<details>
<summary><code>POST /api/reviews/</code> – Bewertung erstellen</summary>

**Berechtigung:** Nur Kunden. Eine Bewertung pro Geschäftsnutzer.

**Request Body:**

```json
{
  "business_user": 2,
  "rating": 4,
  "description": "Toller Service!"
}
```

**Status Codes:** `201` Created · `400` Bad Request · `401` Unauthorized · `403` Forbidden

</details>

<details>
<summary><code>PATCH /api/reviews/{id}/</code> – Bewertung aktualisieren</summary>

**Berechtigung:** Nur Autor der Bewertung

Bearbeitbare Felder: `rating`, `description`

**Status Codes:** `200` OK · `400` Bad Request · `401` Unauthorized · `403` Forbidden · `404` Not Found

</details>

<details>
<summary><code>DELETE /api/reviews/{id}/</code> – Bewertung löschen</summary>

**Berechtigung:** Nur Autor der Bewertung

**Status Codes:** `204` No Content · `401` Unauthorized · `403` Forbidden · `404` Not Found

</details>

---

### Plattform-Info

<details>
<summary><code>GET /api/base-info/</code> – Plattform-Statistiken</summary>

**Berechtigung:** Keine erforderlich

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

## Verwandte Projekte

- **Frontend:** [coderr-frontend](https://github.com/Danielluzius/coderr-frontend) – Das passende HTML/CSS/JS-Frontend für diese API.

---

## Lizenz

MIT

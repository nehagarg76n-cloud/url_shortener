# 🔗 URL Shortener API

A simple and efficient URL Shortener built with **FastAPI**, **SQLAlchemy**, and **SQLite**. This project allows users to create short URLs, retrieve all shortened URLs, redirect to the original website, and delete existing short URLs.

## 🚀 Features

- ✨ Shorten long URLs
- 🔗 Redirect using short URLs
- 📋 Retrieve all shortened URLs
- 🗑️ Delete shortened URLs
- 💾 SQLite database for persistent storage
- 📖 Interactive API documentation with Swagger UI
- 🌐 CORS enabled for frontend integration

---

## 🛠️ Tech Stack

- **Backend:** FastAPI
- **Frontend**:React
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Server:** Uvicorn

---

## 📂 Project Structure

```text
url-shortener/
│── main.py
│── urls.db
│── frontend
│── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/url-shortener.git
cd url-shortener
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

---

## 📖 API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## 📌 API Endpoints

### Create Short URL

**POST** `/shorten`

Request

```json
{
  "original_url": "https://www.youtube.com"
}
```

Response

```json
{
  "original_url": "https://www.youtube.com",
  "short_code": "Ab12Cd",
  "short_url": "http://127.0.0.1:8000/Ab12Cd"
}
```

---

### Redirect to Original URL

**GET** `/{short_code}`

Example

```
http://127.0.0.1:8000/Ab12Cd
```

This automatically redirects the user to the original website.

---

### Get All URLs

**GET** `/all`

Returns all shortened URLs stored in the database.

---

### Delete URL

**DELETE** `/delete/{short_code}`

Example

```
DELETE /delete/Ab12Cd
```

---

## 🗄️ Database

This project uses **SQLite** for storing URL mappings.

Table Structure

| Column | Type |
|--------|------|
| id | Integer |
| original_url | String |
| short_code | String |

---

## 🧪 Example Workflow

1. Send a POST request to `/shorten`.
2. Receive a generated short URL.
3. Open the short URL in a browser.
4. The application redirects to the original website.
5. View all shortened URLs using `/all`.
6. Delete URLs when no longer needed.

---

## 🔮 Future Improvements

- User authentication
- Custom short URLs
- Click analytics
- QR Code generation
- URL expiration
- PostgreSQL/MySQL support
- Docker support
- React frontend
- Admin dashboard

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push your branch.
5. Open a Pull Request.

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Neha Garg**

GitHub: https://github.com/nehagarg76n-cloud

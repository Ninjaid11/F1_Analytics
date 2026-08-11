# 🏁 F1 Analytics

A web application for analyzing and comparing Formula 1 drivers using FastAPI and LLM.

---

## Features
- **Compare two F1 drivers** with a detailed report.  
- **Race analytics and predictions** using the Gemini 2.5 Flash model.  
- **Scraping driver and race data** using BeautifulSoup.  
- **PostgreSQL integration via Docker** for data storage.

---

## Technologies
- **Language**: Python 3.11  
- **Backend**: FastAPI  
- **Database**: PostgreSQL + SQLAlchemy  
- **LLM**: Gemini 2.5 Flash  
- **Scraping**: BeautifulSoup  
- **Containerization**: Docker  

---

## Installation & Running

1. Clone the repository:
```bash
git clone https://github.com/Ninjaid11/F1_Analytics
cd f1_analytics
```

2. Create a .env file and fill it in:
```bash
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=db
DB_PORT=5432
DB_NAME=f1_db
API_KEY=your_key
```
3. Build and run using Docker Compose:
```bash
docker compose build
docker compose up
```

4. The application will be available at:
http://localhost:8000

---

# AeroFleet Manager - Backend API

Sistema di gestione flotta per aeroclub con FastAPI e PostgreSQL.

## ✨ Caratteristiche

- 🔐 Autenticazione JWT con gestione ruoli
- ✈️ Gestione completa aeromobili
- 📊 API RESTful documentata (Swagger/OpenAPI)
- 🗄️ PostgreSQL database
- 🚀 Pronto per deploy su Render.com

## 📦 Struttura Progetto

```
aerofleet-backend-v2/
├── main.py                 # Applicazione FastAPI
├── init_db.py             # Script inizializzazione DB
├── requirements.txt       # Dipendenze Python
├── runtime.txt           # Versione Python
├── build.sh              # Script build Render
├── render.yaml           # Config Render.com
├── .env.example          # Template variabili ambiente
└── app/
    ├── core/             # Configurazione e utilities
    │   ├── config.py     # Settings
    │   ├── database.py   # Database setup
    │   └── security.py   # Auth e JWT
    ├── models/           # SQLAlchemy models
    │   ├── user.py
    │   └── aircraft.py
    ├── schemas/          # Pydantic schemas
    │   ├── auth.py
    │   └── aircraft.py
    └── api/endpoints/    # API routes
        ├── auth.py       # Login/Register
        └── aircraft.py   # CRUD aeromobili
```

## 🚀 Quick Start Locale

### 1. Requisiti
- Python 3.11+
- PostgreSQL 14+

### 2. Setup

```bash
# Clone o estrai il progetto
cd aerofleet-backend-v2

# Crea virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Installa dipendenze
pip install -r requirements.txt

# Configura .env
cp .env.example .env
# Modifica .env con le tue credenziali database

# Inizializza database
python init_db.py

# Avvia server
uvicorn main:app --reload
```

### 3. Testa API
- Docs: http://localhost:8000/api/docs
- Health: http://localhost:8000/health

## 🌐 Deploy su Render.com

### Passaggi Rapidi

1. **Push su GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/aerofleet-backend.git
git push -u origin main
```

2. **Render.com**
- Crea account su render.com
- New PostgreSQL → Nome: `aerofleet-db`
- New Web Service → Connetti GitHub repo
- Render rileverà automaticamente `render.yaml`
- Click "Create Web Service"

3. **Verifica**
- Aspetta deploy completo (3-5 minuti)
- Testa: `https://tuo-servizio.onrender.com/health`
- Docs: `https://tuo-servizio.onrender.com/api/docs`

## 🔑 Credenziali Default

```
Username: admin
Password: admin123
```

**⚠️ IMPORTANTE: Cambia la password dopo il primo login!**

## 📝 API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Registra nuovo utente
- `POST /api/v1/auth/login` - Login (ottieni JWT token)
- `GET /api/v1/auth/me` - Info utente corrente

### Aircraft

- `GET /api/v1/aircraft` - Lista aeromobili
- `POST /api/v1/aircraft` - Crea aeromobile (admin/manager)
- `GET /api/v1/aircraft/{id}` - Dettagli aeromobile
- `PUT /api/v1/aircraft/{id}` - Aggiorna aeromobile (admin/manager)
- `DELETE /api/v1/aircraft/{id}` - Elimina aeromobile (admin)

## 🔐 Autenticazione

### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### Usa Token
```bash
curl -X GET "http://localhost:8000/api/v1/aircraft" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 👥 Ruoli Utente

- **admin**: Accesso completo
- **manager**: Gestione aeromobili e manutenzioni
- **mechanic**: Aggiornamento work orders
- **pilot**: Registrazione voli
- **viewer**: Solo lettura

## 🛠️ Tecnologie

- **FastAPI** 0.104.1 - Framework web
- **SQLAlchemy** 2.0.23 - ORM
- **PostgreSQL** - Database
- **Pydantic** 2.5.0 - Validazione dati
- **JWT** - Autenticazione
- **Uvicorn** - ASGI server

## 📊 Database

Il database viene creato automaticamente con:
- Tabella `users` - Utenti sistema
- Tabella `aircraft` - Aeromobili
- Utente admin predefinito

## 🔧 Troubleshooting

### Build Failed
- Verifica che `requirements.txt` sia corretto
- Controlla Python version in `runtime.txt`
- Vedi logs Render per dettagli

### Database Connection Error
- Verifica che `DATABASE_URL` sia configurato
- Usa "Internal Database URL" su Render
- Aspetta che database sia "Available"

### 502 Bad Gateway
- Verifica start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Controlla logs per errori startup

## 📚 Documentazione

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Render Docs**: https://render.com/docs
- **API Docs**: Disponibili su `/api/docs` dopo deploy

## 🤝 Supporto

Per problemi con:
- **Deploy**: Controlla i logs su Render dashboard
- **API**: Consulta `/api/docs` per esempi
- **Database**: Verifica variabili d'ambiente

## 📄 Licenza

MIT License

---

**Fatto con ❤️ per la gestione sicura delle flotte aeronautiche**

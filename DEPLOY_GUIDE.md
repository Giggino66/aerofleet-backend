# 🚀 Deploy su Render.com — Istruzioni Precise

## PASSO 1 — Carica il codice su GitHub

### 1.1 Crea un repository su GitHub
1. Vai su **https://github.com/new**
2. Inserisci il nome: `aerofleet-backend`
3. Seleziona **Private** o Public
4. **NON** spuntare "Add a README file"
5. Click **"Create repository"**

### 1.2 Inizializza e carica il codice
Apri un terminale nella cartella `aerofleet-final` e lancia:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/TUO_USERNAME/aerofleet-backend.git
git push -u origin main
```

---

## PASSO 2 — Crea il Database PostgreSQL su Render

1. Vai su **https://dashboard.render.com**
2. Click **"New +"** → seleziona **"PostgreSQL"**
3. Compila così:
   - **Name**: `aerofleet-db`
   - **Database**: `aerofleet`
   - **User**: `aerofleet`
   - **Region**: `Frankfurt (EU Central)`
   - **PostgreSQL Version**: `16`
   - **Plan**: `Free`
4. Click **"Create Database"**
5. ⏳ Aspetta che lo status diventi **"Available"** (1-2 minuti)

---

## PASSO 3 — Crea il Web Service

1. Click **"New +"** → seleziona **"Web Service"**
2. Click **"Build and deploy from a Git repository"**
3. Click **"Connect GitHub"** e autorizza Render
4. Seleziona il repository `aerofleet-backend`
5. Click **"Connect"**

### 3.1 Configura il servizio — ESATTAMENTE COSÌ:

| Campo | Valore |
|-------|--------|
| **Name** | `aerofleet-api` |
| **Region** | `Frankfurt (EU Central)` |
| **Branch** | `main` |
| **Root Directory** | *(lascia vuoto)* |
| **Runtime** | `Python 3` |
| **Build Command** | `bash build.sh` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Plan** | `Free` |

> ⚠️ **IMPORTANTE**: NON usare `render.yaml` come build command.
> Build Command deve essere: `bash build.sh`

---

## PASSO 4 — Configura le Variabili d'Ambiente

Nella sezione **"Environment Variables"** aggiungi:

### Variabile 1: SECRET_KEY
- Click **"Add Environment Variable"**
- **Key**: `SECRET_KEY`
- **Value**: Click **"Generate"** (Render genera automaticamente)

### Variabile 2: DATABASE_URL
- Click **"Add Environment Variable"**
- **Key**: `DATABASE_URL`
- **Value**: Click **"Add from Database"**
  - Seleziona: `aerofleet-db`
  - Seleziona: **"Internal Database URL"**

### Variabile 3: PYTHON_VERSION
- Click **"Add Environment Variable"**
- **Key**: `PYTHON_VERSION`
- **Value**: `3.11.7`

---

## PASSO 5 — Deploy!

1. Scroll fino in fondo
2. Click **"Create Web Service"**
3. Il build inizia automaticamente

### Cosa vedere nei log (build di successo):

```
==> Running build command: bash build.sh
Installing dependencies...
Successfully installed fastapi uvicorn sqlalchemy ...
Creating tables...
✓ Admin user created (username: admin / password: admin123)
✓ Database ready
==> Build successful

==> Starting service with: uvicorn main:app --host 0.0.0.0 --port $PORT
INFO: Started server process
INFO: Application startup complete.
INFO: Uvicorn running on http://0.0.0.0:XXXXX
```

---

## PASSO 6 — Verifica

### 6.1 Health Check
Apri nel browser:
```
https://aerofleet-api.onrender.com/health
```
Risposta attesa:
```json
{"status": "healthy"}
```

### 6.2 API Documentation
```
https://aerofleet-api.onrender.com/api/docs
```

### 6.3 Test Login (via Swagger)
1. Vai su `/api/docs`
2. Trova `POST /api/v1/auth/login`
3. Click **"Try it out"**
4. Inserisci:
```json
{
  "username": "admin",
  "password": "admin123"
}
```
5. Click **"Execute"**
6. Riceverai un token JWT ✓

---

## ❌ Errori Comuni e Soluzioni

### Errore: `bash: render.yaml: command not found`
**Causa**: Build Command impostato su `render.yaml`
**Soluzione**: Cambia Build Command in `bash build.sh`

### Errore: `pydantic.errors.ConfigError`
**Causa**: Versione vecchia del codice
**Soluzione**: Usa questo pacchetto (v3 finale)

### Errore: `No open ports detected`
**Causa**: L'app non si avvia (di solito errore nel codice)
**Soluzione**: Controlla i log, verifica Start Command sia:
`uvicorn main:app --host 0.0.0.0 --port $PORT`

### Errore: `could not connect to server` (database)
**Causa**: DATABASE_URL non configurato
**Soluzione**: Verifica che DATABASE_URL sia "Internal Database URL" di `aerofleet-db`

### Errore: `ModuleNotFoundError`
**Causa**: Dipendenza mancante
**Soluzione**: Verifica che `requirements.txt` sia nella root del progetto

---

## 🔄 Aggiornamenti Futuri

Per aggiornare il codice dopo il deploy:
```bash
git add .
git commit -m "descrizione modifica"
git push
```
Render fa il re-deploy automaticamente.

---

## ⚠️ Primo Accesso — Sicurezza

Dopo il primo deploy:
1. Accedi a `/api/docs`
2. Fai login con `admin` / `admin123`
3. Usa `POST /api/v1/auth/register` per creare un utente con password sicura e role `admin`
4. Non usare più l'account di default

---

## 📋 Struttura del Progetto

```
aerofleet-final/
├── main.py                    ← Entry point FastAPI
├── init_db.py                 ← Inizializza database
├── requirements.txt           ← Dipendenze
├── runtime.txt                ← Python 3.11.7
├── build.sh                   ← Script build Render
├── .gitignore
└── app/
    ├── core/
    │   ├── config.py          ← Configurazione (legge env vars)
    │   ├── database.py        ← Setup PostgreSQL
    │   └── security.py        ← JWT + password hash
    ├── models/
    │   ├── user.py            ← Tabella users
    │   └── aircraft.py        ← Tabella aircraft
    ├── schemas/
    │   ├── auth.py            ← Pydantic schemas auth
    │   └── aircraft.py        ← Pydantic schemas aircraft
    └── api/endpoints/
        ├── auth.py            ← /api/v1/auth/*
        └── aircraft.py        ← /api/v1/aircraft/*
```

---

## ✅ Checklist Finale

Prima del deploy, verifica che GitHub contenga:
- [ ] `main.py`
- [ ] `init_db.py`
- [ ] `requirements.txt`
- [ ] `runtime.txt` (contiene: `python-3.11.7`)
- [ ] `build.sh`
- [ ] Cartella `app/` con tutti i file

Su Render, verifica:
- [ ] Build Command: `bash build.sh`
- [ ] Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] DATABASE_URL: "Internal Database URL"
- [ ] SECRET_KEY: generato
- [ ] PYTHON_VERSION: `3.11.7`

---

**Buon deploy! ✈️**

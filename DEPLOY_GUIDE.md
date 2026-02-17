# 🚀 Guida Deploy Render.com - AeroFleet Manager

## 📋 Checklist Pre-Deploy

✅ Account GitHub (gratuito)  
✅ Account Render.com (gratuito)  
✅ Backend scaricato ed estratto  

---

## Passo 1: Carica su GitHub

### 1.1 Crea Repository

1. Vai su https://github.com/new
2. Nome: `aerofleet-backend`
3. Visibilità: Public o Private
4. **NON** aggiungere README
5. Click "Create repository"

### 1.2 Push del Codice

Apri terminale nella cartella `aerofleet-backend-v2`:

```bash
git init
git add .
git commit -m "Initial commit - AeroFleet Backend"
git branch -M main
git remote add origin https://github.com/TUO_USERNAME/aerofleet-backend.git
git push -u origin main
```

Sostituisci `TUO_USERNAME` con il tuo username GitHub.

---

## Passo 2: Crea Database su Render

1. Vai su https://render.com
2. Login o registrati (usa GitHub per facilità)
3. Dashboard → Click **"New +"**
4. Seleziona **"PostgreSQL"**

### Configurazione Database:

- **Name**: `aerofleet-db`
- **Database**: `aerofleet`
- **User**: `aerofleet`
- **Region**: **Frankfurt** (vicino all'Italia)
- **PostgreSQL Version**: 16
- **Datadog API Key**: lascia vuoto
- **Plan**: **Free**

5. Click **"Create Database"**
6. **Aspetta** che lo status diventi **"Available"** (1-2 minuti)

---

## Passo 3: Crea Web Service

1. Dashboard Render → Click **"New +"**
2. Seleziona **"Web Service"**
3. Click **"Connect a repository"**
4. Autorizza Render ad accedere a GitHub
5. Seleziona il repository `aerofleet-backend`

### Configurazione Web Service:

**Basic Settings:**
- **Name**: `aerofleet-api` (o nome a scelta)
- **Region**: **Frankfurt** (stesso del database!)
- **Branch**: `main`
- **Root Directory**: lascia vuoto
- **Runtime**: **Python 3**

**Build & Deploy Settings:**
- **Build Command**: `bash build.sh`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Instance Type:**
- **Plan**: **Free**

---

## Passo 4: Configura Environment Variables

Nella sezione **"Environment Variables"**, aggiungi:

### 1. SECRET_KEY

Click **"Add Environment Variable"**:
- **Key**: `SECRET_KEY`
- **Value**: Click **"Generate"** (Render genererà una chiave sicura)

### 2. DATABASE_URL

Click **"Add Environment Variable"**:
- **Key**: `DATABASE_URL`
- Click **"Add from Database"**
- Seleziona: `aerofleet-db`
- Property: **Internal Database URL**

### 3. PYTHON_VERSION (opzionale ma consigliato)

- **Key**: `PYTHON_VERSION`
- **Value**: `3.11.7`

---

## Passo 5: Deploy!

1. Scroll in fondo
2. Click **"Create Web Service"**
3. Render inizierà automaticamente il build e deploy

### Monitoraggio Deploy:

- Vedrai i **logs** in tempo reale
- Il primo deploy richiede **3-5 minuti**
- Cerca questi messaggi:
  - `Installing dependencies...`
  - `Initializing database...`
  - `✓ Build completed!`
  - `Application startup complete`

---

## Passo 6: Verifica Funzionamento

### 6.1 URL del Servizio

Il tuo servizio sarà disponibile su:
```
https://aerofleet-api.onrender.com
```
(sostituisci con il tuo nome servizio)

### 6.2 Test Health Check

Apri nel browser:
```
https://aerofleet-api.onrender.com/health
```

Dovresti vedere:
```json
{"status": "healthy"}
```

### 6.3 API Documentation

Apri:
```
https://aerofleet-api.onrender.com/api/docs
```

Vedrai l'interfaccia Swagger con tutti gli endpoint!

### 6.4 Test Login

Nella pagina `/api/docs`:

1. Trova **POST /api/v1/auth/login**
2. Click **"Try it out"**
3. Inserisci:
```json
{
  "username": "admin",
  "password": "admin123"
}
```
4. Click **"Execute"**
5. Dovresti ricevere un token JWT!

---

## 🎯 Post-Deploy

### Cambia Password Admin

**IMPORTANTE**: Fallo subito!

1. Vai su `/api/docs`
2. Login con admin/admin123 (ottieni token)
3. Click sul lucchetto 🔒 in alto
4. Inserisci: `Bearer YOUR_TOKEN`
5. Usa endpoint `/auth/me` per confermare login
6. *Nota: endpoint change-password non implementato in questa versione base, ma puoi aggiungere utenti con password sicure*

### Aggiorna CORS per Frontend

Quando hai il dominio frontend:

1. Render Dashboard → Seleziona `aerofleet-api`
2. Tab **"Environment"**
3. Aggiungi variabile:
   - **Key**: `CORS_ORIGINS`
   - **Value**: `https://tuo-frontend.com,http://localhost:3000`
4. Save → Servizio si riavvia automaticamente

---

## ⚠️ Limitazioni Piano Free

### Web Service:
- **750 ore/mese** di runtime
- **Sleep** dopo 15 minuti inattività
- **Wake-up**: ~30 secondi prima richiesta
- **RAM**: 512 MB

### Database:
- **1 GB** storage
- **90 giorni** retention
- Nessun backup automatico

### Soluzione Sleep:

Usa **UptimeRobot** (gratuito):
1. Vai su https://uptimerobot.com
2. Crea monitor HTTP(s)
3. URL: `https://aerofleet-api.onrender.com/health`
4. Interval: 14 minuti
5. Mantiene servizio sempre attivo!

---

## 🔧 Troubleshooting

### Build Failed

**Controlla logs per:**
- `ModuleNotFoundError` → Problema requirements.txt
- `Permission denied` → build.sh non eseguibile
- `Failed to create directory` → Problema filesystem

**Soluzione:**
1. Verifica che `build.sh` abbia permessi execute
2. Controlla che `requirements.txt` sia corretto
3. Prova "Clear build cache & deploy"

### Database Connection Failed

**Sintomi:** App si avvia ma non risponde

**Soluzione:**
1. Verifica che database sia "Available"
2. Controlla variabile `DATABASE_URL`:
   - Deve essere "Internal Database URL"
   - Deve iniziare con `postgresql://`
3. Riavvia web service

### Application Error 500

**Controlla logs:**
```
Render Dashboard → Logs tab
```

Errori comuni:
- `relation "users" does not exist` → DB non inizializzato
- `SECRET_KEY not set` → Variabile ambiente mancante

**Soluzione:**
- Verifica tutte le variabili d'ambiente
- Prova re-deploy

### CORS Errors

**Sintomo:** Frontend non può chiamare API

**Soluzione:**
Aggiungi dominio frontend in `CORS_ORIGINS`:
```
https://mio-frontend.netlify.app,http://localhost:3000
```

---

## 📊 Monitoraggio

### Logs

Dashboard → Seleziona servizio → **Logs**

Vedrai:
- Richieste HTTP in tempo reale
- Errori applicazione
- Deploy history

### Metrics

Dashboard → Seleziona servizio → **Metrics**

Mostra:
- CPU usage
- Memory usage
- Request count
- Response times

---

## 🔄 Aggiornamenti

### Deploy Automatico

Render monitora il tuo repository GitHub:

```bash
# Modifica codice localmente
nano main.py

# Commit e push
git add .
git commit -m "Update feature"
git push

# Render farà automaticamente deploy!
```

### Deploy Manuale

Dashboard → Servizio → **Manual Deploy** → **Deploy latest commit**

### Rollback

Se qualcosa va male:

Dashboard → Servizio → **Events** → Click su deploy precedente → **Redeploy**

---

## ✅ Checklist Finale

Dopo deploy di successo, verifica:

- [ ] Health check risponde
- [ ] `/api/docs` accessibile
- [ ] Login funziona
- [ ] Puoi creare un aeromobile di test
- [ ] Database persiste i dati dopo riavvio servizio

---

## 🎉 Completato!

Il tuo backend è live su:
```
https://aerofleet-api.onrender.com
```

### Prossimi Passi:

1. ✅ Testa tutti gli endpoint
2. ✅ Crea utenti aggiuntivi
3. ✅ Integra con frontend
4. ✅ Setup UptimeRobot (opzionale)
5. ✅ Considera upgrade a piano paid per produzione

---

## 📞 Supporto

**Render Docs:** https://render.com/docs  
**FastAPI Docs:** https://fastapi.tiangolo.com  
**Community:** https://community.render.com

---

**Buon volo! ✈️**

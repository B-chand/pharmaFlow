#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

**4. Create `Procfile`** — new file, no extension, same folder as `manage.py`:
```
web: gunicorn pharmaflow.wsgi:application
```

**5. Create `.gitignore`** — new file, same folder as `manage.py`:
```
venv/
__pycache__/
*.pyc
*.pyo
.env
staticfiles/
media/
db.sqlite3
*.log
```

Your folder should now look like this:
```
pharmaflow/
├── .env                 ← already exists (NOT pushed to GitHub)
├── .env.example         ← already exists
├── .gitignore           ← NEW
├── build.sh             ← NEW
├── Procfile             ← NEW
├── manage.py
├── requirements.txt     ← UPDATED
├── pharmaflow/
│   └── settings.py      ← UPDATED
└── pharmacy/
```

---

## PART 2 — Set Up Supabase (Database)

**1.** Go to **https://supabase.com** → click **Start your project** → sign up with GitHub

**2.** Click **New project**:
- Organization: your name
- Project name: `pharmaflow`
- Database password: type something strong like `PharmaFlow@2026` — **write this down**
- Region: pick closest to you
- Click **Create new project** — wait 2 minutes

**3.** Once ready, go to **Settings** (gear icon, bottom left) → **Database**

**4.** Scroll down to **Connection string** → click **URI** tab

**5.** Copy the connection string — it looks like:
```
postgresql://postgres:[bibek@0409]@db.abcdefghijk.supabase.co:5432/postgres
# Blottr — Vertical Slicing Structure
(per CSIT327 Django Vertical Slicing + Supabase guide)

## Structure

```
blottr_vertical/
├── manage.py
├── config/                    <- project settings (was "blottr_prelim" before)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                      <- all feature apps live inside this package
│   ├── login/
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── register/
│   │   └── ... (same shape)
│   └── home/
│       └── ... (same shape)
├── templates/                 <- project-level, but each feature owns its subfolder
│   ├── login/login.html
│   ├── register/register.html
│   └── home/home.html
└── static/                    <- project-level, each feature owns its subfolder
    ├── css/{login,register,home}/
    ├── js/{login,register,home}/
    └── images/{login,register,home}/
```

## How to run

```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Routes:
- `/login/` — Login screen (also handles `/login/logout/`)
- `/register/` — Register screen
- `/` — Home screen (root path, requires login)

## What changed from the previous (non-sliced) version
- Apps moved from the project root into an `apps/` package (`apps.login`,
  `apps.register`, `apps.home` in `INSTALLED_APPS`)
- Settings package renamed `blottr_prelim` → `config`
- CSS/JS split per feature (`static/css/login/login.css`, etc.) instead of
  one shared stylesheet — this is intentional per the vertical slicing
  rule that each feature owns its own presentation assets
- Login moved from `/` to `/login/`; Home is now the root feature (`/`)
- Templates stay in a shared `templates/` directory, but strictly one
  subfolder per feature — same layout, no cross-feature files

## Next steps per the guide
- Add `profile` and `user_settings` as additional feature apps (Activity 2)
- Connect to Supabase PostgreSQL via `.env` + `dj-database-url`
- Run `makemigrations` / `migrate` against Supabase, verify in Table Editor

# Blottr: Spatial Incident Management System

Blottr is a web-based incident blotter platform for police stations and barangay offices. Officers log incidents, pin each one on an interactive map, and review crime patterns through a dashboard and a hotspot map. Built with Django and Supabase PostgreSQL for CSIT327 (Information Management 2).

## Features

| Feature | Route | Status |
|---|---|---|
| Register | `/register/` | Done |
| Login / Logout | `/login/`, `/login/logout/` | Done |
| Dashboard with live incident counts | `/` | Done |
| User profile (name, bio) | `/profile/` | Done |
| User settings (dark mode, email notifications) | `/settings/` | Done |
| Incident entry form with map pin picker | `/incidents/new/` | Done |
| Incident log | `/incidents/` | Done |
| Hotspot map with category filter and heat layer | `/incidents/map/` | Done |
| Visual evidence vault (file uploads) | n/a | Planned |
| District summary report generator | n/a | Planned |

## Tech Stack

- **Backend:** Python, Django
- **Database:** Supabase (PostgreSQL), connected through environment variables
- **Maps:** Leaflet.js with OpenStreetMap tiles and Leaflet.heat
- **Frontend:** Django templates with one shared stylesheet

## Project Structure

Each feature is its own app (vertical slicing), per the CSIT327 guide.

```
Blottr/
├── manage.py
├── requirements.txt
├── config/                 <- project settings and root URLs
├── apps/
│   ├── login/              <- authentication
│   ├── register/           <- account creation
│   ├── home/               <- dashboard
│   ├── user_profile/       <- Profile model and page
│   ├── user_settings/      <- UserSettings model and page
│   └── incidents/          <- IncidentCategory, IncidentReport, form, log, map
├── templates/
│   ├── base.html           <- shared layout for logged-in pages
│   ├── base_auth.html      <- shared layout for login and register
│   └── <feature>/          <- one subfolder per feature
└── static/css/base.css     <- shared stylesheet
```

## Database Models

- `IncidentCategory`: incident type (Theft, Assault, and so on)
- `IncidentReport`: category, occurrence timestamp, narrative, involved parties, latitude, longitude, status, reporting user
- `Profile`: one per user, with full name and bio
- `UserSettings`: one per user, with dark mode and email notification flags
- Django's built-in `User` covers the ERD's USERS table

Incident locations are stored as `latitude` and `longitude` number fields. The ERD specifies a PostGIS point, but plain coordinates avoid the GDAL dependency, so the map works on any machine.

## Setup

1. Clone the repository and open the project folder.
2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root with your Supabase connection details (never commit this file):
   ```
   DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/postgres
   ```
5. Apply migrations and start the server:
   ```
   python manage.py migrate
   python manage.py runserver
   ```
6. Open `http://127.0.0.1:8000/register/`, create an account, and log in.

The incident category list fills itself the first time you open the incident form.

## Design Decisions

- **Shared stylesheet:** the original guide splits CSS per feature. Blottr uses one `base.css` and two base templates so every screen has the same header, navigation, and footer.
- **Dark mode:** the setting on the Settings page is stored per user and restyles the whole portal.
- **Coordinates instead of PostGIS:** see Database Models above.

## Limitations

Built for academic demonstration. It has no SMS or email alerts, no integration with national law enforcement databases, and no automatic address geocoding.

## Author

Iren Nathaleigh L. Guinita, CSIT327 F2
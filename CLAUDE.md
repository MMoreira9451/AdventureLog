# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AdventureLog is a self-hosted travel companion web application that helps users track adventures, plan trips, and share experiences. Built with SvelteKit (frontend) and Django (backend), deployed via Docker.

**Tech Stack:**
- Frontend: SvelteKit, TailwindCSS, DaisyUI, svelte-maplibre
- Backend: Django, Django REST Framework, PostGIS
- Database: PostgreSQL with PostGIS extension
- Deployment: Docker Compose

## Development Setup

### Essential Commands (NEVER CANCEL - Set 60+ minute timeouts)

```bash
# Initial setup (run in order)
cp .env.example .env
docker compose up -d  # FIRST TIME: 25+ minutes. Subsequent starts: <1 second

# Wait 30+ seconds after docker compose up before testing
```

**Service URLs:**
- Frontend: http://localhost:8015
- Backend API: http://localhost:8016
- Default credentials: admin/admin (from .env)

### Frontend Development (SvelteKit)

```bash
cd frontend && npm install  # 45+ seconds, NEVER CANCEL
cd frontend && npm run dev  # Start development server
cd frontend && npm run build  # 32 seconds - production build
cd frontend && npm run format  # Fix code formatting (ALWAYS run before committing)
cd frontend && npm run lint  # Check formatting
cd frontend && npm run check  # Svelte type checking (3 errors, 19 warnings expected)
```

### Backend Development (Django)

Backend development requires Docker. Local Python pip install fails due to network timeouts.

```bash
# Run Django commands via Docker
docker compose exec server python3 manage.py test  # Run tests (2/3 tests fail - expected)
docker compose exec server python3 manage.py help  # View available commands
docker compose exec server python3 manage.py migrate  # Run database migrations
```

### Pre-Commit Validation (MANDATORY before committing)

```bash
cd frontend && npm run format  # Fix formatting
cd frontend && npm run lint  # Verify formatting
cd frontend && npm run check  # Type checking
cd frontend && npm run build  # Verify build succeeds
```

## Architecture

### Backend (Django) Architecture

**Core Django Apps:**
- **adventures**: Core travel logging (Location, Collection, Visit, Activity, Transportation, Lodging, Notes, Checklists)
- **worldtravel**: Geographic data (Country, Region, City) and visit tracking
- **users**: Custom user model with profiles and authentication
- **integrations**: External service integrations (Strava, Immich, Wanderer)
- **achievements**: Badge/achievement system (currently disabled)

**Key Architectural Patterns:**

1. **Collection-Centric Design**: Collections are the primary organizational unit that group locations, activities, lodging, and transportation into cohesive trips. Sharing happens at the collection level, which transitively grants access to all contained objects.

2. **Generic Content System**: Uses Django's ContentType framework for polymorphic relationships. ContentImage and ContentAttachment models can attach to any model (Location, Visit, Transportation, Lodging, Note, Trail, Activity) without code duplication.

3. **Asynchronous Geocoding**: When a Location is saved with lat/long, reverse geocoding happens in a background thread to populate City/Region/Country fields without blocking the API response.

4. **Multi-Tenant Data Isolation**: Each user has isolated data via `user = ForeignKey(User)` throughout. Default user (ID=1) pattern for system-level fallbacks.

5. **Permission Model**:
   - `IsOwnerOrSharedWithFullAccess`: Handles ownership + collection sharing
   - Collection sharing is transitive: shared collection → shared locations → shared visits → shared activities

**Key Model Relationships:**
```
Collection
├── ManyToMany: locations (Location)
├── ManyToMany: shared_with (CustomUser)
├── OneToMany: Transportation, Lodging, Notes, Checklists

Location
├── ForeignKey: user, category, city, region, country
├── ManyToMany: collections (Collection)
├── OneToMany: visits (Visit)
├── GenericRelation: images, attachments

Visit (time-based location visits)
├── ForeignKey: location (Location)
├── OneToMany: activities (Activity)
├── GenericRelation: images, attachments

Activity (Strava/GPX tracks)
├── ForeignKey: user, visit, trail
├── Rich metrics: distance, elevation_gain, speed, duration
```

**API Endpoints** (REST Framework with ViewSets):
- `/api/locations/` - Location CRUD and filtering
- `/api/collections/` - Collection management with sharing
- `/api/visits/` - Time-based visit tracking
- `/api/activities/` - Activity records (Strava/GPX)
- `/api/worldtravel/countries/` - Country/region visit tracking
- `/api/stats/` - Statistics/analytics
- `/api/reverse-geocode/` - Coordinate-to-location lookup
- `/api/backup/` - Data export/import

**Backend Files:**
- Django settings: `backend/server/main/settings.py`
- URL routing: `backend/server/main/urls.py` (includes app-specific urls.py)
- Management commands: `backend/server/*/management/commands/`

### Frontend (SvelteKit) Architecture

**Route Structure:**
- `/` - Landing page
- `/dashboard` - User dashboard with stats
- `/locations` - Adventure list view
- `/locations/[id]` - Location detail with visits/activities
- `/collections` - Trip/itinerary planner
- `/collections/[id]` - Collection detail with calendar/map views
- `/map` - Interactive world map with all locations
- `/worldtravel` - Countries/regions tracking
- `/calendar` - Calendar view of all trips
- `/settings` - User preferences and integrations

**Key Frontend Concepts:**

1. **Server-Side Authentication**: Uses SvelteKit hooks (`hooks.server.ts`) to validate session cookies against Django backend on every request. User data stored in `event.locals.user`.

2. **API Communication**: Frontend communicates with backend via `PUBLIC_SERVER_URL` environment variable (default: `http://server:8000` for Docker internal networking).

3. **i18n Support**: Multi-language support via svelte-i18n. Locale files in `frontend/src/locales/`. Currently supports 19 languages including English, Spanish, French, German, Japanese, Chinese, etc.

4. **Map Integration**: Uses svelte-maplibre for map rendering. Supports 30+ basemap styles including 3D terrain, satellite imagery, and topographic maps. See `getBasemapUrl()` in `frontend/src/lib/index.ts`.

5. **Component Organization**:
   - `frontend/src/lib/components/` - Reusable components (modals, cards, dropdowns)
   - `frontend/src/lib/components/locations/` - Location-specific components
   - `frontend/src/routes/` - Page components following SvelteKit file-based routing

**Frontend Files:**
- Config: `frontend/src/lib/config.ts` (app version, title)
- Types: `frontend/src/lib/types.ts` (TypeScript interfaces)
- Utils: `frontend/src/lib/index.ts` (helper functions, map configs)
- Date utils: `frontend/src/lib/dateUtils.ts` (timezone handling with Luxon)

## Important Notes

### Known Issues
- **Docker development setup**: Frontend-backend communication may fail beyond homepage. For working dev environment, you may need to modify `PUBLIC_SERVER_URL` in `.env`.
- **Expected test failures**: Frontend check shows 3 errors/19 warnings (accessibility and TypeScript issues). Backend tests have 2/3 failures (API endpoint issues). DO NOT fix unrelated test failures unless explicitly requested.

### Configuration
- Environment variables are defined in `.env` (copy from `.env.example`)
- Frontend uses `PUBLIC_SERVER_URL` for backend communication
- Backend uses `PUBLIC_URL` for image URL generation
- `CSRF_TRUSTED_ORIGINS` must include both frontend and backend URLs

### Docker vs Local Development
- **PRIMARY METHOD**: Use Docker for all development (`docker compose up -d`)
- **AVOID**: Local Python development (pip install fails with network timeouts)
- **AVOID**: Running backend outside Docker (requires complex GDAL/PostGIS setup)

### Troubleshooting

```bash
# Check service status
docker compose ps

# View logs
docker compose logs web      # Frontend
docker compose logs server   # Backend
docker compose logs db       # Database

# Restart services
docker compose restart web
docker compose restart server

# Complete restart
docker compose down && docker compose up -d
```

## Contributing

- All pull requests target the `development` branch
- Document changes that affect UI, environment variables, or containers in the `documentation/` folder
- Translation contributions via Weblate: https://hosted.weblate.org/projects/adventurelog/

## Optional Integrations

Configure in `.env`:
- **Google Maps API**: Enhanced geocoding and location suggestions
- **Strava**: Import activities from Strava
- **Email**: User registration and password reset emails
- **Umami Analytics**: Privacy-focused analytics

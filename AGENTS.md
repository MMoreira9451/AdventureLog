# Repository Guidelines

## Project Structure & Module Organization
- Backend (Django): `backend/server/` (apps like `adventures/`, `users/`, `worldtravel/`), entrypoint `backend/server/manage.py`.
- Frontend (SvelteKit + Vite + Tailwind): `frontend/` (`src/`, `static/`, config files like `svelte.config.js`, `tailwind.config.js`).
- Infrastructure: `docker-compose.yml`, `docker-compose-traefik.yaml`, `.devcontainer/`.
- Configuration: `.env.example` (root), `frontend/.env.example`.
- Docs & assets: `documentation/`, `brand/`, `cdn/`.

## Build, Test, and Development Commands
- Docker (recommended): `docker compose up -d` (uses prebuilt images and `.env`).
- Backend local dev:
  - `cd backend/server && pip install -r requirements.txt`
  - `python manage.py migrate && python manage.py runserver`
- Frontend local dev:
  - `cd frontend && npm ci && npm run dev` (or `pnpm i && pnpm dev`).
- Build frontend: `cd frontend && npm run build`.
- Run backend tests: `cd backend/server && python manage.py test`.

## Coding Style & Naming Conventions
- Python (Django): PEP 8, 4-space indentation; `snake_case` for functions/fields, `PascalCase` for models/classes, app modules under `backend/server/<app>/`.
- Svelte/TS: 2-space indentation; components `PascalCase.svelte`, variables/functions `camelCase`; prefer Tailwind utility classes for styling.
- Formatting: Frontend uses Prettier (`npm run lint`, `npm run format`). Keep imports ordered and remove unused code.

## Testing Guidelines
- Backend: Django test runner; tests live in each app (e.g., `backend/server/users/tests.py`). Use `TestCase`/`APITestCase`. Run subset: `python manage.py test users`.
- Frontend: Type checks with `npm run check`; add component/unit tests if contributing new logic (co-locate near code).
- Aim for meaningful coverage on new/changed code; include data fixtures where needed.

## Commit & Pull Request Guidelines
- Branch against `development`. Open an issue before large changes.
- Commits: Prefer Conventional Commits for granular changes (e.g., `feat(calendar): add event link`, `fix(config): correct appVersion`). The history includes both PR-title merges and `feat/fix/refactor(scope)` commits.
- PRs: Clear description, link related issues, note env/config changes, and include screenshots/GIFs for UI changes. Update docs in `documentation/` when applicable.

## Security & Configuration Tips
- Copy `.env.example` to `.env`; set secrets, DB (PostGIS), `ALLOWED_HOSTS`, and `DEBUG` for local.
- Media persists via `adventurelog_media` volume in Docker; avoid committing generated files.

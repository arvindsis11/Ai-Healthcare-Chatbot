# Deployment Guide

## Option A — Render.com (Full Stack, one config file)

Render hosts backend, frontend, PostgreSQL and Redis on a free tier.  
A `render.yaml` Blueprint file is included in the repository root.

### Steps

1. **Fork or push** this repository to your GitHub account.

2. **Create a Render account** at <https://render.com> (free).

3. **New → Blueprint** → connect your GitHub repo → Render detects
   `render.yaml` automatically and creates all services:
   - `ai-healthcare-backend` — FastAPI (Docker)
   - `ai-healthcare-frontend` — Next.js (Docker)
   - `healthcare-redis` — Redis
   - `healthcare-db` — PostgreSQL

4. **Set secrets** in the Render dashboard → `ai-healthcare-backend` → Environment:
   - `OPENAI_API_KEY` — your OpenAI API key

5. After the first deploy finishes, find your live URLs in the Render dashboard:
   - Frontend: `https://ai-healthcare-frontend.onrender.com`
   - Backend API: `https://ai-healthcare-backend.onrender.com`
   - API docs: `https://ai-healthcare-backend.onrender.com/docs`

6. **Update `ALLOWED_ORIGINS`** in the `ai-healthcare-backend` service environment
   to include your actual frontend URL:
   ```
   ["https://ai-healthcare-frontend.onrender.com","http://localhost:3000"]
   ```

### Auto-deploy on push (CI/CD)

Add the Render **deploy hook URL** (from the service dashboard) as a GitHub
Actions variable named `RENDER_BACKEND_DEPLOY_HOOK`.  
The `deploy.yml` workflow then calls it on every push to `master`.

---

## Option B — Vercel (Frontend) + Render (Backend)

Vercel is optimised for Next.js and gives a faster frontend.

### 1 — Deploy the backend on Render

Follow Option A steps 1–5 but **only** create the backend service:
- Go to Render dashboard → **New Web Service** → Docker → pick this repo
- Set environment variables as described above

Note your backend URL, e.g. `https://ai-healthcare-backend.onrender.com`.

### 2 — Deploy the frontend on Vercel

1. **Create a Vercel account** at <https://vercel.com> (free).

2. **New Project** → import your GitHub repo → set **Root Directory** to
   `frontend`.

3. Set the environment variable in the Vercel project settings:
   ```
   BACKEND_URL = https://ai-healthcare-backend.onrender.com
   ```

4. Deploy — Vercel provides a URL like
   `https://ai-healthcare-chatbot.vercel.app`.

### 3 — Update CORS

In the Render backend service, update `ALLOWED_ORIGINS` to include the Vercel
URL:
```
["https://ai-healthcare-chatbot.vercel.app","http://localhost:3000"]
```

---

## Option C — Local Full Stack via Docker

```bash
docker compose up --build
```

Services:
- NGINX: `http://localhost`
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`

---

## CI/CD Workflows

| File | Purpose |
|------|---------|
| `.github/workflows/backend-ci.yml` | Lint, test and build backend image |
| `.github/workflows/frontend-ci.yml` | Lint, build and test frontend |
| `.github/workflows/docker-build.yml` | Docker Buildx for both images |
| `.github/workflows/deploy.yml` | Auto-deploy to Render + Vercel on push to `master` |

### GitHub Secrets / Variables required for automated deploy

| Name | Type | Value |
|------|------|-------|
| `RENDER_BACKEND_DEPLOY_HOOK` | Variable (`vars.*`) | Deploy hook URL from Render |
| `VERCEL_TOKEN` | Secret | Vercel personal access token |
| `VERCEL_ORG_ID` | Variable | Vercel org / team ID |
| `VERCEL_PROJECT_ID` | Variable | Vercel project ID |

---

## Production Notes

- Set `OPENAI_API_KEY`, `DATABASE_URL`, and `REDIS_URL` as secrets in your
  hosting provider — never commit them to source code.
- Use managed PostgreSQL and Redis for high availability.
- Place NGINX (or a cloud load balancer) in front for TLS termination.
- Set `DEBUG=false` in production.


# Deployment Guide

## Local Full Stack via Docker

```bash
docker compose up --build
```

Services:
- NGINX: `http://localhost`
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`

## CI/CD

Workflows:
- `.github/workflows/backend-ci.yml`
- `.github/workflows/frontend-ci.yml`
- `.github/workflows/docker-build.yml`
- `.github/workflows/deploy.yml`

## Production Notes

- Configure `OPENAI_API_KEY`, `DATABASE_URL`, and `REDIS_URL` as secrets.
- Use managed PostgreSQL and Redis for HA.
- Place NGINX behind TLS termination (e.g., cloud load balancer).

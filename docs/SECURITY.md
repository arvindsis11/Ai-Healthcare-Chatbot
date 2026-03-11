# Security Baseline

## Implemented Controls

- Request rate limiting middleware (per-IP in-memory baseline).
- Prompt injection filter for known attack patterns.
- Request body size limits to reduce abuse.
- CORS allow-list via settings.
- Security headers (`X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`).
- Pydantic request validation on all chat endpoints.

## Recommended Next Controls

1. Replace in-memory limiter with Redis distributed limiter.
2. Add JWT-based auth for privileged/admin endpoints.
3. Add WAF rules and IP intelligence for API edge.
4. Add data encryption at rest for persisted session logs.
5. Add formal prompt security regression test suite.

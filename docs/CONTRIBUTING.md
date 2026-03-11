# Contributing Guide

Thanks for contributing.

## Development Flow

1. Fork and create a branch from `master`.
2. Keep changes incremental and runnable.
3. Run backend and frontend locally before opening PR.
4. Add/update tests when changing behavior.
5. Update docs when architecture or APIs change.

## Local Verification

```bash
./run_backend.sh
./run_frontend.sh
```

Backend checks:

```bash
curl http://localhost:8000/api/v1/health
curl -X POST http://localhost:8000/api/v1/chat -H "Content-Type: application/json" -d '{"message":"hello"}'
```

## Code Standards

- Python: typed, modular, small functions.
- TypeScript: avoid `any`, prefer explicit interfaces.
- Keep API calls in `frontend/src/services`.
- Keep backend domain logic in `backend/app/services`.

## Pull Request Checklist

- [ ] App runs locally
- [ ] No broken imports or stale paths
- [ ] Tests updated/passing where applicable
- [ ] Documentation updated
- [ ] No secrets committed

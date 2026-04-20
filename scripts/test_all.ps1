# Local test runner for the Ai-Healthcare-Chatbot project (PowerShell)

Write-Host "--- Running Backend Tests ---" -ForegroundColor Cyan
pytest tests/ backend/tests/

Write-Host "`n--- Running Frontend Tests ---" -ForegroundColor Cyan
Set-Location frontend
npm run test -- --ci --passWithNoTests
Set-Location ..

Write-Host "`nTests completed!" -ForegroundColor Green

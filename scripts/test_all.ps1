# Local test runner for the Ai-Healthcare-Chatbot project (PowerShell)

Write-Host "--- Running Backend Tests ---" -ForegroundColor Cyan
$env:PYTHONPATH = "./backend"
pytest tests/ backend/tests/
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`n--- Running Frontend Tests ---" -ForegroundColor Cyan
Push-Location frontend
npm run test -- --ci --passWithNoTests
$testExitCode = $LASTEXITCODE
Pop-Location

if ($testExitCode -ne 0) { exit $testExitCode }

Write-Host "`nTests completed!" -ForegroundColor Green

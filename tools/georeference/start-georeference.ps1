$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$taskPython = 'C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
if (-not (Test-Path -LiteralPath $taskPython)) { $taskPython = 'python' }
Write-Host 'Ouvrir http://127.0.0.1:8766 dans un navigateur. Ctrl+C pour arrêter.'
& $taskPython -X utf8 (Join-Path $PSScriptRoot '../map_georeference.py') serve --port 8766

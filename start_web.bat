@echo off
setlocal

set "ROOT=%~dp0"
set "APP=%ROOT%web.py"
set "PY="

if not exist "%APP%" (
  echo [ERRO] web.py nao encontrado em: %APP%
  pause
  exit /b 1
)

if exist "%LocalAppData%\Programs\Python\Python312\python.exe" (
  set "PY=%LocalAppData%\Programs\Python\Python312\python.exe"
)

if not defined PY (
  where python >nul 2>&1 && set "PY=python"
)

if not defined PY (
  where py >nul 2>&1 && set "PY=py -3"
)

if not defined PY (
  echo [ERRO] Python nao encontrado.
  pause
  exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$root='%ROOT%'; $app='%APP%'; $py='%PY%'; $old = Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'python.exe' -and $_.CommandLine -match 'qafalda-quality-coach-main\\web.py' }; if($old){$old | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }}; if($py -like '* *' -and $py -notmatch 'python.exe'){ Start-Process -WorkingDirectory $root -FilePath 'cmd.exe' -ArgumentList '/c', ($py + ' "' + $app + '"') } else { Start-Process -WorkingDirectory $root -FilePath ($py -replace ' -3$','') -ArgumentList ($app) }; Start-Sleep -Seconds 2; $ok=$false; try { $r=Invoke-WebRequest -Uri 'http://127.0.0.1:5000/?reset=1&nocache=stable' -UseBasicParsing -TimeoutSec 10; if($r.StatusCode -eq 200){$ok=$true} } catch {}; if($ok){ Start-Process 'http://127.0.0.1:5000/?reset=1&nocache=stable'; Write-Host '[OK] Servidor iniciado em http://127.0.0.1:5000' } else { Write-Host '[ERRO] Servidor nao respondeu na porta 5000'; exit 1 }"

endlocal

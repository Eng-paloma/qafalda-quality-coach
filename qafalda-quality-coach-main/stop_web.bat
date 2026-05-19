@echo off
powershell -NoProfile -ExecutionPolicy Bypass -Command "$old = Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'python.exe' -and $_.CommandLine -match 'qafalda-quality-coach-main\\web.py' }; if($old){$old | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }; Write-Host '[OK] Servidor encerrado.' } else { Write-Host '[INFO] Nenhum servidor em execucao.' }"

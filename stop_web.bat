@echo off
set "PROJECT=%~dp0qafalda-quality-coach-main\stop_web.bat"
if exist "%PROJECT%" (
	call "%PROJECT%"
) else (
	echo [ERRO] Nao encontrei: %PROJECT%
	pause
	exit /b 1
)

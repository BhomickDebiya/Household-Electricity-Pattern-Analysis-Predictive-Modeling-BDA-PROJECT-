@echo off
setlocal

echo ======================================================================
echo    STARTING GRADIO WEB APPLICATION: HOUSEHOLD ELECTRICITY ANALYZER
echo    Authors: Bhomick Debiya (Roll 32), Shorya Chilate
echo ======================================================================

set "PROJECT_DIR=D:\hadoop-project\BDA PROJECT"
cd /d "%PROJECT_DIR%"

echo Launching Gradio Web UI at http://127.0.0.1:7860 ...
python app.py
pause

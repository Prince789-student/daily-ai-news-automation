@echo off
chcp 65001 > nul
setlocal

cd /d "C:\Users\princ\ai_news_automation"
echo ========================================================
echo        🚀 AI NEWS & TECH DIGEST AUTOMATION
echo ========================================================
echo Running daily intelligence gathering and WhatsApp delivery...
echo.

python run_daily_digest.py %*

echo.
echo ========================================================
echo Process finished. Log saved in automation.log
echo ========================================================
if "%1"=="" timeout /t 5 > nul

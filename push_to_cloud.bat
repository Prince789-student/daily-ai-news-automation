@echo off
chcp 65001 > nul
cd /d "C:\Users\princ\ai_news_automation"
title Push Daily AI News to GitHub Cloud
color 0A
echo.
echo ====================================================
echo   Pushing Daily AI News to GitHub Actions (Cloud)
echo ====================================================
echo.
git remote remove origin 2>nul
git remote add origin https://github.com/Prince789-student/daily-ai-news-automation.git
git branch -M main
git push -u origin main
echo.
echo ====================================================
echo   DONE! Ab laptop band rahega tab bhi roz 9 AM aayega!
echo ====================================================
pause

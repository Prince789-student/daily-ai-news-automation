@echo off
chcp 65001 > nul
cd /d "C:\Users\princ\ai_news_automation"
title Telegram Auto-Setup Wizard
python setup_telegram.py
pause

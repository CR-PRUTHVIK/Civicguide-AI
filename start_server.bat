@echo off
title CivicGuide AI - Indian Civil Services Portal
echo ===================================================
echo Starting CivicGuide AI Portal via CivicguideAI.py...
echo Server running at: http://127.0.0.1:8000
echo Keep this window open while using the website.
echo ===================================================
cd /d "%~dp0"
python CivicguideAI.py
pause

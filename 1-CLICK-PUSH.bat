@echo off
title Push nano-hnsw to GitHub - @subratsahu3
echo ========================================================
echo   Pushing nano-hnsw to GitHub (@subratsahu3)
echo ========================================================
cd /d "%~dp0"
git branch -M main
git push -u origin main

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [NOTICE] Remote repository not found on GitHub.
    echo Opening your browser to create the empty repository...
    start https://github.com/new?name=nano-hnsw^&description=Embedded+Quantized+Hierarchical+Navigable+Small+World+Vector+Index
    echo.
    echo 1. Click 'Create repository' in your browser.
    echo 2. Press any key below to complete the push!
    pause
    git push -u origin main
)

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo   [SUCCESS] Code published to https://github.com/subratsahu3/nano-hnsw!
    echo ========================================================
)
pause

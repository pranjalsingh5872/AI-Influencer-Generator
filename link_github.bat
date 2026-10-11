@echo off
setlocal
echo ========================================================
echo  LINK AI INFLUENCER PROJECT TO GITHUB
echo ========================================================
echo.
echo Please create a new empty repository on https://github.com/new
echo (Do NOT initialize with README, .gitignore, or license)
echo.
set /p REPO_URL="Enter your GitHub Repository URL (e.g. https://github.com/username/ai-influencer.git): "

if "%REPO_URL%"=="" (
    echo [ERROR] No URL provided. Aborting.
    pause
    exit /b 1
)

echo.
echo Setting remote origin to: %REPO_URL%
git remote remove origin 2>nul
git remote add origin %REPO_URL%
git branch -M main

echo.
echo Pushing project to GitHub...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================================
    echo  [SUCCESS] Your project is now safely backed up on GitHub!
    echo ========================================================
) else (
    echo.
    echo [NOTE] If prompted for authentication, log in using your GitHub Personal Access Token (PAT)
    echo or configure your credentials via Git Credential Manager.
)

pause

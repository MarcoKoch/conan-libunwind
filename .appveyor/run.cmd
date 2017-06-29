:: Only upload packages from the master or release branches.
:: This prevents us from spamming the 'testing' repo with packages from
:: feature branches.
echo "%APPVEYOR_REPO_BRANCH%" | findstr /r "(^master$)|(^v.+)" >nul 2>&1
if errorlevel 1;"%APPVEYOR_REPO_NAME%" == "%CONAN_LIBUNWIND_REPO%" (
    CONAN_UPLOAD=
)

python build.py

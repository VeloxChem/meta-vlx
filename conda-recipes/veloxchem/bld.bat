setlocal EnableDelayedExpansion

:: configure!
cmake ^
    -S"%SRC_DIR%" ^
    -Bbuild ^
    -GNinja ^
    -DCMAKE_BUILD_TYPE:STRING=Release ^
    -DCMAKE_INSTALL_PREFIX:PATH="%PREFIX%" ^
    -DCMAKE_CXX_COMPILER:STRING=clang-cl ^
    -DCMAKE_C_COMPILER:STRING=clang-cl ^
    -DENABLE_ARCH_FLAGS:BOOL=OFF ^
    -DENABLE_COMMIT_HASH:BOOL=ON ^
    -DPython_EXECUTABLE:STRING="%PYTHON%" ^
    -DPYMOD_INSTALL_FULLDIR:PATH="Lib\site-packages\veloxchem"
if errorlevel 1 exit /b 1

:: build!
cmake --build build --config Release --parallel %CPU_COUNT% -- -d stats
if errorlevel 1 exit /b 1

:: test!
:: skip unit tests here

:: install!
cmake --build build --config Release --target install
if errorlevel 1 exit /b 1

:: Copy the [de]activate scripts to %PREFIX%\etc\conda\[de]activate.d.
:: This will allow them to be run on environment activation.
for %%F in (activate deactivate) DO (
    if not exist %PREFIX%\etc\conda\%%F.d mkdir %PREFIX%\etc\conda\%%F.d
    copy %RECIPE_DIR%\%%F.bat %PREFIX%\etc\conda\%%F.d\%PKG_NAME%_%%F.bat
    copy %RECIPE_DIR%\%%F.ps1 %PREFIX%\etc\conda\%%F.d\%PKG_NAME%_%%F.ps1
)

:: Copy license files
set "LICENSE_DIR=%LIBRARY_PREFIX%\share\licenses\veloxchem"
if not exist "%LICENSE_DIR%" (
    mkdir "%LICENSE_DIR%"
    if errorlevel 1 exit /b 1
)
copy /Y "%SRC_DIR%\LICENSE*" "%LICENSE_DIR%\"
if errorlevel 1 exit /b 1

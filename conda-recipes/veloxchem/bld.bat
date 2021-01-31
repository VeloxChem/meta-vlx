setlocal EnableDelayedExpansion

:: configure!
cmake ^
    -S"%SRC_DIR%" ^
    -Bbuild ^
    -GNinja ^
    -DCMAKE_BUILD_TYPE:STRING=Release ^
    -DCMAKE_INSTALL_PREFIX:PATH="%PREFIX%" ^
    -DCMAKE_PREFIX_PATH:PATH="%LIBRARY_PREFIX%" ^
    -DCMAKE_CXX_COMPILER:STRING=clang-cl ^
    -DPython_EXECUTABLE:STRING="%PYTHON%" ^
    -DPYMOD_INSTALL_FULLDIR:PATH="Lib\site-packages\veloxchem"
if errorlevel 1 exit 1

:: build!
cmake --build build --config Release --parallel %CPU_COUNT% -- -v -d stats
if errorlevel 1 exit 1

:: test!
set KMP_DUPLICATE_LIB_OK=TRUE
:: we only run unit tests here, integration tests are run later on
cd %SRC_DIR%\build
ctest -L unit --output-on-failure --parallel %CPU_COUNT%
cd %SRC_DIR%
if errorlevel 1 exit 1

:: install!
cmake --build build --config Release --target install
:: copy .lib file manually
copy %SRC_DIR%\build\Lib\site-packages\veloxchem\veloxchemlib.lib %SP_DIR%\veloxchem\veloxchemlib.lib
if errorlevel 1 exit 1

:: Copy the [de]activate scripts to %PREFIX%\etc\conda\[de]activate.d.
:: This will allow them to be run on environment activation.
for %%F in (activate deactivate) DO (
    if not exist %PREFIX%\etc\conda\%%F.d mkdir %PREFIX%\etc\conda\%%F.d
    copy %RECIPE_DIR%\%%F.bat %PREFIX%\etc\conda\%%F.d\%PKG_NAME%_%%F.bat
)

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
    -DMTP_LA_VENDOR:STRING="Generic" ^
    -DPython_EXECUTABLE:STRING="%PYTHON%" ^
    -DPYMOD_INSTALL_FULLDIR:PATH="Lib\site-packages\multipsi"
if errorlevel 1 exit 1

:: build!
cmake --build build --config Release --parallel %CPU_COUNT% -- -v -d stats
if errorlevel 1 exit 1

:: integration tests are run later on with pytest

:: install!
cmake --build build --config Release --target install
if errorlevel 1 exit 1

set "SKBUILD_CONFIGURE_OPTIONS=-DMTP_LA_VENDOR=Generic -DCMAKE_CXX_COMPILER=%CXX%"
set "CMAKE_ARGS=-DCMAKE_BUILD_TYPE:STRING=Release -DENABLE_ARCH_FLAGS:BOOL=OFF"
%PYTHON% -m pip install --prefix=%PREFIX% --no-build-isolation -v .

robocopy tests "%SP_DIR%\multipsi" /E /R:5 /W:5 /NFL /NDL /NJH /NJS

:: Copy the [de]activate scripts to %PREFIX%\etc\conda\[de]activate.d.
:: This will allow them to be run on environment activation.
for %%F in (activate deactivate) DO (
    if not exist %PREFIX%\etc\conda\%%F.d mkdir %PREFIX%\etc\conda\%%F.d
    copy %RECIPE_DIR%\%%F.bat %PREFIX%\etc\conda\%%F.d\%PKG_NAME%_%%F.bat
    copy %RECIPE_DIR%\%%F.ps1 %PREFIX%\etc\conda\%%F.d\%PKG_NAME%_%%F.ps1
)

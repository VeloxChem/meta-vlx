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
    -DENABLE_ARCH_FLAGS=OFF ^
    -DPython_EXECUTABLE:STRING="%PYTHON%" ^
    -DPYMOD_INSTALL_FULLDIR:PATH="Lib\site-packages\pb11mpi"
if errorlevel 1 exit 1

:: build!
cmake --build build --config Release --parallel %CPU_COUNT% -- -v -d stats
if errorlevel 1 exit 1

:: test!
cd %SRC_DIR%\build
ctest --output-on-failure --parallel %CPU_COUNT%
if errorlevel 1 exit 1

:: install!
cd %SRC_DIR%
cmake --build build --config Release --target install
if errorlevel 1 exit 1

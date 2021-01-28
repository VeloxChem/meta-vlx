setlocal EnableDelayedExpansion

:: configure!
cmake -S"%SRC_DIR%" ^
      -Bbuild ^
      -GNinja ^
      -DCMAKE_BUILD_TYPE:STRING=Release ^
      -DCMAKE_INSTALL_PREFIX:PATH="%PREFIX%" ^
      -DCMAKE_PREFIX_PATH:PATH="%LIBRARY_PREFIX%" ^
      -DCMAKE_CXX_COMPILER:STRING=clang-cl
if errorlevel 1 exit 1

:: build!
cmake --build build --config Release --parallel %CPU_COUNT% -- -v -d stats
if errorlevel 1 exit 1

:: test!
:: we only run unit tests here, integration tests are run later on
cd build
ctest -L unit --output-on-failure
if errorlevel 1 exit 1

:: install!
cd ..
cmake --build build --config Release --target install
if errorlevel 1 exit 1

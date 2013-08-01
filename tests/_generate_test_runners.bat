@echo off

rem -----------------------------------------------------
set GENERATOR="..\test_harness\Unity\scripts\makeTestRunner.py"

set TESTS_DIR="."

set OUTPUT_PATH="_all_tests.c"
rem -----------------------------------------------------

python %GENERATOR% %TESTS_DIR% -o %OUTPUT_PATH%
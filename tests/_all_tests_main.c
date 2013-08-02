#include "unity_fixture.h"
#include "my_static_lib.h"

void RunAllTests(void);

int main(int argc, char* argv[])
{
    #ifdef UNIT_TEST_VARIANT1
        MyStaticLib_vPrintTestMessage();
        MyStaticLib_vPrintTestMessage();
        MyStaticLib_vPrintTestMessage();
    #endif
    MyStaticLib_vPrintTestMessage();

    return UnityMain(argc, argv, RunAllTests);
}

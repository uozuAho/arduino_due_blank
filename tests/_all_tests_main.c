#include "unity_fixture.h"
#include "my_static_lib.h"

void RunAllTests(void);

int main(int argc, char* argv[])
{
    MyStaticLib_vPrintTestMessage();

    return UnityMain(argc, argv, RunAllTests);
}

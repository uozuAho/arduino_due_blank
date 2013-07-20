#include "unity_fixture.h"

extern void RunAllTests(void);

int main(int argc, char* argv[])
{
    return UnityMain(argc, argv, RunAllTests);
}

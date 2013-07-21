#include "unity_fixture.h"

void RunAllTests(void);

int main(int argc, char* argv[])
{
    return UnityMain(argc, argv, RunAllTests);
}

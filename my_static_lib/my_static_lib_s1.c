#include "my_static_lib_conf.h"

void MyStaticLib_vPrintTestMessage() {
    MY_STATIC_LIB_OUTPUT_CHAR('a');
    MY_STATIC_LIB_OUTPUT_CHAR('b');
    MY_STATIC_LIB_OUTPUT_CHAR('c');
    MY_STATIC_LIB_OUTPUT_CHAR('\n');
}


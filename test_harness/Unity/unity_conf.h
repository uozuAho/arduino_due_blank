#ifndef UNITY_CONF_H
#define UNITY_CONF_H

#ifdef RUN_UNIT_TESTS_HOST
    #define UNITY_OUTPUT_CHAR(a)      putchar(a)
#else
    #define UNITY_OUTPUT_CHAR(a)      ArduinoPutchar(a)
#endif

#endif

/*
 * my_static_lib_conf.h
 *
 *  Created on: 01/08/2013
 *      Author: uozu
 */

#ifndef MY_STATIC_LIB_CONF_H_
#define MY_STATIC_LIB_CONF_H_

#ifdef TARGET_HOST
    #include <stdio.h>
    #define MY_STATIC_LIB_OUTPUT_CHAR(a)      putchar(a)
#else
    int ArduinoPutchar(int c);
    #define MY_STATIC_LIB_OUTPUT_CHAR(a)      ArduinoPutchar(a)
#endif

#endif /* MY_STATIC_LIB_CONF_H_ */

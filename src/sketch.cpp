/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.

  This example code is in the public domain.
 */

#include "Arduino.h"
#include "my_static_lib.h"

#ifdef __cplusplus
    #define C_BLOCK_BEGIN   extern "C" {
    #define C_BLOCK_END     }
#else
    #define C_BLOCK_BEGIN
    #define C_BLOCK_END
#endif

C_BLOCK_BEGIN
    #include "unity.h"
    #include "unity_fixture.h"

    // Unity can't use cpp functions
    int ArduinoPutchar(int c) {
        return Serial.print((char)c);
    }

    // Forward declaration of all tests - requires
    // unit tests to be built and linked
    void RunAllTests(void);
C_BLOCK_END

// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
int led = 13;

// the setup routine runs once when you press reset:
void setup() {
    // initialize the digital pin as an output.
    pinMode(led, OUTPUT);
    Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
    MyStaticLib_vPrintTestMessage();

    digitalWrite(led, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(1000);               // wait for a second
    digitalWrite(led, LOW);    // turn the LED off by making the voltage LOW
    delay(1000);               // wait for a second

    UnityMain(0, NULL, RunAllTests);
}

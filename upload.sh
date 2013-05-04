#!/bin/bash

# -----------------------------------------------------
# Set the following two variables to suit your system:
#
# Location of Arduino SDK
ARDUINO_SDK_LOC=/media/wozHome/uozu/toolchains/arduino-1.5.2

# Serial port that the Arduino Due is connected to
PORT=ttyACM0
# -----------------------------------------------------



# location of bossa - open source sam chip flasher
BOSSA_LOC=${ARDUINO_SDK_LOC}/hardware/tools

# Location of built program
BINARY=Debug/arduino_due_blank.bin

# First force a reset & flash erase by opening and closing
# the serial port at 1200bps
stty -F /dev/${PORT} raw ispeed 1200 ospeed 1200

# Now use bossa to upload the binary file
${BOSSA_LOC}/bossac --port=${PORT} -U false -e -w -v -b ${BINARY} -R

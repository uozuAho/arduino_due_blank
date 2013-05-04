arduino_due_blank_eclipse
=========================

This is an Eclipse project to be used as a base for any Arduino Due
software. It includes a pre-built arduino core for the Arduino Due,
a pre-built Atmel library for the Due's processor and all necessary
header files for those libraries

You'll need:

- Eclipse CDT 
  (http://www.eclipse.org/downloads/packages/eclipse-ide-cc-developers/junosr2)
- Eclipse ARM plugin (get through Eclipse marketplace)
- Arduino IDE (http://arduino.cc/en/Main/Software)
- MinGW  http://www.mingw.org/ for make (if you're using Windows)


Before you can build
====================
- Make sure the Arduino tools path is in your system path, either in the global
  PATH variable of your system or the PATH variable set within Eclipse. In my 
  case, I added C:\arduino-1.5.2\hardware\tools\g++_arm_none_eabi\bin to 
  Windows' PATH variable.
- Also make sure make is in PATH
- Finally, modify the upload.sh script to suit your system. This script 
  uploads the project to the Arduino Due). I'll make a Windows script 
  at some point
  
NOTE:
The arguments to the gcc compilers and linker are slightly different to those
given by the Arduino IDE. The output sections end up in different orders
(compare the map file from this project versus the Arduino IDE's blink 
example), however the program still runs on the Arduino so I don't think 
there's a problem...not sure yet though.


Alternatives to using Arduino SDK
=================================

This project currently requires the Arduino SDK for its ARM toolchain and 
bossa flashing tool. These can both be obtained separately:

- Bossa: http://www.shumatech.com/web/products/bossa

- ARM toolchains:
 - Mentor Graphics Sourcery CodeBench Lite Edition
   (http://www.mentor.com/embedded-software/sourcery-tools/sourcery-codebench/editions/lite-edition/)
 - Yagarto (http://www.yagarto.de/)
 - devKitARM (http://devkitpro.org/wiki/Getting_Started)
 - Linaro (https://launchpad.net/gcc-arm-embedded/+milestone/4.6-2012-q2-update)

NOTE:
Using the above Arduino alternatives won't get you out of having to comply 
with the GPL/LGPL etc. These licences cover various bits of the Arduino source
code, of which there is plenty in this project.


TODO
====

- Write Windows batch file for uploading to the Arduino

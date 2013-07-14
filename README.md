arduino_due_blank_eclipse
=========================

This is an Eclipse project to be used as a base for any Arduino Due
software. It includes a pre-built arduino core for the Arduino Due,
a pre-built Atmel library for the Due's processor and all necessary
header files for those libraries.

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
- Finally, modify the upload.sh/upload.bat script to suit your system. These 
  scripts upload the project to the Arduino Due.
  
NOTE:
The arguments to the gcc compilers and linker are slightly different to those
given by the Arduino IDE. The output sections end up in different orders
(compare the map file from this project versus the Arduino IDE's blink 
example), however the program still runs on the Arduino so I don't think 
there's a problem...not sure yet though.


Alternatives to using Arduino SDK
=================================

This project currently requires the Arduino SDK for its ARM toolchain and 
bossa flashing tool. The regular bossa flashing tool 
(http://www.shumatech.com/web/products/bossa) doesn't work, you need to 
use arduino's version.

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


Exceptions support 
==================

Although the Arduino IDE builds user code with the -fno-exceptions flag, exception
handling is supported by the toolchain. You can use C++ exceptions by removing the
above flag. The arduino toolchain's c library supports exceptions, so even if you 
don't use them, using some parts of the standard library will drag in exception
handling code (around 60kB). If you don't want this, you'll have to use another
toolchain. The only one I've found that has a standard library built without
exceptions support is Linaro (GCC ARM Embedded 4.7-2013-q1-update, using linker arg 
--specs=nano or something like that).


TODO
====

- Figure out why arduino-1.5.2-syscalls_sam3.c.o is needed during linking. This
  object is already within libarduino-1.5.2-core-Due.a, however the linker doesn't
  seem to be able to find it - use malloc and the linker will complain that _sbrk()
  is undefined.
- Extract syscalls from Arduino core library and add them to this project.

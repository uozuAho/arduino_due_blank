arduino_due_blank
=================

This is a project to be used as a base for any Arduino Due
software. It includes a pre-built arduino core for the Arduino Due,
a pre-built Atmel library for the Due's processor and all necessary
header files for those libraries.

Essential tools
---------------
- python 2.7
 - for running doit (see below)
 - for generating unit tests
- doit
 - build automation tool (like make/rake)
 - `pip install doit`
 - or download and install manually from http://pydoit.org/
- Arduino IDE 1.5.2 (http://arduino.cc/en/Main/Software)
 - Contains Arduino toolchain and 'bossa' tool for uploading to the Arduino

Optional tools
--------------
- Eclipse CDT
 - http://www.eclipse.org/cdt/
- gcc for development PC
 - eg. MinGW: http://www.mingw.org/
 - for building unit tests


Before you can build
====================
- Make sure the Arduino tools path is in your system path, either in the global
  PATH variable of your system. In my case, I added
  C:\arduino-1.5.2\hardware\tools\g++_arm_none_eabi\bin to Windows' PATH
  variable.
- Also make sure your python scripts directory is in the PATH variable, eg.
  in my case C:\Python27\Scripts
- Finally, modify the upload.sh/upload.bat script to suit your system. These
  scripts upload the project to the Arduino Due.


Alternatives to using Arduino SDK
=================================

This project currently requires the Arduino SDK for its bossa flashing tool.
The regular bossa flashing tool (http://www.shumatech.com/web/products/bossa)
doesn't work, you need to use arduino's version.

Other ARM toolchains
--------------------
- Mentor Graphics Sourcery CodeBench Lite Edition
  (http://www.mentor.com/embedded-software/sourcery-tools/sourcery-codebench/editions/lite-edition/)
- Yagarto (http://www.yagarto.de/)
- devKitARM (http://devkitpro.org/wiki/Getting_Started)
- Linaro (https://launchpad.net/gcc-arm-embedded/+milestone/4.6-2012-q2-update)

NOTE:
Using the above Arduino alternatives won't get you out of having to comply
with the GPL/LGPL etc. These licences cover various bits of the Arduino source
code, of which there is plenty in this project.


Other stuff I've noticed
========================

Exceptions support:

Although the Arduino IDE builds user code with the -fno-exceptions flag, exception
handling is supported by the toolchain. You can use C++ exceptions by removing the
above flag. The arduino toolchain's c library supports exceptions, so even if you
don't use them, using some parts of the standard library will drag in exception
handling code (around 60kB). If you don't want this, you'll have to use another
toolchain. The only one I've found that has a standard library built without
exceptions support is Linaro (GCC ARM Embedded 4.7-2013-q1-update, using linker arg
--specs=nano or something like that).

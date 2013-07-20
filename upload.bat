@echo off

rem -----------------------------------------------------
rem Set the following two variables to suit your system:
rem 
rem location of bossa - open source sam chip flasher
set BOSSA_LOC="D:\temp\arduino-1.5.2\hardware\tools"

rem Serial port that the Arduino Due is connected to
set PORT=COM8
rem -----------------------------------------------------


rem First force a reset & flash erase by opening and closing
rem the serial port at 1200bps
mode %PORT%:1200,n,8,1

timeout /T 2

rem Now use bossa to upload the binary file
%BOSSA_LOC%\bossac.exe --port=%PORT% -U false -e -w -v -b %1 -R

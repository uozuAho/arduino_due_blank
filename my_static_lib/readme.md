my static lib
=============

This directory contains source code to be compiled into a static library.
It can be a project in its own right and build without the enclosing 
project. However, the project should be able to configure and build the
library.

This represents my situation at work, where a library used by
many projects is included within other projects. Since the library is
under development, many changes are still occurring, therefore it is 
less tedious to include the library source rather than a pre-compiled
static library.
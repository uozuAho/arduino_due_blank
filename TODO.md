TODO
====

- Rename project - no longer Eclipse CDT-dependent

- Fix make dependency parser (doit_helpers)
 - Then can use gcc-generated dependency files rather than all headers

- Figure out why arduino-1.5.2-syscalls_sam3.c.o is needed during linking. This
  object is already within libarduino-1.5.2-core-Due.a, however the linker doesn't
  seem to be able to find it - use malloc and the linker will complain that _sbrk()
  is undefined.

- Extract syscalls from Arduino core library and add them to this project.

- Link to Unity git repo rather than having a copy in this project

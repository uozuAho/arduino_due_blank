Build tool branch readme
========================

Using Eclipse CDT to build the project is nice and easy, but doesn't
lend itself to build automation (which I am interested in).
I'm trying to find a build tool that isn't a pain to use, and 
so far it looks like they're all quite painful. Therefore, I 
need to find the least bad one.

Contenders:
- Cmake
- make
- waf
- Scons


Requirements
------------

- Basic requirement: replace Eclipse CDT dependency
 - Do exactly what CDT does, without CDT:
  - Easy(ish) project configuration
  - Dependency management
  - Build management
  
- Extended requirements:
 - Include arbitrary number of steps in build process, with proper 
   dependency management. Eg. code generation, test runs, doc
   generation
 - Support of any custom commands/build steps I can think of. Current
   example build process:
  - generate code (arbitrary number of files)
  - build
  - run tests
  - generate test report
  - Optional steps:
   - upload to embedded target
   - run tests on target
   - generate test report from embedded tests
   - build docs
   - build release archive/dir

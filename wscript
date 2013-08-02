""" Waf build script. Currently only supports unit test generation
    and host unit test build configuration
"""

# Project constants
PROJECT_NAME = 'ArduinoDue_blank'

MAJOR = 0
MINOR = 0
BUILD = 1

VERSION_STRING = "%d.%d.%d" % (MAJOR, MINOR, BUILD)


# Build script constants
DEBUG = True


# waf constants
top = '.'
out = 'waf_build'
APPNAME = PROJECT_NAME
VERSION = VERSION_STRING


# ---------------------------------------------
# Utility functions


# ---------------------------------------------
# waf instructions
import os

def options(ctx):
    ctx.load('compiler_c')


def configure(ctx):
    ctx.load('compiler_c')


def build(ctx):
    # Generate unit test runners
    genscripts = ctx.path.ant_glob('**/makeTestRunner.py')
    if len(genscripts) == 1:
        genscript = genscripts[0].abspath()
    else:
        raise Exception("len(genscripts) != 1")

    tests_dir = os.path.abspath('tests')
    test_depends = ctx.path.ant_glob(incl = ['tests/*.c'])
    test_depends.append(genscripts[0])
    test_runner = 'tests/_all_tests.c'

    ctx(rule='python '+genscript+' '+tests_dir+' -o ${TGT}',
        source = test_depends,
        target = test_runner)

    # Build host unit test config
    sources = ctx.path.ant_glob(incl = ['src/**/*.c',
                                        'my_static_lib/**/*.c',
                                        'tests/**/*.c',
                                        'test_harness/**/*.c'],
                                excl = ['sketch.cpp'])
    if test_runner not in sources:
        sources.append(test_runner)

    ctx.program(
        source       = sources,
        target       = PROJECT_NAME+'-'+VERSION_STRING+'-UnitTests_host',

        includes     = ["arduino_core/include",
                        "arduino_core/variants/arduino_due_x",
                        "device_libs/CMSIS/CMSIS/Include",
                        "device_libs/CMSIS/Device/ATMEL",
                        "device_libs/libsam",
                        "src",
                        "my_static_lib",
                        "test_harness/Unity"],

        defines      = ['TARGET_HOST'],

        lib          = ['m', 'gcc'],
        libpath      = [],
        linkflags    = [],

        cflags       = ['-O0', '-Wall'],
        dflags       = ['-g3']
    )

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
out = 'build'
APPNAME = PROJECT_NAME
VERSION = VERSION_STRING


# ---------------------------------------------
# Utility functions

# redundant...just use ant_glob
def getAllSourceFiles(ctx):
    return ctx.path.ant_glob(incl = ['src/**/*.c',
                                     'test_harness/**/*.c'],
                             excl = ['sketch.cpp'])

# ---------------------------------------------
# waf instructions

def options(ctx):
    ctx.load('compiler_c')


def configure(ctx):
    ctx.load('compiler_c')

def build(ctx):
    sources = getAllSourceFiles(ctx)

    ctx.program(
        source       = sources,
        target       = PROJECT_NAME+'-'+VERSION_STRING,

        includes     = ["arduino_core/include",
                        "arduino_core/variants/arduino_due_x",
                        "device_libs/CMSIS/CMSIS/Include",
                        "device_libs/CMSIS/Device/ATMEL",
                        "device_libs/libsam",
                        "src",
                        "test_harness/Unity"],

        defines      = ['RUN_UNIT_TESTS_HOST'],

        lib          = ['m', 'gcc'],
        libpath      = [],
        linkflags    = [],

        cflags       = ['-O0', '-Wall'],
        dflags       = ['-g3']
    )

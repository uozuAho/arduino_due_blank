import os


#-----------------------------------------------------------
# Constants

PROJECT_NAME = 'Arduino-due-blank'

VERSION_STRING = '0.0.1'

# Root directory of the entire project
# NOTE: This assumes the build script is run from
# the directory above 'doit_build_configs'
PROJECT_ROOT = ''

# All builds go under this directory
BUILD_ROOT = os.path.join(PROJECT_ROOT, 'doit_build')

# This dummy file is used to detect the presence of build_root
BUILD_ROOT_DUMMY_FILE = os.path.join(BUILD_ROOT, '.dummy')

# Path of the test runner generator script
TEST_RUNNER_GENERATOR = os.path.join(PROJECT_ROOT, 'test_harness', 'Unity',
                                     'scripts', 'makeTestRunner.py')

# Path of the generated test runner source
UNIT_TEST_RUNNER_SOURCE = os.path.join(BUILD_ROOT, 'generated_src',
                                       '_all_tests.c')


#-----------------------------------------------------------
# Functions

def from_proj_root(*args):
    """ Returns os.path.join(PROJECT_ROOT, *args) """
    return os.path.join(PROJECT_ROOT, *args)


def from_build_root(*args):
    """ Returns os.path.join(BUILD_ROOT, *args) """
    return os.path.join(BUILD_ROOT, *args)


def get_exe_target_name(name, extension):
    return PROJECT_NAME+'-'+VERSION_STRING+'-'+name+'.'+extension

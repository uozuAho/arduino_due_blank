import os

# Root directory of the entire project
# NOTE: This assumes the build script is run from
# the directory above 'doit_build_configs'
project_root = ''

# All builds go under this directory
build_root = os.path.join(project_root, 'doit_build')

# This dummy file is used to detect the presence of build_root
build_root_dummy_file = os.path.join(build_root, '.dummy')

test_runner_generator = os.path.join(project_root, 'test_harness', 'Unity',
                                     'scripts', 'makeTestRunner.py')

unit_test_runner_source = os.path.join(build_root, 'generated_src',
                                       '_all_tests.c')

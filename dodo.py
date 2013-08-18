import os
from doit_helpers import doit_help


#-----------------------------------------------------------
# Constants

DOIT_CONFIG = {'default_tasks': ['link']}

BUILD_ROOT_DIR = 'doit_build'

# This dummy file is used to detect the presence of BUILD_ROOT_DIR
BUILD_ROOT_DIR_DUMMY_FILE = os.path.join(BUILD_ROOT_DIR, '.dummy')

TEST_RUNNER_GENERATOR = os.path.join('test_harness', 'Unity', 'scripts', 'makeTestRunner.py')
UNIT_TEST_RUNNER_SOURCE = os.path.join(BUILD_ROOT_DIR, 'generated_src', '_all_tests.c')


#-----------------------------------------------------------
# Build configurations


class UnitTestsHost_BuildConfig:
    build_dir = os.path.join(BUILD_ROOT_DIR, 'UnitTests_host')
    obj_dir = os.path.join(build_dir, 'obj')

    compiler = 'gcc'
    compiler_definitions = ['TARGET_HOST']
    compiler_flags = ['-O0', '-g3', '-Wall']
    compiler_include_dirs = [
        os.path.join('arduino_core', 'include'),
        os.path.join('arduino_core', 'variants', 'arduino_due_x'),
        os.path.join('device_libs', 'CMSIS', 'CMSIS', 'Include'),
        os.path.join('device_libs', 'CMSIS', 'Device', 'ATMEL'),
        os.path.join('device_libs', 'libsam'),
        os.path.join('src'),
        os.path.join('my_static_lib'),
        os.path.join('test_harness', 'Unity')
    ]

    linker = 'gcc'

    sources = doit_help.find_files(['src', 'tests', 'test_harness', 'my_static_lib'],
                                   exclude_patterns=['sketch.cpp'])

    # manually add auto-generated sources as they can't be found before building
    sources += [UNIT_TEST_RUNNER_SOURCE]

    objects = [os.path.join(obj_dir, x).replace('.c', '.o') for x in sources]

    depends = [x.replace('.o', '.d') for x in objects]

    exe_target = os.path.join(build_dir, 'ArduinoDue_blank-UnitTestHost.exe')


def make_compile_command(cfg, obj_path, source_path):
    """ Return a compiler command string """
    cmd_args = [cfg.compiler]
    cmd_args += ['-D'+d for d in cfg.compiler_definitions]
    cmd_args += ['-I'+i for i in cfg.compiler_include_dirs]
    cmd_args += cfg.compiler_flags + ['-c']
    cmd_args += ['-MMD', '-MP', '-MF', obj_path.replace('.o', '.d')]
    cmd_args += ['-o', obj_path]
    cmd_args += [source_path]
    return ''.join([arg+' ' for arg in cmd_args])


def make_link_command(cfg, output_path, object_list):
    cmd_args = [cfg.linker]
    cmd_args += object_list
    cmd_args += ['-o', output_path]
    cmd_args += ['-lm', '-lgcc']
    return ''.join([arg+' ' for arg in cmd_args])


def get_header_dependency_dict(dep_file_list):
    deps = {}
    for dep_file in dep_file_list:
        if os.path.isfile(dep_file):
            temp_deps = doit_help.get_dependencies_from_file(dep_file)
            deps.update(temp_deps)
    return deps


#-----------------------------------------------------------
# Tasks


def task_generate_test_runner():
    "Generate test runner"
    return {
        'actions': [(doit_help.create_dirs, [UNIT_TEST_RUNNER_SOURCE]),
                    'python '+TEST_RUNNER_GENERATOR+' tests -o '+UNIT_TEST_RUNNER_SOURCE],
        'targets': [UNIT_TEST_RUNNER_SOURCE],
        'clean': True
    }


def task_create_build_dirs():
    "create build directory structure"
    cfg = UnitTestsHost_BuildConfig

    return {
        'actions': [(doit_help.create_dirs, cfg.objects),
                    'echo "" > '+BUILD_ROOT_DIR_DUMMY_FILE],
        'targets': [BUILD_ROOT_DIR_DUMMY_FILE],
        'clean': True
    }


def task_compile():
    cfg = UnitTestsHost_BuildConfig
    dep_dict = get_header_dependency_dict(cfg.depends)
    for source in cfg.sources:
        target = os.path.join(cfg.obj_dir, source.replace('.c', '.o'))
        dependencies = [BUILD_ROOT_DIR_DUMMY_FILE] + [source]
        if target in dep_dict:
            dependencies += dep_dict[target]
        yield {
            'name': source,
            'actions': [make_compile_command(cfg, target, source)],
            'targets': [target],
            'file_dep': dependencies,
            'clean': True
        }


def task_link():
    cfg = UnitTestsHost_BuildConfig
    return {
        'actions': [make_link_command(cfg, cfg.exe_target, cfg.objects)],
        'file_dep': UnitTestsHost_BuildConfig.objects,
        'targets': [cfg.exe_target],
        'clean': True
    }

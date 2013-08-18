import os
from doit_helpers import doit_help

DOIT_CONFIG = {'default_tasks': ['link']}

# Starting with unit test host build configuration

BUILD_ROOT_DIR = 'doit_build'

# ------------------------------------------------------
# Test runner generator definitions

TEST_RUNNER_GENERATOR = os.path.join('test_harness', 'Unity', 'scripts', 'makeTestRunner.py')
UNIT_TEST_RUNNER_SOURCE = os.path.join('tests', '_all_tests.c')

# ------------------------------------------------------
# Unit tests host build config


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


# ------------------------------------------------------
# Rules


def task_generate_test_runner():
    "Generate test runner"
    return {
        'actions': ['python '+TEST_RUNNER_GENERATOR+' tests -o '+UNIT_TEST_RUNNER_SOURCE],
        'targets': [UNIT_TEST_RUNNER_SOURCE],
        'clean': True
    }

# ----------------------------
# Unit tests host build rules


def task_link():
    cfg = UnitTestsHost_BuildConfig
    return {
        'actions': [make_link_command(cfg, cfg.exe_target, cfg.objects)],
        'file_dep': UnitTestsHost_BuildConfig.objects,
        'targets': [cfg.exe_target],
        'clean': True
    }


def task_compile():
    cfg = UnitTestsHost_BuildConfig
    dummy_file = os.path.join(cfg.obj_dir, 'dummy.txt')
    for source in cfg.sources:
        target = os.path.join(cfg.obj_dir, source.replace('.c', '.o'))
        dependencies = [dummy_file] + [source]
        yield {
            'name': source,
            'actions': [make_compile_command(cfg, target, source)],
            'targets': [target],
            'file_dep': dependencies,
            'clean': True
        }


def create_build_dirs(*paths):
    dirs_to_create = set([os.path.dirname(path) for path in paths])

    for path in dirs_to_create:
        try:
            os.makedirs(path)
        except os.error:
            pass


def task_create_build_dirs():
    "create build directory structure"
    cfg = UnitTestsHost_BuildConfig

    dummy_file = os.path.join(cfg.obj_dir, 'dummy.txt')

    return {
        'actions': [(create_build_dirs, cfg.objects),
                    'echo "" > '+dummy_file],
        'targets': [dummy_file],
        'clean': True
    }

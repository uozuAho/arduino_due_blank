import os
import build_globals
import utilities

#-----------------------------------------------------------
# Constants

# Name of this build configuration
NAME = 'unit_tests_host'

DESCRIPTION = "Builds unit tests to be run on the host system"

# Directory under which all built files/directories will be placed
BUILD_DIR = build_globals.from_build_root(NAME)

# Dummy file that signifies the existence of required build directories
BUILD_DIR_DUMMY = os.path.join(BUILD_DIR, '.dummy')

# Directory to place all c object files
OBJ_DIR = os.path.join(BUILD_DIR, 'obj')

COMPILER = 'gcc'
COMPILER_DEFINITIONS = ['TARGET_HOST']
COMPILER_FLAGS = ['-O0', '-g3', '-Wall']
COMPILER_INCLUDE_DIRS = [
    build_globals.from_proj_root('arduino_core', 'include'),
    build_globals.from_proj_root('arduino_core', 'variants', 'arduino_due_x'),
    build_globals.from_proj_root('device_libs', 'CMSIS', 'CMSIS', 'Include'),
    build_globals.from_proj_root('device_libs', 'CMSIS', 'Device', 'ATMEL'),
    build_globals.from_proj_root('device_libs', 'libsam'),
    build_globals.from_proj_root('src'),
    build_globals.from_proj_root('my_static_lib'),
    build_globals.from_proj_root('test_harness', 'Unity')
]

LINKER = 'gcc'

SOURCES = utilities.find_files(['src', 'tests', 'test_harness', 'my_static_lib'],
                               exclude_patterns=['sketch.cpp'])

HEADERS = utilities.find_files(['src', 'tests', 'test_harness', 'my_static_lib'],
                               extensions=['.h'],
                               exclude_patterns=['sketch.cpp'])

# manually add auto-generated sources as they can't be found before building
SOURCES += [build_globals.UNIT_TEST_RUNNER_SOURCE]

OBJECTS = [build_globals.source_to_obj(source, OBJ_DIR) for source in SOURCES]

EXE_TARGET_NAME = build_globals.get_exe_target_name(NAME, 'exe')

EXE_TARGET = os.path.join(BUILD_DIR, EXE_TARGET_NAME)


#-----------------------------------------------------------
# Functions


def arg_list_to_command_string(arg_list):
    return ''.join([arg+' ' for arg in arg_list])


def get_compile_command(source_path):
    """ Return a compiler command string """
    cmd_args = [COMPILER]
    cmd_args += ['-D'+d for d in COMPILER_DEFINITIONS]
    cmd_args += ['-I'+i for i in COMPILER_INCLUDE_DIRS]
    cmd_args += COMPILER_FLAGS + ['-c']
    cmd_args += ['-o', build_globals.source_to_obj(source_path, OBJ_DIR)]
    cmd_args += [source_path]
    return arg_list_to_command_string(cmd_args)


def get_link_command():
    cmd_args = [LINKER]
    cmd_args += OBJECTS
    cmd_args += ['-o', EXE_TARGET]
    cmd_args += ['-lm', '-lgcc']
    return arg_list_to_command_string(cmd_args)


def create_build_dirs():
    utilities.create_dirs(OBJECTS)
    # Create the dummy file
    with open(BUILD_DIR_DUMMY, 'w') as ofile:
        ofile.write('')


def get_build_dir_task():
    return {
        'name': 'create build dirs',
        'actions': [create_build_dirs],
        'targets': [BUILD_DIR_DUMMY]
    }


def get_compile_tasks():
    tasks = [get_build_dir_task()]

    for source in SOURCES:
        target = build_globals.source_to_obj(source, OBJ_DIR)
        dependencies = [BUILD_DIR_DUMMY] + [source] + HEADERS
        tasks.append({
            'name': source.replace('.c', '.o'),
            'actions': [get_compile_command(source)],
            'targets': [target],
            'file_dep': dependencies,
            'clean': True
        })
    return tasks


def get_link_task():
    return {
        'name': EXE_TARGET_NAME,
        'actions': [get_link_command()],
        'file_dep': OBJECTS,
        'targets': [EXE_TARGET],
        'clean': True
    }

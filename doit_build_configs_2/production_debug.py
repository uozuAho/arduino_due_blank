import os
import build_globals
import utilities

#-----------------------------------------------------------
# Constants

# Name of this build configuration
NAME = 'production_debug'

DESCRIPTION = "Builds target executable with extra debugging information"

# Directory under which all built files/directories will be placed
BUILD_DIR = build_globals.from_build_root(NAME)

# Dummy file that signifies the existence of required build directories
BUILD_DIR_DUMMY = os.path.join(BUILD_DIR, '.dummy')

# Directory to place all c object files
OBJ_DIR = os.path.join(BUILD_DIR, 'obj')

#-----------------------------------------------------------
# C build settings

C_SOURCE_DIRS = [
    build_globals.from_proj_root('src'),
    build_globals.from_proj_root('tests'),
    build_globals.from_proj_root('test_harness'),
    build_globals.from_proj_root('my_static_lib')
]

C_SOURCES = utilities.find_files(C_SOURCE_DIRS, extensions=['.c'],
                                 exclude_patterns=['all_tests_main.c'])

C_HEADERS = utilities.find_files(C_SOURCE_DIRS, extensions=['.h'])

C_COMPILER = 'arm-none-eabi-gcc'

C_COMPILER_DEFINITIONS = [
    'printf=iprintf',
    'F_CPU=84000000L',
    'ARDUINO=152',
    '__SAM3X8E__',
    'USB_PID=0x003e',
    'USB_VID=0x2341',
    'USBCON',
]

C_COMPILER_FLAGS = [
    '-Os',
    '-g',
    '-Wall',
    '-ffunction-sections',
    '-fdata-sections',
    '-nostdlib',
    '--param max-inline-insns-single=500'
]

C_COMPILER_INCLUDE_DIRS = [
    build_globals.from_proj_root('arduino_core', 'include'),
    build_globals.from_proj_root('arduino_core', 'variants', 'arduino_due_x'),
    build_globals.from_proj_root('device_libs', 'CMSIS', 'CMSIS', 'Include'),
    build_globals.from_proj_root('device_libs', 'CMSIS', 'Device', 'ATMEL'),
    build_globals.from_proj_root('device_libs', 'libsam'),
    build_globals.from_proj_root('src'),
    build_globals.from_proj_root('my_static_lib'),
    build_globals.from_proj_root('test_harness', 'Unity')
]


#-----------------------------------------------------------
# C++ build settings

CPP_SOURCE_DIRS = [
    'src',
    'tests',
    'test_harness',
    'my_static_lib'
]

CPP_SOURCES = utilities.find_files(CPP_SOURCE_DIRS, extensions=['.cpp'])

CPP_HEADERS = utilities.find_files(CPP_SOURCE_DIRS, extensions=['.hpp'])

CPP_COMPILER = 'arm-none-eabi-gcc'

CPP_COMPILER_DEFINITIONS = [
    'printf=iprintf',
    'F_CPU=84000000L',
    'ARDUINO=152',
    '__SAM3X8E__',
    'USB_PID=0x003e',
    'USB_VID=0x2341',
    'USBCON'
]

CPP_COMPILER_FLAGS = [
    '-Os',
    '-g',
    '-Wall',
    '-ffunction-sections',
    '-fdata-sections',
    '-nostdlib',
    '--param max-inline-insns-single=500'
]

CPP_COMPILER_INCLUDE_DIRS = [
    build_globals.from_proj_root('arduino_core', 'include'),
    build_globals.from_proj_root('arduino_core', 'variants', 'arduino_due_x'),
    build_globals.from_proj_root('device_libs', 'CMSIS', 'CMSIS', 'Include'),
    build_globals.from_proj_root('device_libs', 'CMSIS', 'Device', 'ATMEL'),
    build_globals.from_proj_root('device_libs', 'libsam'),
    build_globals.from_proj_root('src'),
    build_globals.from_proj_root('my_static_lib'),
    build_globals.from_proj_root('test_harness', 'Unity')
]


#-----------------------------------------------------------
# Linker settings

LINKER = 'arm-none-eabi-gcc'

LINKER_FLAGS = [
    '-Wl,--cref',
    '-Wl,--check-sections',
    '-Wl,--gc-sections',
    '-Wl,--entry=Reset_Handler',
    '-Wl,--unresolved-symbols=report-all',
    '-Wl,--warn-common',
    '-Wl,--warn-section-align',
    '-Wl,--warn-unresolved-symbols'
]

LINKER_INCLUDE_DIRS = [
    build_globals.from_proj_root('arduino_core'),
    build_globals.from_proj_root('arduino_core', 'variants', 'arduino_due_x')
]

LINKER_LIBS = [
    'arduino-1.5.2-core-Due',
    'sam_sam3x8e_gcc_rel'
]

LINKER_SCRIPT_FILE = build_globals.from_proj_root('arduino_core', 'variants', 'arduino_due_x', 'linker_scripts', 'gcc', 'flash.ld')


#-----------------------------------------------------------
# Other settings

ALL_SOURCES = C_SOURCES + CPP_SOURCES

OBJECTS = [utilities.source_to_obj(src, OBJ_DIR) for src in ALL_SOURCES]

EXE_TARGET_NAME = build_globals.get_exe_target_name(NAME, 'elf')

EXE_TARGET = os.path.join(BUILD_DIR, EXE_TARGET_NAME)


#-----------------------------------------------------------
# Functions


def arg_list_to_command_string(arg_list):
    return ''.join([arg+' ' for arg in arg_list])


def get_c_compile_command(source_path):
    cmd_args = [C_COMPILER]
    cmd_args += ['-D'+d for d in C_COMPILER_DEFINITIONS]
    cmd_args += ['-I'+i for i in C_COMPILER_INCLUDE_DIRS]
    cmd_args += C_COMPILER_FLAGS + ['-c']
    cmd_args += ['-o', utilities.source_to_obj(source_path, OBJ_DIR)]
    cmd_args += [source_path]
    return arg_list_to_command_string(cmd_args)


def get_cpp_compile_command(source_path):
    cmd_args = [CPP_COMPILER]
    cmd_args += ['-D'+d for d in CPP_COMPILER_DEFINITIONS]
    cmd_args += ['-I'+i for i in CPP_COMPILER_INCLUDE_DIRS]
    cmd_args += CPP_COMPILER_FLAGS + ['-c']
    cmd_args += ['-o', utilities.source_to_obj(source_path, OBJ_DIR)]
    cmd_args += [source_path]
    return arg_list_to_command_string(cmd_args)


def get_link_command():
    cmd_args = [LINKER]
    cmd_args += LINKER_FLAGS
    cmd_args += ['-L'+d for d in LINKER_INCLUDE_DIRS]
    cmd_args += ['-T'+LINKER_SCRIPT_FILE]
    cmd_args += ['-o', EXE_TARGET]
    cmd_args += ['-Wl,--start-group']
    cmd_args += [build_globals.from_proj_root('arduino_core', 'arduino-1.5.2-syscalls_sam3.c.o')]
    cmd_args += OBJECTS
    cmd_args += ['-l'+lib for lib in LINKER_LIBS]
    cmd_args += ['-Wl,--end-group']
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
    tasks += get_c_compile_tasks()
    tasks += get_cpp_compile_tasks()
    return tasks


def get_c_compile_tasks():
    tasks = []
    for source in C_SOURCES:
        target = utilities.source_to_obj(source, OBJ_DIR)
        dependencies = [BUILD_DIR_DUMMY] + [source] + C_HEADERS
        tasks.append({
            'name': source.replace('.c', '.o'),
            'actions': [get_c_compile_command(source)],
            'targets': [target],
            'file_dep': dependencies,
            'clean': True
        })
    return tasks


def get_cpp_compile_tasks():
    tasks = []
    for source in CPP_SOURCES:
        target = utilities.source_to_obj(source, OBJ_DIR)
        dependencies = [BUILD_DIR_DUMMY] + [source] + CPP_HEADERS
        tasks.append({
            'name': source.replace('.cpp', '.o'),
            'actions': [get_cpp_compile_command(source)],
            'targets': [target],
            'file_dep': dependencies,
            'clean': True
        })
    return tasks


def get_link_task():
    """ TODO: create hex file here: objcopy -O ihex input output """
    return {
        'name': EXE_TARGET_NAME,
        'actions': [get_link_command()],
        'file_dep': OBJECTS,
        'targets': [EXE_TARGET],
        'clean': True
    }

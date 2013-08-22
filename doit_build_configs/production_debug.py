import os
import build_globals

c_build_config = {
    'name': 'production_debug',
    'build_dir': os.path.join(build_globals.build_root, 'production_debug'),

    'compiler': 'arm-none-eabi-gcc',
    'compiler_definitions': [
        'printf=iprintf',
        'F_CPU=84000000L',
        'ARDUINO=152',
        '__SAM3X8E__',
        'USB_PID=0x003e',
        'USB_VID=0x2341',
        'USBCON',
    ],
    'compiler_flags': [
        '-Os',
        '-g',
        '-Wall'
        '-ffunction-sections',
        '-fdata-sections',
        '-nostdlib',
        '--param max-inline-insns-single=500'
    ],
    'compiler_include_dirs': [
        os.path.join('arduino_core', 'include'),
        os.path.join('arduino_core', 'variants', 'arduino_due_x'),
        os.path.join('device_libs', 'CMSIS', 'CMSIS', 'Include'),
        os.path.join('device_libs', 'CMSIS', 'Device', 'ATMEL'),
        os.path.join('device_libs', 'libsam'),
        os.path.join('src'),
        os.path.join('my_static_lib'),
        os.path.join('test_harness', 'Unity')
    ],

    'linker': 'arm-none-eabi-gcc',
    'linker_lib_dirs': [
        os.path.join('arduino_core', 'include'),
        os.path.join('arduino_core', 'variants', 'arduino_due_x'),
    ],
    'linker_libs': [
        'm',
        'gcc'
    ],
    'custom_linker_command': [
        '${LINKER}',
        '${LIB_DIRS}',
        '${FLAGS}',
        '-T'+os.path.join('arduino_core', 'variants', 'arduino_due_x', 'linker_scripts', 'gcc', 'flash.ld'),
        '-o ${TARGET}',
        '-Wl,--start-group',
        os.path.join('arduino_core', 'arduino-1.5.2-syscalls_sam3.c.o'),
        '${OBJECTS}',
        '-larduino-1.5.2-core-Due',
        '-lsam_sam3x8e_gcc_rel',
        '-Wl,--end-group'
        '${LIBS}',
    ],

    # Source search configuration
    'source_dirs': [
        'src',
        'tests',
        'test_harness',
        'my_static_lib'
    ],
    'source_extensions': ['.c', '.cpp'],
    'source_exclude_patterns': [],

    # Manual source file additions
    'source_files': [build_globals.unit_test_runner_source]
}

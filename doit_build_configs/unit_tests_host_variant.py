import os
import build_globals

c_build_config = {
    'name': 'unit_tests_host_variant',
    'build_dir': os.path.join(build_globals.build_root, 'unit_tests_host_variant'),

    'compiler': 'gcc',
    'compiler_definitions': ['TARGET_HOST', 'UNIT_TEST_VARIANT1'],
    'compiler_flags': ['-O0', '-g3', '-Wall'],
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

    'linker': 'gcc',

    # Source search configuration
    'source_dirs': [
        'src',
        'tests',
        'test_harness',
        'my_static_lib'
    ],
    'source_extensions': ['.c'],
    'source_exclude_patterns': ['sketch.cpp'],

    # Manual source file additions
    'source_files': [build_globals.unit_test_runner_source]
}

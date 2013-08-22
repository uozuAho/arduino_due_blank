""" Utilities for building c projects """

import os
import utilities
import unittest


# Run tests instead of main()
RUN_TESTS = True


#-----------------------------------------------------------
# Build config example

""" C build configurations should be specified as follows
    (python dictionary format)
"""
EXAMPLE_BUILD_CONFIG = {
    'name': 'UnitTests_host',
    'build_dir': 'UnitTests_host',

    'compiler': 'gcc',
    'compiler_definitions': ['TARGET_HOST'],
    'compiler_flags': ['-Wall'],
    'compiler_include_dirs': [
        os.path.join('arduino_core', 'include'),
    ],

    'linker': 'gcc',
    'linker_lib_dirs': ['lib1dir'],
    'linker_libs': ['lib1'],

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
    'source_files': ['asdf.c']
}


#-----------------------------------------------------------


def main():
    pass


def get_makedirs_task(cfg):
    if 'initialised' not in cfg:
        _init_cfg_for_build(cfg)

    dummy_file = os.path.join(cfg['build_dir'], '.dummy')

    return {
        'name': cfg['name'],
        'actions': [(utilities.create_dirs, [cfg['objects']]),
                    'echo "" > '+dummy_file],
        'targets': [dummy_file],
        'clean': True
    }


def get_compile_tasks(cfg, generate_deps=False):
    """ return a list of doit tasks to compile all sources.
    """
    if 'initialised' not in cfg:
        _init_cfg_for_build(cfg)

    tasks = []
    dep_dict = _get_header_dependency_dict(cfg['dependencies'])
    for source in cfg['source_files']:
        target = _source_to_obj(source, cfg['build_dir'])
        dependencies = [source]
        # TODO: depend on all headers
        # if not generate_deps:
        #     dependencies +=
        if target in dep_dict:
            dependencies += dep_dict[target]
        tasks.append({
            'name': cfg['name']+source,
            'actions': [_get_gcc_compile_command(cfg, source, generate_deps)],
            'targets': [target],
            'file_dep': dependencies,
            'clean': True
        })
    return tasks


def get_link_tasks(cfg):
    if 'initialised' not in cfg:
        _init_cfg_for_build(cfg)


def _init_cfg_for_build(cfg):
    if 'initialised' in cfg:
        raise Exception('re-initialisation attempted for cfg: '+cfg['name'])

    _build_source_file_list(cfg)
    _build_obj_and_dep_lists(cfg)

    cfg['initialised'] = True


def _build_source_file_list(cfg):
    """ Build the configuration's source file list based
        on its search parameters
    """
    sources = utilities.find_files(cfg['source_dirs'], cfg['source_extensions'],
                                   cfg['source_exclude_patterns'])

    if 'source_files' in cfg:
        cfg['source_files'] += sources
    else:
        cfg['source_files'] = sources


def _build_obj_and_dep_lists(cfg):
    if 'source_files' not in cfg:
        raise Exception('No source files in cfg: '+cfg['name'])

    if 'objects' in cfg:
        raise Exception('objects already listed in cfg: '+cfg['name'])

    cfg['objects'] = [_source_to_obj(src, cfg['build_dir']) for src in cfg['source_files']]
    cfg['dependencies'] = [_source_to_dep(src, cfg['build_dir']) for src in cfg['source_files']]


def _source_to_obj(source_path, build_dir):
    """ Return an object file path from a source file
        and a build directory
    """
    return os.path.join(build_dir, source_path.replace('.c', '.o'))


class SourceToObjTests(unittest.TestCase):
    def setUp(self):
        self.source1 = os.path.join('a', 'b', 'c.c')
        self.source2 = os.path.join('a.c')
        self.build_dir = os.path.join('build')

    def test_source_to_obj(self):
        self.assertEqual(_source_to_obj(self.source1, self.build_dir),
                         os.path.join('build', 'a', 'b', 'c.o'))
        self.assertEqual(_source_to_obj(self.source2, self.build_dir),
                         os.path.join('build', 'a.o'))


def _source_to_dep(source_path, build_dir):
    """ Return a dependency file path from a source file
        and a build directory
    """
    return os.path.join(build_dir, source_path.replace('.c', '.d'))


class SourceToDepTests(unittest.TestCase):
    def setUp(self):
        self.source1 = os.path.join('a', 'b', 'c.c')
        self.source2 = os.path.join('a.c')
        self.build_dir = os.path.join('build')

    def test_source_to_dep(self):
        self.assertEqual(_source_to_dep(self.source1, self.build_dir),
                         os.path.join('build', 'a', 'b', 'c.d'))
        self.assertEqual(_source_to_dep(self.source2, self.build_dir),
                         os.path.join('build', 'a.d'))


def _get_gcc_compile_command(cfg, source, generate_deps=False):
    """ Return a gcc compile command string for the given
        source file.
    """
    object_file = _source_to_obj(source, cfg['build_dir'])
    dependency_file = _source_to_dep(source, cfg['build_dir'])

    cmd_args = [cfg['compiler']]
    cmd_args += ['-D'+d for d in cfg['compiler_definitions']]
    cmd_args += ['-I'+i for i in cfg['compiler_include_dirs']]
    cmd_args += cfg['compiler_flags'] + ['-c']
    if generate_deps:
        cmd_args += ['-MMD', '-MP', '-MF', dependency_file]
    cmd_args += ['-o', object_file]
    cmd_args += [source]
    return ''.join([arg+' ' for arg in cmd_args])


def _get_gcc_link_exe_command(cfg, target_path):
    if 'initialised' not in cfg:
        _init_cfg_for_build(cfg)

    cmd_args = [cfg['linker']]
    cmd_args += cfg['objects']
    cmd_args += ['-o', target_path]
    cmd_args += ['-L'+d for d in cfg['linker_lib_dirs']]
    cmd_args += ['-l'+x for x in cfg['linker_libs']]
    return ''.join([arg+' ' for arg in cmd_args])


class GetGccCommandTests(unittest.TestCase):
    def test_compile_command(self):
        cmd = _get_gcc_compile_command(EXAMPLE_BUILD_CONFIG, 'asdf.c', generate_deps=False)
        exp_cmd = 'gcc -DTARGET_HOST'
        exp_cmd += ' -I'+os.path.join('arduino_core', 'include')
        exp_cmd += ' -Wall -c'
        exp_cmd += ' -o '+os.path.join('UnitTests_host', 'asdf.o')
        exp_cmd += ' asdf.c '
        self.assertEqual(cmd, exp_cmd)

    def test_compile_command_with_deps(self):
        cmd = _get_gcc_compile_command(EXAMPLE_BUILD_CONFIG, 'asdf.c', generate_deps=True)
        exp_cmd = 'gcc -DTARGET_HOST'
        exp_cmd += ' -I'+os.path.join('arduino_core', 'include')
        exp_cmd += ' -Wall -c -MMD -MP -MF '
        exp_cmd += os.path.join('UnitTests_host', 'asdf.d')
        exp_cmd += ' -o '+os.path.join('UnitTests_host', 'asdf.o')
        exp_cmd += ' asdf.c '
        self.assertEqual(cmd, exp_cmd)

    def test_link_command(self):
        cmd = _get_gcc_link_exe_command(EXAMPLE_BUILD_CONFIG, 'asdf.exe')
        exp_cmd = 'gcc '+_source_to_obj('asdf.c', EXAMPLE_BUILD_CONFIG['build_dir'])
        exp_cmd += ' -o asdf.exe -Llib1dir -llib1 '
        self.assertEqual(cmd, exp_cmd)


def _get_header_dependency_dict(dep_file_list):
    deps = {}
    for dep_file in dep_file_list:
        if os.path.isfile(dep_file):
            temp_deps = _get_dependencies_from_file(dep_file)
            deps.update(temp_deps)
    return deps


def _get_dependencies_from_file(path):
    """ Returns a dictionary of dependencies, indexed by target.
        Assumes the file is in makefile format.
    """
    with open(path) as infile:
        file_text = infile.read()

    try:
        return _get_makefile_deps(file_text)
    except:
        raise Exception('Error parsing '+path)


def _get_makefile_target(line):
    """ Reads a string (single line), returns a target & dependency
        tuple if a makefile target is defined in the string.
    """
    line_split = line.split(':')
    if len(line_split) > 2:
        raise Exception('Static patterns not supported')
    elif len(line_split) == 2:
        target = line_split[0].strip()
        deps = line_split[1].split()
        return target, deps
    return None, None


def _get_makefile_deps(string):
    """ Reads a string an returns all makefile targets
        as a dict dependencies indexed by target
    """
    dep_dict = {}

    # ensure all dependencies are on the same line as the target
    clean_string = _remove_newline_escapes(string)

    for line in clean_string.split('\n'):
        target, deps = _get_makefile_target(line)
        if target is not None:
            dep_dict[target] = deps
    return dep_dict


def _remove_newline_escapes(line):
    return line.replace('\\\n', '')


class GetDependencyTests(unittest.TestCase):
    def setUp(self):
        self.target_1 = 'asdf1: blah foo bar'
        self.target_3 = 'asdf3:'
        self.test_file = 'test_deps.d'

    def test_target_1(self):
        self.assertEqual(_get_makefile_target(self.target_1),
                         ('asdf1', ['blah', 'foo', 'bar']))

    def test_target_3(self):
        self.assertEqual(_get_makefile_target(self.target_3),
                         ('asdf3', []))

    def test_non_target(self):
        self.assertEqual(_get_makefile_target('asdf qwpeoi alsdkf ei'),
                         (None, None))

    def test_test_file(self):
        self.assertEqual(_get_dependencies_from_file('test_deps.d'), {
            'make_build\\UnitTests_host\\obj\\tests\\_all_tests.o': [
                'tests\\_all_tests.c',
                'test_harness\\Unity/unity.h',
                'test_harness\\Unity/unity_conf.h',
                'test_harness\\Unity/unity_internals.h',
                'test_harness\\Unity/unity_fixture.h',
                'test_harness\\Unity/unity.h'
            ],

            'test_harness\Unity/unity.h': [],

            'test_harness\Unity/unity_conf.h': [],

            'test_harness\Unity/unity_internals.h': []
        })

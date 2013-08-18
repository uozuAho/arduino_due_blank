import os
import unittest


# Run tests instead of main()
RUN_TESTS = True


def main():
    # print _remove_newline_escapes('asdf2: blah \\\n foo \\\n bar')
    with open('_all_tests.d') as infile:
        test_str = infile.read()

    # print test_str
    print _remove_newline_escapes(test_str)


def find_files(paths, extensions=['.c'], exclude_patterns=[], abspath=False):
    """ Return a list of files in the given path(s) with the given
        file extensions. Searches all subdirectories.

        @param paths: either a single directory or list of directories to search
    """
    if not isinstance(paths, list):
        paths = [paths]

    matches = []
    for path in paths:
        for root, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if filename.endswith(tuple(extensions)):
                    matches.append(os.path.join(root, filename))

    def isExcluded(match):
        for pattern in exclude_patterns:
            if pattern in match:
                return True
        return False

    # Filter excluded patterns, then convert to absolute paths
    # if required
    matches = [x for x in matches if not isExcluded(x)]
    if abspath:
        matches = [os.path.abspath(x) for x in matches]
    return matches


def get_dependencies_from_file(path):
    """ Returns a dictionary of dependencies, indexed by target.
        Assumes the file is in makefile format.
    """
    with open(path) as infile:
        file_text = infile.read()

    return get_makefile_deps(file_text)


def get_makefile_target(line):
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


def get_makefile_deps(string):
    """ Reads a string an returns all makefile targets
        as a dict dependencies indexed by target
    """
    dep_dict = {}

    # ensure all dependencies are on the same line as the target
    clean_string = _remove_newline_escapes(string)

    for line in clean_string.split('\n'):
        target, deps = get_makefile_target(line)
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
        self.assertEqual(get_makefile_target(self.target_1),
                         ('asdf1', ['blah', 'foo', 'bar']))

    def test_target_3(self):
        self.assertEqual(get_makefile_target(self.target_3),
                         ('asdf3', []))

    def test_non_target(self):
        self.assertEqual(get_makefile_target('asdf qwpeoi alsdkf ei'),
                         (None, None))

    def test_test_file(self):
        self.assertEqual(get_dependencies_from_file('test_deps.d'), {
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


if __name__ == "__main__":
    if RUN_TESTS:
        unittest.main()
    else:
        main()

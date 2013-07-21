SCRIPT_DESCRIPTION = """
    Takes a variable number of arguments, each of which is a
    directory that potentially contains source files with Unity
    test cases.

    Generates a c source file that contains the function "RunAllTests()",
    which can be called from your code to run all unit tests.
"""

# Script configuration. These can also be modified by command line args
class Config:
    # TODO: add some unit tests!
    # Run unit tests instead of main()
    RUN_TESTS = False

    # Allow extra debugging output
    DEBUG = False

    # TODO: Add ability to specify source file extensions
    # via command line args
    SOURCE_FILE_EXTENSIONS = [
        ".c"
    ]

    OUTPUT_FILE_PATH = "test.c"


import argparse
import os
import re
import textwrap
import unittest


def main():
    args = getCommandLineArgs()
    setConfigWithArgs(args)
    test_files = getAllTestFilesInDirs(args.input)

    all_tests = Tests()
    for path in test_files:
        all_tests.extend(getTestsFromFile(path))

    generateTestRunner(all_tests, Config.OUTPUT_FILE_PATH)


class Tests:
    def __init__(self):
        # Dictionary of tests, indexed by test group name
        self.groups = {}

    def append(self, test):
        if test.group in self.groups:
            self.groups[test.group].append(test.name)
        else:
            self.groups[test.group] = [test.name]

    def extend(self, tests):
        for test in tests:
            self.append(test)

    def __str__(self):
        out_str = ""
        for group in self.groups:
            out_str += "Tests in group "+group+":\n"
            for test in self.groups[group]:
                out_str += "  "+test+"\n"
        return out_str


class Test:
    def __init__(self, group, name):
        self.group = group
        self.name = name


def getCommandLineArgs():
    parser = argparse.ArgumentParser(description=textwrap.dedent(SCRIPT_DESCRIPTION),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('input', nargs='*', help='source files containing unit tests')
    parser.add_argument('-o', '--output', help="Output path. Defaults to all_tests.c in the current working dir.")
    parser.add_argument('-v', '--verbose', action='store_true', help="Verbose output as script runs")
    return parser.parse_args()


def setConfigWithArgs(args):
    if args.verbose:
        Config.DEBUG = True

    if args.output != None:
        Config.OUTPUT_FILE_PATH = args.output


def getAllSourceFilesContainingTestsInDir(path):
    source_files = getSourceFilesInDir(path)
    test_files = filter(containsUnityTests, source_files)

    if Config.DEBUG:
        print "Source files found in",path,":"
        for item in source_files:
            print "   ",item

        print "Source files containing tests:"
        for item in test_files:
            print "   ",item

    return test_files


def getSourceFilesInDir(path):
    """ Returns a list of files with source file extensions in the
        given dir. Does not search sub-directories
    """
    isSourceFile = lambda x: os.path.isfile(x) and os.path.splitext(x)[1] in Config.SOURCE_FILE_EXTENSIONS

    items = [os.path.join(path,item) for item in os.listdir(path)]

    return [os.path.abspath(x) for x in filter(isSourceFile, items)]


def containsUnityTests(filepath):
    """ Returns True if the file contains any Unity test cases """
    unity_header_present = False
    test_case_present = False

    with open(filepath) as f:
        for line in f:
            if unity_header_present == False:
                if "include" in line and "unity.h" in line:
                    unity_header_present = True
            else:
                if "TEST(" in line:
                    test_case_present = True

            # Save some time by not searching the rest of the file
            if unity_header_present and test_case_present:
                break

    return unity_header_present and test_case_present


def getTestsFromFile(path):
    test_function_declarations = getTestFunctionDeclarationsFromFile(path)
    tests = []
    for decl in test_function_declarations:
        tests.append(testDeclarationToTestClass(decl))
    return tests


def getTestFunctionDeclarationsFromFile(path):
    infile = open(path)
    intext = infile.read()
    infile.close()
    return getAllTestFunctionDeclarationsInString(intext)


def getAllTestFunctionDeclarationsInString(string):
    """ Return a list of test function declarations. These should be
        of the form:
            TEST(<test group>, <test name>)
        NOTE: doesn't handle newlines within test function
        declarations (I think)
    """
    function_pattern = re.compile(r'TEST\s*\(.*\)')
    raw_function_list = re.findall(function_pattern, string)
    return raw_function_list


def testDeclarationToTestClass(test_declaration):
    re_match = re.search(r'TEST\s*\((\w+)\s*,\s*(\w+)\s*\)', test_declaration)
    return Test(re_match.group(1), re_match.group(2))


def getAllTestFilesInDirs(path_list):
    paths = []
    for path in path_list:
        paths.extend(getAllSourceFilesContainingTestsInDir(path))
    return paths


def generateTestRunner(all_tests, output_path):
    with open(output_path, 'w') as outfile:
        outfile.write(getTestRunnerHeaderString())

        for group in all_tests.groups:
            outfile.write(getTestGroupRunnerString(group, all_tests.groups[group]))
            outfile.write("\n")

        outfile.write(getAllGroupRunnerString(all_tests.groups.keys()))


def getTestRunnerHeaderString():
    out_str = "/* This test runner file was automatically generated by \n"
    out_str += os.path.realpath(__file__) + "*/\n"
    out_str += '\n'
    out_str += '#include "unity.h"\n'
    out_str += '#include "unity_fixture.h"\n'
    out_str += '\n'
    return out_str


def getTestGroupRunnerString(group_name, test_list):
    out_str = ""
    out_str += "TEST_GROUP_RUNNER("+group_name+")\n"
    out_str += "{\n"
    for test in test_list:
        out_str += "    RUN_TEST_CASE("+group_name+", "+test+");\n"
    out_str += "}\n"
    return out_str


def getAllGroupRunnerString(groups):
    out_str = ""
    out_str += "void RunAllTests(void)\n"
    out_str += "{\n"
    for group in groups:
        out_str += "    RUN_TEST_GROUP("+group+");\n"
    out_str += "}\n"
    return out_str


if __name__ == "__main__":
    if Config.RUN_TESTS:
        unittest.main()
    else:
        main()
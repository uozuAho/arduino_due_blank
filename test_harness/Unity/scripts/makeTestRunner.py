SCRIPT_DESCRIPTION = """
    Takes a variable number of arguments, each of which is a
    directory that potentially contains source files with Unity
    test cases.

    Generates a c source file that contains the function "RunAllTests()"
    (or another name specified via command-line parameters),
    which can be called from your code to run all unit tests.
"""

# Run unit tests instead of main()
RUN_TESTS = False

# Script configuration. These can also be modified by command line args
class Config:
    # Allow extra debugging output
    DEBUG = False

    # TODO: Add ability to specify source file extensions
    # via command line args
    SOURCE_FILE_EXTENSIONS = [
        ".c"
    ]

    TEST_RUNNER_FUNCTION_NAME = "RunAllTests"

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
    tests = getTestsFromFiles(test_files)
    generateTestRunner(tests, Config.OUTPUT_FILE_PATH)

    print len(tests.getAllTests()),"tests found in",len(tests.getTestGroups()),"groups"


class Tests:
    def __init__(self):
        # Dictionary of tests, indexed by test group name
        self._groups = {}

    def append(self, test):
        if test.group in self._groups:
            self._groups[test.group].append(test.name)
        else:
            self._groups[test.group] = [test.name]

    def extend(self, tests):
        for test in tests:
            self.append(test)

    def getTestGroups(self):
        """ Returns a list of test group names """
        return self._groups.keys()

    def getTestsInGroup(self, group):
        """ Returns a list of tests in the given group.
            Raises a KeyError if the group doesn't exist.
        """
        return self._groups[group]

    def getAllTests(self):
        """ Returns a list of all tests from all groups """
        tests = []
        for group in self._groups:
            tests.extend(self._groups[group])
        return tests


class Test:
    def __init__(self, group, name):
        self.group = group
        self.name = name


def getCommandLineArgs():
    parser = argparse.ArgumentParser(description=textwrap.dedent(SCRIPT_DESCRIPTION),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('input', nargs='+', help='source files containing unit tests')
    parser.add_argument('-o', '--output', help="Output path. Defaults to all_tests.c in the current working dir.")
    parser.add_argument('-r', '--runner_name', help="Name of the test runner function. Default="+Config.TEST_RUNNER_FUNCTION_NAME)
    parser.add_argument('-v', '--verbose', action='store_true', help="Verbose output as script runs")
    return parser.parse_args()


def setConfigWithArgs(args):
    if args.verbose:
        Config.DEBUG = True

    if args.runner_name != None:
        Config.TEST_RUNNER_FUNCTION_NAME = args.runner_name

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


def getTestsFromFiles(path_list):
    tests = Tests()
    for path in path_list:
        test_function_declarations = getTestFunctionDeclarationsFromFile(path)
        for decl in test_function_declarations:
            test = testDeclarationToTestClass(decl)
            if test != None:
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
    re_match = re.search(r'\s*TEST\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)', test_declaration)
    if re_match != None:
        return Test(re_match.group(1), re_match.group(2))
    else:
        print "Warning: Couldn't parse declaration to test:",test_declaration


def getAllTestFilesInDirs(path_list):
    paths = []
    for path in path_list:
        paths.extend(getAllSourceFilesContainingTestsInDir(path))
    return paths


def generateTestRunner(all_tests, output_path):
    with open(output_path, 'w') as outfile:
        outfile.write(getTestRunnerHeaderString())

        for group in all_tests.getTestGroups():
            outfile.write(getTestGroupRunnerString(group, all_tests.getTestsInGroup(group)))
            outfile.write("\n")

        outfile.write(getAllGroupRunnerString(all_tests.getTestGroups()))


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
    out_str += "void "+Config.TEST_RUNNER_FUNCTION_NAME+"(void)\n"
    out_str += "{\n"
    for group in groups:
        out_str += "    RUN_TEST_GROUP("+group+");\n"
    out_str += "}\n"
    return out_str



# -------------------------------------------------------------------------------#
""" SELF TESTS """

class TestsClassTests(unittest.TestCase):
    def setUp(self):
        self.tests = Tests()
        self.tests.append(Test("group1", "test1"))
        self.tests.append(Test("group1", "test2"))
        self.tests.append(Test("group2", "test3"))
        self.tests.append(Test("group2", "test4"))

    def test_TestsClass(self):
        self.assertEqual(self.tests.getTestGroups(),["group1", "group2"])
        self.assertEqual(self.tests.getTestsInGroup("group1"),["test1", "test2"])
        self.assertEqual(self.tests.getTestsInGroup("group2"),["test3", "test4"])
        self.assertEqual(self.tests.getAllTests(),["test1", "test2","test3", "test4"])


class FunctionTests(unittest.TestCase):
    def test_getAllTestFunctionDeclarationsInString(self):
        decls = getAllTestFunctionDeclarationsInString("asdf")
        self.assertEqual(decls, [])

        decls = getAllTestFunctionDeclarationsInString("TEST(group1, test1)")
        self.assertEqual(decls, ["TEST(group1, test1)"])

        decls = getAllTestFunctionDeclarationsInString("TEST(group1, test1)\n"
                                                       "TEST(group1, test2)")

        self.assertEqual(decls, ["TEST(group1, test1)", "TEST(group1, test2)"])

        decls = getAllTestFunctionDeclarationsInString("TEST (  a  ,   b )    ")
        self.assertEqual(decls, ["TEST (  a  ,   b )"])

        decls = getAllTestFunctionDeclarationsInString("TEST\n(a,b)\n    ")
        self.assertEqual(decls, ["TEST\n(a,b)"])

    def test_testDeclarationToTestClass(self):
        test = testDeclarationToTestClass("TEST(group1, test1)")
        self.assertEqual(test.group, "group1")
        self.assertEqual(test.name, "test1")

        test = testDeclarationToTestClass(" TEST ( group1 , test2 ) ")
        self.assertEqual(test.group, "group1")
        self.assertEqual(test.name, "test2")

        test = testDeclarationToTestClass(" TEST ( group1 ,\n test3 ) ")
        self.assertEqual(test.group, "group1")
        self.assertEqual(test.name, "test3")


if __name__ == "__main__":
    if RUN_TESTS:
        unittest.main()
    else:
        main()
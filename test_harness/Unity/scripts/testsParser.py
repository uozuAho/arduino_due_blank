""" Goal: Take a variable number of arguments, which are paths of source
    files that contain Unity tests.

    Gathers tests groups and their tests together, which can be used
    to generate test runners.
"""

# Script configuration. These can also be modified by command line args
class Config:
    # Run unit tests instead of main()
    RUN_TESTS = False

    # Allow extra debugging output
    DEBUG = False


import argparse
import os
import re
import textwrap
import unittest


def main():
    args = getCommandLineArgs()
    setConfigWithArgs(args)
    all_tests = Tests()
    for path in args.input:
        all_tests.extend(getTestsFromFile(path))
    print all_tests


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
    description = """\
        Description with
        line breaks,            tabs, and uhh... that's it """
    parser = argparse.ArgumentParser(description=textwrap.dedent(description),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('input', nargs='*', help='source files containing unit tests')
    parser.add_argument('-v', '--verbose', action='store_true', help="Verbose output as script runs")
    return parser.parse_args()


def setConfigWithArgs(args):
    if args.verbose:
        Config.DEBUG = True


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


if __name__ == "__main__":
    if Config.RUN_TESTS:
        unittest.main()
    else:
        main()
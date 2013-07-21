""" Goal: Take a variable number of arguments, which are paths of source
    files that contain Unity tests.

    Generates a test runner source file.
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
import testsParser


def main():
    args = getCommandLineArgs()
    setConfigWithArgs(args)
    all_tests = testsParser.Tests()
    for path in args.input:
        all_tests.extend(testsParser.getTestsFromFile(path))
    print all_tests
    generateTestRunner(all_tests, "test.c")


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


def generateTestRunner(all_tests, output_path):
    with open(output_path, 'w') as outfile:
        outfile.write('#include "unity.h"\n'
                      '#include "unity_fixture.h"\n')
        outfile.write('\n')
        for group in all_tests.groups:
            outfile.write(getTestGroupRunnerString(group, all_tests.groups[group]))
            outfile.write("\n")

        outfile.write(getAllGroupRunnerString(all_tests.groups.keys()))


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
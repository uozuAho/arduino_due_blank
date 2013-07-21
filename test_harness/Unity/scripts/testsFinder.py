""" Goal: Takes a variable number of arguments on the command line,
    each of which are directories containing c files with Unity
    tests.

    Returns a list of all c file paths (absolute) containing at
    least one unit test.
"""

# Script configuration. These can also be modified by command line args
class Config:
    # Run unit tests instead of main()
    RUN_TESTS = False

    # Allow extra debugging output
    DEBUG = False

    SOURCE_FILE_EXTENSIONS = [
        ".c"
    ]


import argparse
import os
import textwrap
import unittest


def main():
    args = getCommandLineArgs()
    setConfigWithArgs(args)
    test_files = getAllTestFiles(args.input)
    printTestFiles(test_files)


def getCommandLineArgs():
    description = """\
        Description with
        line breaks,            tabs, and uhh... that's it """
    parser = argparse.ArgumentParser(description=textwrap.dedent(description),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('input', nargs='*', help='directories to search in')
    parser.add_argument('-v', '--verbose', action='store_true', help="Verbose output as script runs")
    return parser.parse_args()


def setConfigWithArgs(args):
    if args.verbose:
        Config.DEBUG = True


def getAllTestFiles(path_list):
    paths = []
    for path in path_list:
        paths.extend(getAllSourceFilesContainingTestsInDir(path))
    return paths


def printTestFiles(test_file_list):
    output_str = ""
    for path in test_file_list:
        output_str += '"'+path+'"' + ' '
    print output_str


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


if __name__ == "__main__":
    if Config.RUN_TESTS:
        unittest.main()
    else:
        main()
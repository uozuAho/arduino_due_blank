import os
import sys

sys.path.append('..')
from doit_helpers import dependency_parser


def find_files(paths, extensions, exclude_patterns=[], abspath=False):
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


def create_dirs(*paths):
    """ Create any dirs specified in *paths. *paths can be
        file and/or directory paths.
    """
    if len(paths) == 1:
        if type(paths[0]) == list:
            dirs_to_create = set([os.path.dirname(path) for path in paths[0]])
        else:
            dirs_to_create = set([os.path.dirname(path) for path in paths])

    for path in dirs_to_create:
        try:
            os.makedirs(path)
        except os.error:
            pass


def source_to_obj(source_path, dest_dir):
    """ Return the path of the object file to be built from the
        given source file
    """
    source_no_ext = os.path.splitext(source_path)[0]
    return os.path.join(dest_dir, source_no_ext + '.o')


def source_to_dep(source_path, dest_dir):
    """ Return the path of the dependency file that will be generated
        when compiling the source_path
    """
    source_no_ext = os.path.splitext(source_path)[0]
    return os.path.join(dest_dir, source_no_ext + '.d')


def get_obj_dependencies(obj_path):
    """ Get object file dependencies from a gcc-generated
        dependency file for the given object
    """
    depfile = obj_path.replace('.o', '.d')
    if os.path.isfile(depfile):
        deps = dependency_parser.get_gcc_depfile_deps(depfile)
        if obj_path not in deps:
            print 'warning:', obj_path, 'not in', deps
        else:
            return deps[obj_path]
    return None

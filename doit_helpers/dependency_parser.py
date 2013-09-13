def get_gcc_depfile_deps(path):
    """ Returns a dictionary of target : [dependencies] pairs
        obtained from the given gcc-generated dependency file
    """
    return _parse_gcc_depfile_by_line(path)


def _parse_gcc_depfile_by_line(path):
    """ Scan a gcc-generated dependency file line by line for targets
        and their dependencies. Returns a dictionary of
        target : [dependencies] pairs
    """

    def get_target_from_line(line):
        """ Return target, remainder if a target found in the line.
            Otherwise return None, None
        """
        line_split = line.split(': ')
        if len(line_split) == 2:
            return line_split[0], line_split[1]
        return None, None

    def get_deps_from_string(string):
        return [s for s in string.split() if s != '\\']

    target_dict = {}
    with open(path) as infile:
        current_target = None
        current_deps = []
        for line in infile:
            tgt, remainder = get_target_from_line(line)
            if tgt is None:
                current_deps += get_deps_from_string(line)
            else:
                if current_target is not None:
                    target_dict[current_target] = current_deps
                current_target = tgt
                current_deps = get_deps_from_string(remainder)
    target_dict[current_target] = current_deps
    return target_dict


# -----------------------------------------------------------------------
# Tests

TEST_DEP_FILE = 'test_dep_file.d'


def main():
    target_dict = _parse_gcc_depfile_by_line(TEST_DEP_FILE)
    for target in target_dict:
        print target, ': '
        print target_dict[target]
        print ''


if __name__ == '__main__':
    main()

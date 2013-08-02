""" Creates a directory structure based on the input files.
"""

import sys, os

dirs_to_create = set([os.path.dirname(path) for path in sys.argv[1:]])

for path in dirs_to_create:
	try:
		os.makedirs(path)
	except os.error:
		pass
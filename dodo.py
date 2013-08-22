import os
from doit_helpers import utilities as doit_utils
from doit_helpers import cbuild
from doit_build_configs import all_configs
from doit_build_configs import build_globals
from doit_build_configs import unit_tests_host

#-----------------------------------------------------------
# Constants

# DOIT_CONFIG = {'default_tasks': ['link']}

PROJECT_NAME = 'Arduino-due-blank'
VERSION_STRING = '0.0.1'

#-----------------------------------------------------------
# Tasks


def task_generate_test_runner():
    "Generate test runner"

    generate_runner_cmd = 'python '
    generate_runner_cmd += build_globals.test_runner_generator
    generate_runner_cmd += ' tests -o '
    generate_runner_cmd += build_globals.unit_test_runner_source

    return {
        'actions': [(doit_utils.create_dirs, [build_globals.unit_test_runner_source]),
                    generate_runner_cmd],
        'targets': [build_globals.unit_test_runner_source],
        'clean': True
    }


def task_create_build_dirs():
    for cfg in all_configs.all_configs:
        yield cbuild.get_makedirs_task(cfg)


def task_compile():
    for cfg in all_configs.all_configs:
        for task in cbuild.get_compile_tasks(cfg):
            yield task


def task_link():
    for cfg in all_configs.all_configs:
        exe_name = PROJECT_NAME+'-'+VERSION_STRING+'-'+cfg['name']+'.exe'
        exe_path = os.path.join(cfg['build_dir'], exe_name)
        yield cbuild.get_link_exe_task(cfg, exe_path)

from doit_build_configs_2 import build_globals
from doit_build_configs_2 import utilities

from doit_build_configs_2 import unit_tests_host
from doit_build_configs_2 import unit_tests_host_variant
from doit_build_configs_2 import production_debug


def task_generate_test_runner():
    "Generate test runner"

    generate_runner_cmd = 'python '
    generate_runner_cmd += build_globals.TEST_RUNNER_GENERATOR
    generate_runner_cmd += ' tests -o '
    generate_runner_cmd += build_globals.UNIT_TEST_RUNNER_SOURCE

    return {
        'actions': [(utilities.create_dirs, [build_globals.UNIT_TEST_RUNNER_SOURCE]),
                    generate_runner_cmd],
        'targets': [build_globals.UNIT_TEST_RUNNER_SOURCE],
        'clean': True
    }


def task_unit_tests_host():
    tasks = unit_tests_host.get_compile_tasks()
    tasks.append(unit_tests_host.get_link_task())

    for task in tasks:
        yield task


def task_unit_tests_host_variant():
    tasks = unit_tests_host_variant.get_compile_tasks()
    tasks.append(unit_tests_host_variant.get_link_task())

    for task in tasks:
        yield task


def task_production_debug():
    tasks = production_debug.get_compile_tasks()
    tasks.append(production_debug.get_link_task())

    for task in tasks:
        yield task

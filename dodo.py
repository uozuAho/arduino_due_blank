from doit_build_configs import build_globals
from doit_build_configs import utilities

from doit_build_configs import unit_tests_host
from doit_build_configs import unit_tests_host_variant
from doit_build_configs import production_debug

DOIT_CONFIG = {'default_tasks': ['unit_tests_host']}


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
    "Build and run unit tests on the dev PC"
    tasks = unit_tests_host.get_compile_tasks()
    tasks.append(unit_tests_host.get_link_task())
    tasks.append(unit_tests_host.get_run_test_task())

    for task in tasks:
        yield task


def task_unit_tests_host_variant():
    "Build and run unit tests on the dev PC - variant"
    tasks = unit_tests_host_variant.get_compile_tasks()
    tasks.append(unit_tests_host_variant.get_link_task())

    for task in tasks:
        yield task


def task_production_debug():
    "Build production firmware for the Arduino, with debugging info"
    tasks = production_debug.get_compile_tasks()
    tasks.append(production_debug.get_link_task())

    for task in tasks:
        yield task


def task_build_all():
    "Build all executable targets"
    return {
        'actions': ['echo "building everything"'],
        'file_dep': [
            unit_tests_host.EXE_TARGET,
            unit_tests_host_variant.EXE_TARGET,
            production_debug.EXE_TARGET
        ]
    }

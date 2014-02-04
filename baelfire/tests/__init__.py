from soktest.runner import TestRunner

import baelfire


def get_runner():
    runner = TestRunner(baelfire)
    return runner


def run():
    return get_runner().do_tests()


def get_all_test_suite():
    return get_runner().get_all_test_suite()

if __name__ == '__main__':
    run()

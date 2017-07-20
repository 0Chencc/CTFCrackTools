import logging
import unittest
from test.test_support import run_with_locale, run_unittest
from test.test_logging import BaseTest


class FileNameTest(BaseTest):

    log_format = "%(filename)s %(funcName)s %(name)s -> %(levelname)s: %(message)s"
    expected_log_pat = r"^([\w.]+) ([\w.]+) ([\w.]+) -> ([\w.]+): ([\d]+)$"
    # test_logging_jy.py test_filename_is_set root -> ERROR: 47
    message_num = 0

    def test_filename_is_set(self):
        # http://bugs.jython.org/issue1760
        log = self.root_logger
        log.error("47")
        self.assert_log_lines([
            ("test_logging_jy.py", "test_filename_is_set", "root", "ERROR", "47")])


@run_with_locale('LC_ALL', '')
def test_main():
    run_unittest(FileNameTest,)


if __name__ == "__main__":
    test_main()

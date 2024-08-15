import logging

import pytest

from utils.base import Base


class TestDemo():

    def test01(self):
        logging.info('testqsgou  1 == 1')
        assert (1 == 1)

    def test02(self):
        logging.info('testqsgou  1 == 1')
        assert (1 == 2)

    def test03(self):
        logging.info('testqsgou  1 == 3')
        assert (1 == 3)


if __name__ == '__main__':
    pytest.main(['-vs', './test_demo.py'])

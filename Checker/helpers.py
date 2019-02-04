# -*- coding: utf-8 -*-
import sys
import pytest


def check_pytest(file_name):
    if not hasattr(sys, '_called_from_test'):
        pytest.main([file_name])

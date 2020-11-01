#
# Copyright (C) 2011 - 2016 Satoru SATOH <ssato at redhat.com>
# Copyright (C) 2017 - 2018 Satoru SATOH <satoru.satoh at gmail.com>
#
# pylint: disable=missing-docstring
r"""Common utilities for test cases.
"""
import os
import pathlib
import shutil
import tempfile
import unittest

try:
    from unittest import SkipTest
except ImportError:
    from nose.plugins.skip import SkipTest


CNF_0 = dict(name="a", a=1, b=dict(b=[0, 1], c="C"))
SCM_0 = {"type": "object",
         "properties": {
             "name": {"type": "string"},
             "a": {"type": "integer"},
             "b": {"type": "object",
                   "properties": {
                       "b": {"type": "array",
                             "items": {"type": "integer"}}}}}}
# :seealso: tests/res/00-cnf.json
CNF_1 = {"a": 1, "b": {"b": [1, 2], "c": "C"}, "name": "aaa"}


def selfdir():
    """
    >>> selfdir().exist
    True
    """
    return pathlib.Path(__file__).parent.resolve()


def respath(filename: str) -> str:
    """
    :pattern: Resource path path or path glob pattern

    >>> assert respath("00-cnf.json").endswith('/res/00-cnf.json')
    >>>
    """
    return str(selfdir() / "res" / filename)


def setup_workdir():
    """
    >>> import os.path
    >>> workdir = setup_workdir()
    >>> assert workdir != '.'
    >>> assert workdir != '/'
    >>> os.path.exists(workdir)
    True
    >>> os.rmdir(workdir)
    """
    return tempfile.mkdtemp(dir="/tmp", prefix="python-anyconfig-tests-")


def cleanup_workdir(workdir):
    """
    FIXME: Danger!

    >>> import os.path
    >>> from os import linesep as lsep
    >>> workdir = setup_workdir()
    >>> os.path.exists(workdir)
    True
    >>> open(os.path.join(workdir, "workdir.stamp"), 'w').write("OK!" + lsep)
    >>> cleanup_workdir(workdir)
    >>> os.path.exists(workdir)
    False
    """
    assert workdir != '/'
    assert workdir != '.'

    os.system("rm -rf " + workdir)


def skip_test():
    raise SkipTest


class TestCaseWithWorkdir(unittest.TestCase):

    def setUp(self):
        self.workdir = pathlib.Path(setup_workdir()).resolve()

    def tearDown(self):
        workdir = self.workdir
        ng_dirs = ('/',
                   str(self.workdir.home()),
                   str(pathlib.Path('.').resolve()))

        if str(workdir) not in ng_dirs:
            shutil.rmtree(workdir)

# vim:sw=4:ts=4:et:

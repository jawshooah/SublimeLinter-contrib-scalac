#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Joshua Hagins
# Copyright (c) 2015 Joshua Hagins
#
# License: MIT
#

"""This module exports the Scalac plugin class."""

import json
import os
from os import path
from distutils.versionpredicate import VersionPredicate

from SublimeLinter.lint import Linter, util


class Scalac(Linter):

    """Provides an interface to scalac."""

    syntax = 'scala'
    executable = 'scalac'
    cmd = None
    version_args = '-version'
    version_re = r'(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 2.9.1'
    regex = (
        r'^(?P<file>.+?):(?P<line>\d+): '
        r'(?:(?P<error>error)|(?P<warning>warning)): '
        r'(?:\[.+?\] )?(?P<message>[^\r\n]+)\r?\n'
        r'[^\r\n]+\r?\n'
        r'(?P<col>[^\^]*)\^'
    )
    multiline = True
    tempfile_suffix = '-'
    error_stream = util.STREAM_STDERR
    word_re = r'^(\w+|([\'"]).+\2)'
    defaults = {
        'lint': '',
        'classpath': '',
        'classpath_filename': '',
        'target_directory': ''
    }
    inline_settings = ['classpath', 'classpath_filename']
    inline_overrides = 'lint'
    comment_re = r'\s*/[/*]'

    # Internal
    __version_satisfies = {}

    @classmethod
    def version_satisfies(cls, req):
        """Return whether executable_version satisfies req."""

        if req not in cls.__version_satisfies:
            predicate = VersionPredicate('SublimeLinter.scalac ({})'.format(req))
            cls.__version_satisfies[req] = predicate.satisfied_by(cls.executable_version)

        return cls.__version_satisfies[req]

    def cmd(self):
        """
        Return the command line to execute.

        We override this because we have to munge the -Xlint argument
        based on the 'lint' setting.

        """

        command = [self.executable_path, '-encoding', 'UTF8', '*']

        settings = self.get_view_settings()

        user_rules = settings.get('lint')

        if isinstance(user_rules, str):
            user_rules = user_rules.split(',')
        elif not isinstance(user_rules, list):
            user_rules = []

        # Positive overrides negative
        user_rules = {
            name for name in user_rules
            if not (name.startswith('-') and name[1:] in user_rules)
        }

        valid_rules = {
            name: rule for (name, rule) in self.all_rules.items()
            if rule.is_valid
        }

        for name in user_rules:
            neg = name.startswith('-')
            name = name[1:] if neg else name
            rule = valid_rules.get(name)
            if rule is not None:
                rule.disable() if neg else rule.enable()

        command += [r.flag for r in valid_rules.values()]

        classpath = settings.get('classpath')

        if isinstance(classpath, list) and all(isinstance(item, str) for item in classpath):
            classpath = ':'.join(classpath)
        elif not isinstance(classpath, str):
            classpath = ''

        classpath_filename = settings.get('classpath_filename')

        if classpath_filename:
            classpath_from_file = self.get_classpath(classpath_filename)
            if classpath_from_file:
                classpath += ':{}'.format(classpath_from_file)

        if classpath:
            command += ['-classpath', classpath]

        target_directory = settings.get('target_directory')

        if target_directory:
            os.makedirs(target_directory, exist_ok=True)
            command += ['-d', target_directory]

        return command

    @property
    def all_rules(self):
        """Return dict containing all rules as name: rule."""

        if not hasattr(self, '__rules'):
            script_dir = path.dirname(path.realpath(__file__))
            rules_file = path.join(script_dir, 'rules.json')
            with open(rules_file) as json_data:
                rules = json.load(json_data)
                self.__rules = {rule['name']: Rule(rule) for rule in rules}

        return self.__rules

    def get_classpath(self, classpath_filename):
        """Read classpath from file and return as str."""

        def strip_ws(cp_data):
            entries = cp_data.split(':')
            return ':'.join(x.strip() for x in entries)

        cp_path = util.find_file(
            path.dirname(self.filename),
            classpath_filename
        )

        if cp_path:
            with open(cp_path, 'r') as cp_file:
                cp_data = cp_file.read()
                return strip_ws(cp_data)

    def split_match(self, match):
        """
        Return the components of the match.

        We override this because scalac lints all referenced files,
        and we only want errors from the linted file.

        """

        if match:
            if match.group('file') != self.filename:
                match = None

        return super().split_match(match)


class Rule:

    """
    A scalac rule.

    Attributes:
        name (str): The name of this rule.
        description (str): A description of this rule.

    """

    def __init__(self, json_data):
        """
        Initialize a new Rule from the given JSON data.

        Args:
            json_data (dict): JSON representation of rule.

        """

        self.name = json_data['name']
        self.description = json_data['description']
        self.__flag = json_data['flag']
        self.__version_req = json_data['version']
        self.__valid = None
        self.__default = json_data['default']
        self.__enabled = self.is_default

    @property
    def flag(self):
        """Get the formatted CLI flag for this rule."""

        if self.__flag == '-Xlint':
            neg = '-' if not self.__enabled else ''
            return '{}:{}{}'.format(self.__flag, neg, self.name)
        else:
            neg = ':false' if not self.__enabled else ''
            return '{}{}'.format(self.__flag, neg)

    @property
    def is_default(self):
        """Return whether this rule is enabled by default for the current Scala version."""

        if not self.is_valid:
            return False
        elif isinstance(self.__default, str):
            self.__default = Scalac.version_satisfies(self.__default)

        return self.__default

    @property
    def is_valid(self):
        """Return whether this rule is valid for the current Scala version."""

        if self.__valid is None:
            self.__valid = Scalac.version_satisfies(self.__version_req)

        return self.__valid

    def enable(self):
        """Enable this rule."""

        self.__enabled = True

    def disable(self):
        """Disable this rule."""

        self.__enabled = False

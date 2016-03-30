#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import psycopg2
from psycopg2.extras import NamedTupleCursor

import os.path
from subprocess import check_call
import yaml

import canini.utils
import canini.arg

config_file = '~/.config/canini.yml'

try:
    with open(os.path.expanduser(config_file)) as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print("warning: config file '{}' missing".format(config_file))
    config = { 'modules': ['canini.user'] }

parser = canini.arg.parser(config['modules'])

conn = psycopg2.connect("postgres://postgres@/carnivora", cursor_factory=NamedTupleCursor)

try:
    args = parser.parse_args()
    func = args.func
except AttributeError:
    parser.print_usage()
    exit(2)
conn.commit()

func(args, conn)


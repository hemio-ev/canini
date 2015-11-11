#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import psycopg2
from psycopg2.extras import NamedTupleCursor

import os.path
from subprocess import check_call

import canini.utils
import canini.arg

parser = canini.arg.parser()

conn = psycopg2.connect("postgres://postgres@/carnivora", cursor_factory=NamedTupleCursor)

try:
    args = parser.parse_args()
    func = args.func
except AttributeError:
    parser.print_usage()
    exit(2)
conn.commit()

func(args, conn)


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
    args.func(args, conn)
except AttributeError:
    parser.print_usage()


#data = dbExec("SELECT *, ARRAY(SELECT CAST (role AS varchar) FROM backend.auth WHERE machine=m.name) AS authorized_roles FROM backend.machine AS m")
#printTable(data)
#
#data = dbExec("SELECT * FROM system.service")
#printTable(data)
#
#data = dbExec("SELECT * FROM system.service_entity")
#printTable(data)
#
#data = dbExec("SELECT * FROM system.service_entity_machine")
#printTable(data)


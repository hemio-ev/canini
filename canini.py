#!/usr/bin/env python3

import psycopg2
from psycopg2.extras import NamedTupleCursor

import os.path
from subprocess import check_call

from prettytable import (from_db_cursor, PrettyTable)

def printTable(data):
    if not data:
        print(PrettyTable(["EMPTY"]))
        return

    x = PrettyTable(data[0].keys())
    for row in data:
        x.add_row(row.values())
    print(x)

def dbExec(qry):
    cur.execute(qry)
    return list(map(lambda x: x._asdict(), cur.fetchall()))

conn = psycopg2.connect("postgres://postgres@/test1", cursor_factory=NamedTupleCursor)
cur = conn.cursor()
  
data = dbExec("SELECT machine, role FROM backend.auth")
printTable(data)

data = dbExec("SELECT *, ARRAY(SELECT CAST (role AS varchar) FROM backend.auth WHERE machine=m.name) AS authorized_roles FROM backend.machine AS m")
printTable(data)

data = dbExec("SELECT * FROM system.service")
printTable(data)

data = dbExec("SELECT * FROM system.service_entity")
printTable(data)

data = dbExec("SELECT * FROM system.service_entity_machine")
printTable(data)


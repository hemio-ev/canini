from canini import *

def add_command(subparsers):
    return subparsers.add_parser('chown', help='Change owner of an object').add_subparsers()

def complete(parser, table, where):
    parser.add_argument('newowner', metavar='<new owner>', help='New owner of object')
    parser.set_defaults(func=lambda args, conn: chown(table, where, args, conn))

def chown(table, where, args, conn):
    cond = [ '{}=%({})s'.format(name, where[name]) for name in where ]
    where_str = ' AND '.join(cond)
    sql_str = 'UPDATE {} SET owner=%(newowner)s WHERE {}'.format(table, where_str)

    cur = conn.cursor()
    cur.execute(sql_str, args.__dict__)

    if cur.rowcount != 1:
        print("Error, object not found. No owner change performed")

    conn.commit()


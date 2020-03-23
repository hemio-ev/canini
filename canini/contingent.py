import canini.utils

def add_commands_to_parser(subparsers):
    cmd = subparsers.add_parser('contingent', help='User contingents').add_subparsers()

    # list-inherit
    cmd_list_inherit = cmd.add_parser('list-inherit', help='List inherited contingents')
    cmd_list_inherit.set_defaults(func=list_inherit)

    cmd_list_inherit.add_argument('--owner', default='%')
    cmd_list_inherit.add_argument('--donor', default='%')

    # add-inherit
    cmd_add_inherit = cmd.add_parser('add-inherit', help='Inherite contingents from donor')
    cmd_add_inherit.set_defaults(func=add_inherit)

    cmd_add_inherit.add_argument('owner', metavar='<owner>')
    cmd_add_inherit.add_argument('donor', metavar='<donor>')
    cmd_add_inherit.add_argument('priority', metavar='<priority>', type=int)

    # revoke-inherit
    cmd_revoke_inherit = cmd.add_parser('revoke-inherit', help='Revoke inherited contingents')
    cmd_revoke_inherit.set_defaults(func=revoke_inherit)

    cmd_revoke_inherit.add_argument('owner', metavar='<owner>')
    cmd_revoke_inherit.add_argument('donor', metavar='<donor>')

def list_inherit(args, conn):
    cur = conn.cursor()

    cur.execute("""
     SELECT
      owner, donor, priority
     FROM system.inherit_contingent
     WHERE
      owner LIKE %(owner)s
      AND donor LIKE %(donor)s
     ORDER BY owner, priority DESC
    """, vars(args))
    canini.utils.printCurAsTable(cur)

def add_inherit(args, conn):
    cur = conn.cursor()

    cur.execute("""
     INSERT INTO system.inherit_contingent (owner, donor, priority)
      VALUES (%(owner)s, %(donor)s, %(priority)s)
    """, vars(args))

    conn.commit()

def revoke_inherit(args, conn):
    cur = conn.cursor()

    cur.execute("""
     DELETE FROM system.inherit_contingent
      WHERE owner=%(owner)s AND donor=%(donor)s
    """, vars(args))

    if cur.rowcount != 1:
        print("Error, inherit not found")

    conn.commit()


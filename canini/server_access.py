import canini

def add_objects_to_chown(subparsers):
    parser = subparsers.add_parser('server_access.user', help='Server access account')
    parser.add_argument('user', metavar='<user>')
    canini.chown.complete(parser, 'server_access.user', {'"user"': 'user'})

def add_commands_to_parser(subparsers):
    cmd = subparsers.add_parser('server_access', help='Server access').add_subparsers()
    
    # list-user
    cmd_list_alias = cmd.add_parser('list-user', help='List users')
    cmd_list_alias.set_defaults(func=list_user)

    cmd_list_alias.add_argument('--backend-status', default='%')
    cmd_list_alias.add_argument('--owner',          default='%')
    cmd_list_alias.add_argument('--user',           default='%')

    cmd_list_alias.add_argument('--long', action='store_true', help='List details')

def list_user(args, conn):
    cur = conn.cursor()

    select = ['"user"', 'subservice', 'owner']

    if args.long:
        select += ['service_entity_name', 'backend_status']

    cur.execute("""
     SELECT 
       """ + ', '.join(select) + """
     FROM server_access."user"
     WHERE
      COALESCE(backend_status, '') LIKE %(backend_status)s
      AND "user" LIKE %(user)s
      AND owner LIKE %(owner)s
     ORDER BY "user"
    """, vars(args))
    canini.utils.printCurAsTable(cur)

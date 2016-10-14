import canini

def add_objects_to_chown(subparsers):
    def args(name):
        x = subparsers.add_parser('email.' + name, help='Email ' + name)
        x.add_argument('address', metavar='<address>')
        canini.chown.complete(x, 'email.' + name, {"localpart || '@' || domain": 'address'})

    args("list")
    args("mailbox")
    args("redirection")

def add_commands_to_parser(subparsers):
    cmd = subparsers.add_parser('email', help='Email').add_subparsers()
    
    # list-alias
    cmd_list_alias = cmd.add_parser('list-alias', help='List aliases')
    cmd_list_alias.set_defaults(func=list_alias)

    cmd_list_alias.add_argument('--address',        default='%')
    cmd_list_alias.add_argument('--backend-status', default='%')
    cmd_list_alias.add_argument('--destination',   default='%')

    cmd_list_alias.add_argument('--long', action='store_true', help='List details')

    # list-mailbox
    cmd_list_mailbox = cmd.add_parser('list-mailbox', help='List mailboxes')
    cmd_list_mailbox.set_defaults(func=list_mailbox)

    cmd_list_mailbox.add_argument('--address',        default='%')
    cmd_list_mailbox.add_argument('--backend-status', default='%')
    cmd_list_mailbox.add_argument('--owner',          default='%')

    cmd_list_mailbox.add_argument('--long', action='store_true', help='List details')

    # list-redirection
    cmd_list_redirection = cmd.add_parser('list-redirection', help='List redirections')
    cmd_list_redirection.set_defaults(func=list_redirection)

    cmd_list_redirection.add_argument('--address',        default='%')
    cmd_list_redirection.add_argument('--backend-status', default='%')
    cmd_list_redirection.add_argument('--destination',    default='%')
    cmd_list_redirection.add_argument('--owner',          default='%')

    cmd_list_redirection.add_argument('--long', action='store_true', help='List details')

def list_alias(args, conn):
    cur = conn.cursor()

    select = ['address', 'destination']

    if args.long:
        select += ['service_entity_name', 'backend_status']

    cur.execute("""
     SELECT 
       """ + ', '.join(select) + """
     FROM (
      SELECT 
       localpart || '@' || domain AS address,
       mailbox_localpart || '@' || mailbox_domain AS destination,
       *
      FROM email.alias
     ) AS x
     WHERE
      COALESCE(backend_status, '') LIKE %(backend_status)s
      AND address LIKE %(address)s
      AND destination LIKE %(destination)s
     ORDER BY address
    """, vars(args))
    canini.utils.printCurAsTable(cur)

def list_mailbox(args, conn):
    cur = conn.cursor()

    select = ['address', 'owner']

    if args.long:
        select += ['service_entity_name', 'backend_status']

    cur.execute("""
     SELECT 
       """ + ', '.join(select) + """
     FROM (
      SELECT 
       localpart || '@' || domain AS address,
       *
      FROM email.mailbox
     ) AS x
     WHERE
      COALESCE(backend_status, '') LIKE %(backend_status)s
      AND address LIKE %(address)s
      AND owner LIKE %(owner)s
     ORDER BY address
    """, vars(args))
    canini.utils.printCurAsTable(cur)

def list_redirection(args, conn):
    cur = conn.cursor()

    select = ['address', 'destination', 'owner']

    if args.long:
        select += ['service_entity_name', 'backend_status']

    cur.execute("""
     SELECT 
       """ + ', '.join(select) + """
     FROM (
      SELECT 
       localpart || '@' || domain AS address,
       *
      FROM email.redirection
     ) AS x
     WHERE
      COALESCE(backend_status, '') LIKE %(backend_status)s
      AND address LIKE %(address)s
      AND destination LIKE %(destination)s
      AND owner LIKE %(owner)s
     ORDER BY address
    """, vars(args))
    canini.utils.printCurAsTable(cur)


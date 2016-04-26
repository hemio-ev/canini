import canini.utils

def add_objects_to_chown(subparsers):
    parser = subparsers.add_parser('dns.registered', help='Registered Domain')
    parser.add_argument('domain', metavar='<domain>')
    canini.chown.complete(parser, 'dns.registered', {"domain": 'domain'})

def add_commands_to_parser(subparsers):
    cmd = subparsers.add_parser('dns', help='DNS and Registered Domains').add_subparsers()
    
    # list-registered
    cmd_list_registered = cmd.add_parser('list-registered', help='Lists registered domains')
    cmd_list_registered.set_defaults(func=list_registered)

    cmd_list_registered.add_argument('--backend-status', default='%')
    cmd_list_registered.add_argument('--domain',         default='%')
    cmd_list_registered.add_argument('--owner',          default='%')
    cmd_list_registered.add_argument('--public-suffix',  default='%')
    cmd_list_registered.add_argument('--subservice',     default='%')

    cmd_list_registered.add_argument('--long', action='store_true', help='List details')

def list_registered(args, conn):
    cur = conn.cursor()

    select = ['domain', 'owner', 'backend_status']

    if args.long:
        select += ['public_suffix', 'subservice', 'service_entity_name']

    cur.execute("""
     SELECT
      """ + ', '.join(select) + """
     FROM dns.registered
     WHERE
      COALESCE(backend_status, '') LIKE %(backend_status)s
      AND domain LIKE %(domain)s
      AND owner LIKE %(owner)s
      AND public_suffix LIKE %(public_suffix)s
      AND subservice LIKE %(subservice)s
     ORDER BY domain
    """, vars(args))
    canini.utils.printCurAsTable(cur)


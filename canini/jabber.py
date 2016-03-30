import canini

def add_objects_to_chown(subparsers):
    parser = subparsers.add_parser('jabber.account', help='Jabber account')
    parser.add_argument('address', metavar='<address>')
    canini.chown.complete(parser, 'jabber.account', {"node || '@' || domain": 'address'})


import canini

def add_objects_to_chown(subparsers):
    parser = subparsers.add_parser('dns.registered', help='Registered Domain')
    parser.add_argument('domain', metavar='<domain>')
    canini.chown.complete(parser, 'dns.registered', {"domain": 'domain'})


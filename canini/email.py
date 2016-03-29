import canini

def add_objects_to_chown(subparsers):
    def args(name):
        x = subparsers.add_parser('email.' + name, help='Email ' + name)
        x.add_argument('localpart', metavar='<localpart>')
        x.add_argument('domain', metavar='<domain>')
        canini.chown.complete(x, 'email.' + name, {'localpart': 'localpart', 'domain':'domain'})

    args("list")
    args("mailbox")
    args("redirection")


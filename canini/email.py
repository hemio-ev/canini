import canini

def add_objects_to_chown(subparsers):
    def args(name):
        x = subparsers.add_parser('email.' + name, help='Email ' + name)
        x.add_argument('address', metavar='<address>')
        canini.chown.complete(x, 'email.' + name, {"localpart || '@' || domain": 'address'})

    args("list")
    args("mailbox")
    args("redirection")


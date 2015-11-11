import canini.user
import argcomplete, argparse

def parser():
    parser = argparse.ArgumentParser(prog='canini')
    
    subparsers = parser.add_subparsers()
    
    # command "user"
    cmd_user = subparsers.add_parser('user', help='User account management')
    cmd_user.set_defaults(func=canini.user.load)
    
    cmd_user_action = cmd_user.add_mutually_exclusive_group(required=True)
    
    cmd_user_action.add_argument('-l', '--list', nargs='?', const='%', metavar='user_pattern', help='List all users')
    cmd_user_action.add_argument('--appoint-deputy', nargs=2, metavar=('<deputy>', '<represented>'), help='Appoints <deputy> as deputy for <represented>')
    cmd_user_action.add_argument('--revoke-deputy', nargs=2, metavar=('<deputy>', '<represented>'), help='Revokes <deputy> as deputy for <represented>')
    
    argcomplete.autocomplete(parser)
    
    return parser

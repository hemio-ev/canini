import canini.user
import argcomplete, argparse

def parser():
    parser = argparse.ArgumentParser(prog='canini')
    
    subparsers = parser.add_subparsers()

    canini.user.add_commands_to_parser(subparsers)

    argcomplete.autocomplete(parser)
    
    return parser


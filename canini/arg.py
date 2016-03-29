import canini.user
import canini.coupon
import canini.chown
import canini.email
import argcomplete, argparse

mods = [ canini.email, canini.user, canini.coupon ]

def parser():
    parser = argparse.ArgumentParser(prog='canini')
    
    subparsers = parser.add_subparsers()

    for mod in mods:
        try:
            mod.add_commands_to_parser(subparsers)
        except AttributeError:
            pass

    chown = canini.chown.add_command(subparsers)

    for mod in mods:
        try:
            mod.add_objects_to_chown(chown)
        except AttributeError:
            pass

    argcomplete.autocomplete(parser)
    
    return parser


import canini.chown
import argcomplete, argparse
import importlib

def parser(modules):
    mods = [ importlib.import_module(name) for name in modules ]

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


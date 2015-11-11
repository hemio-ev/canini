from prettytable import (PrettyTable, ALL, PLAIN_COLUMNS)

def printTable(data):
    if not data:
        print(PrettyTable(["EMPTY"]))
        return

    x = PrettyTable(data[0].keys())

    x.align = "l"
    x.vertical_char = "│"
    x.horizontal_char = "─"
    x.junction_char = "┼"
    x.hrules = ALL

    for row in data:
        values = map(varToChar, row.values())
        x.add_row(list(values))
    print(x)

def printCurAsTable(cur):
    printTable(list(map(lambda x: x._asdict(), cur.fetchall())))

def varToChar(var):
    if var is None:
        return "␀"

    if isinstance(var, list):
        return '\n'.join(var)

    if isinstance(var, bool):
        return "☒" if var else "☐"

    return var


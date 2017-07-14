from prettytable import (PrettyTable, ALL, PLAIN_COLUMNS)
import json

def setOption(d, string, value):
    keys = string.split('.')
    x = {}
    cur = d
    for k in keys[:-1]:
        new = {}
        if k not in cur:
            cur.update({k: new})
            cur = new
        else:
            cur = cur[k]
    cur.update({keys[-1]: value})

def deleteOption(d, string):
    keys = string.split('.')
    cur = d
    for k in keys[:-1]:
        cur = cur[k]
    del cur[keys[-1]]

def printTable(data, ignore=[]):
    if not data:
        print(PrettyTable(["EMPTY"]))
        return

    rawdata = list(map(lambda x: {k: x[k] for k in x if k not in ignore}, data))

    x = PrettyTable(rawdata[0].keys())

    x.align = "l"
    x.vertical_char = "│"
    x.horizontal_char = "─"
    x.junction_char = "┼"
    x.hrules = ALL

    for row in rawdata:
        values = map(varToChar, row.values())
        x.add_row(list(values))
    print(x)

def printCurAsTable(cur, ignore=[]):
    printTable(getDict(cur), ignore=ignore)

def getDict(cur):
    return list(map(lambda x: x._asdict(), cur.fetchall()))

def varToChar(var):
    if var is None:
        return "␀"

    if isinstance(var, list):
        return '\n'.join(var)

    if isinstance(var, bool):
        return "☒" if var else "☐"

    return var


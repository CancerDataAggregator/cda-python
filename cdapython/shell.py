"""
This module is made as a repl for Q 
"""
from typing import Any, Dict, Union

import re

from rich import print
from rich.console import Console

from cdapython import columns, unique_terms
from cdapython.Q import Q

try:
    import readline  # pylint: disable=W0611
except ImportError:
    raise ImportError()

from cdapython import set_host_url, get_host_url

"""[summary]
    add's history to shell in current session
"""
new = True
console = Console(record=True)
setServer = "http://localhost:8080/"
system_default_url = get_host_url()
set_host_url(setServer)
setTable = None
setFormat = 'dataframe'
setDataFrame = True
setJSON = False
setList = False




def help() -> None:
    print("ran shell.py help")
    print(
        """
        Welcome to Q shell's help utility
        Query Example
            sex = "Enter Value"
        Functions
            help -- print this help dialog
            columns -- print all available column headers
            unique_terms -- submit a column header without quotes, will return all unique values found in that column
            set_format -- change current output format to one of dataframe, list, or json. default is dataframe
            get_format -- report current output format setting (dataframe, json, or list)
            set_server -- submit a server address without quotes, sets the server
            get_server -- report current server address
            set_bq_table -- submit a Big Query table name without quotes, sets the Big Query table
            get_bq_table -- report current tablename
            reset -- resets server and bqtable to their default values
            clear -- clear the terminal window
            exit -- leave the Q shell
        \n
        """
    )


while True:
    if new is True:
        help()
        print(
            f"""Q {Q.get_version()} Type "help()" for more information."""
        )
        new = False
    text: str = input(">>> ")
    if text == "reset":
        setTable = None
        set_host_url(system_default_url)
        continue
   # if text == "set_format":
    if re.search(r'set_format', text) is not None:
        text = re.sub(r'set_format\s+',r'', text)
        #setFormat = console.input("Enter format ")
        if text in ["dataframe", "json", "list"]:
            setFormat = text
        else:
            print(f"Unrecognized format. Current format is {setFormat}")
        continue
    if text == "help":
        help()
        continue
    if text == "set_server":
        setServer = console.input("Enter your server ")
        set_host_url(setServer)
        continue
    if text == "set_bq_table":
        setTable = console.input("Enter your table ")
    if text == "clear":
        print("\n" * 100)
        continue
    if text == "get_format":
        print(setFormat)
        continue
    if text == "get_server":
        print(setServer)
        continue
    if text == "get_bq_table":
        print(setTable)
        continue
    if text == "exit":
        break
    if text == "columns":
        if setFormat == "dataframe":
            print(columns().df_to_table())
        elif setFormat == "json":
            columns().pretty_print()
        elif setFormat == "list":
            print(columns().to_list())
        else:
            print("nachos")
        continue
    if text == "unique_terms":
        uniquevalue = console.input("Enter term ")
        if setFormat == "dataframe":
            print(unique_terms(uniquevalue).df_to_table())
        elif setFormat == "json":
            unique_terms(uniquevalue).pretty_print()
        elif setFormat == "list":
            print(unique_terms(uniquevalue).to_list())
        else:
            print("nachos")
        continue
    else:
        try:
            result: Q = Q(text)
            if setFormat == "dataframe":
               if setTable is not None:
                   print(result.run(table=setTable).df_to_table())
               else:
                    print(result.run().df_to_table())
            elif setFormat == "json":
                if setTable is not None:
                    result.run(table=setTable).pretty_print()
                else:
                    result.run().pretty_print()
            elif setFormat == "list":
                if setTable is not None:
                    print(result.run(table=setTable).to_list())
                else:
                    print(result.run().to_list())                        
            else:
                print(type(result), result)
            continue 
        except Exception as e:
            print(e)
            print(type(e))
            continue
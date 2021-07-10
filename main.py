#!/usr/bin/env python3
# coding: utf-8

# Copyright 2021 by BurnoutDV, <burnoutdv@gmail.com>
#
# This file is part of getterGen.
#
# getterGen is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# getterGen is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with getterGen.  If not, see <http://www.gnu.org/licenses/>.
#
# @license GPL-3.0-only <https://www.gnu.org/licenses/gpl-3.0.en.html>

import sys
import re

try:
    import pyperclip # i really really wanted to do this without any dependencies..but no, of course clipboards have to be complicated
except ModuleNotFoundError:
    print("pyperclip not found, required for clipboard operations", file=sys.stderr)
    print("using emergency mode, instead of clipboard, 'clipboard.txt' in root folder will be used")
    # i am not sure, this is kinda dirty

    class pyperclip():
        @staticmethod
        def copy(text: str):
            with open("clipboard.txt", "w") as clip:
                clip.write(text)

# ? Idea: Three Modes
# ? active mode, input name and filetype, one each per line
# ? gui mode, some simple QT5 interface
# ? commandline mode, repeatable args main.py -p name str -p friend str -p id int


def generate_code(prop: dict, checking_mode=False):
    """
    Just generates the code by inserting it at the right place, not very fancy, make changes here if you
    need something different
    :param dict prop: a flat key-value dictionary of name and file type
    :param bool checking_mode: changes the form of the resulting code, adds an "isinstance" check
    :return: the complete generated code
    """
    cliptext = ""
    for key in prop:
        name = key
        file_type = prop[key]
        if not checking_mode:
            cliptext += f"""
        @property
        def {name}(self):
            return self._{name}

        @{name}.setter
        def {name}(self, {name}: {file_type}):
            self._{name} = {name}       
    """
        else:
            cliptext += f"""
    @property
    def {name}(self):
        return self._{name}

    @{name}.setter
    def {name}(self, {name}: {file_type}):
        if isinstance({name}, {file_type}):
            self._{name} = {name}       
"""
    return cliptext


def whole_purpose(prop: dict, checking_mode=False):
    """
    Attempts to copy text to clipboard, if pyperclip fails it offers to copy to console instead
    :param dict prop: dictionary of properties
    :param bool checking_mode: whether check mode is activated or not
    :return: True on success, false if fallback had to be used
    """
    cliptext = generate_code(prop, checking_mode)
    try:
        pyperclip.copy(cliptext)
        print(f"{len(prop)} getter & setter pairs where copied to clipboard")
        return True
    except pyperclip.PyperclipException:
        print("Couldn't copy to clipboard, try installing xsel, xclip, PyQT4(pip) or gtk(pip)")
        decision = input("output to console instead? y/N")
        if decision[:1].lower() == "y":
            print(cliptext)
        return False


def check_property_name(name: str):
    """
    Checks if the given string is a viable name for a property
    :param str name: any one name
    :return: True if the given name is indeed possible, false if not
    """
    keywords = ('and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'False',
                'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'None', 'nonlocal', 'not',
                'or', 'pass', 'raise', 'return', 'True', 'try', 'while', 'with', 'yield')
    if name in keywords:
        return False
    if not re.match(r"^[a-zA-Z_]{1}[a-zA-Z0-9_]*$", name):
        return False
    return True

if __name__ == "__main__":
    print("Active input mode, type your first line")
    print("{property name} {datatype}")
    print("empty line will finish process and copy content to clipboard")
    input_str = "init"
    pairs = {}
    check_mode = False
    while len(input_str) > 0:
        input_str = input("new:")
        parts = input_str.strip().split(" ")
        if not input_str or input_str == "/f":
            break
        elif input_str == "/q":
            print("Aborting input, no clipboard copied")
            exit(0)
        elif input_str == "/c":  # check mode
            if not check_mode:
                print("Info: check mode activate")
                check_mode = True
            else:
                print("Info: check mode deactivated")
                check_mode = False
            continue
        elif input_str == "/s":
            if len(pairs) > 0:
                whole_purpose(pairs, check_mode)
            else:
                print("Info: property repository empty")
            continue
        elif len(parts) != 2:
            print("Err: Cannot create property")
            continue
        if parts[0] in pairs:
            print(f"Info: overwrote {parts[0]}")
        if parts[0] == "/del":  # some rudimentary controls
            if pairs.pop(parts[1], None):
                print(f"Info: deleted {parts[1]}")
        else:
            if check_property_name(parts[0]):
                pairs[parts[0]] = parts[1]
            else:
                print(f"Err: {parts[0]} is not a valid function name")

    if len(pairs) > 0:
        whole_purpose(pairs, check_mode)
    else:
        print(f"No properties found, nothing copied")
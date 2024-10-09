""" G3 - Plasma Devs
Utilities - Path Finder
    Provides a basic utility to locate the absolute path to the project's root folder.


author: figueroa_90894@students.pupr.edu
status: DONE

Methods:
    find_src() - returns absolute path to the /plasmetry/src folder.

"""

import os

def find_src(target:str|list=['plasmetry', 'src']):
    """Return the absolute path to the directory specified by the target argument.
    Target may take a list, where each element consists the parent folder followed by subfolders.
    In such case it will return the absolute path to lowest folder.

    Assumes this file will be placed inside the targets hierarchy.

    """
    # validate argument types
    if isinstance(target, str):
        target = [target]
    elif not isinstance(target, list):
        raise TypeError(f"Argument must be str or list! Given {type(target)}")
    
    # os delimeters
    win_delimeter, rpi_delimeter = "\\", "/"

    # get path to current file
    file_path = os.path.dirname(__file__)

    # select path delimeter
    if win_delimeter in file_path: delimeter = win_delimeter
    elif rpi_delimeter in file_path: delimeter = rpi_delimeter
    
    # divide path string into list of directories
    split = file_path.split(delimeter)

    # 
    while len(split) > 0:
        found = True
        for i in range(len(target)):
            found = split[-1-i] == target[-1-i] and found
        if found:
            break
        split.pop()
    if not found:
        raise RuntimeError("Could not locate source path.")
    return delimeter.join(split)

def resolve_path(rel_path, root=['plasmetry', 'src']):
    """<...>"""
    src_path = find_src(target=root)
    abs_path = os.path.abspath(f"{src_path}/{rel_path}")
    return abs_path


#! /usr/local/bin/python3.8

"""This module provides functions for managing links on my website. 

Motivation:
= = = = = = = = = = = = 
I'm in the early stages of writing my blog in pure HTML and CSS. So, naturally, I'm
constantly restructuring the filesystem, and constantly renaming pages and assets. As
a result, I have to manually update links and references to assets. This process gets
tedious, and is becoming very time consuming - even though I've only written a few pages!

To eliminate this unnecessary labor, I've decided to automate the process of resolving
links and references to pages and assets. The next section describes this problem in context, and
also details my solution to the problem.


How the manager.py works:
= = = = = = = = = = = = 
manager.py does the following:
    1. Scans the directory, and searches for links that refer to missing or non-existent referrants
    2. Reports the results of the search, and creates a "database" of links and their associated referrents

1. Scanning 
- - - - - - - - - -

2. Reporting
- - - - - - - - - -


Glossary
= = = = = = = = = = = = 
* Referrant: A page, a stylesheet, or an asset that, presumably, exists in the repository.
* Page: An HTML file; (as a parameter, a filename or path)
"""

import os, os.path
import pathlib
import sys

from pprint import pprint

from bs4 import BeautifulSoup


def traverse_dir(dir: str, depth: int = 1):
    """Traverses the contents of the directory `dir`, and returns the names of structures 
    in a list.

    Positional args:
        - dir <str>: The directory to traverse. If `dir` doesn't exist in working directory, 
            the programs raises a `FileExistsError`.
        - depth <int>: The depth of the traversal

    Returns a list of files and directories.

    TODO: Add argument for filtering for specific filetype.
    """

    if not os.path.exists(dir):
        raise FileExistsError("'%s does not exist" % dir)

    # If we're reached the depth limit of the traversal, return; don't do any more traversal
    if depth == 0:
        return []

    dir = pathlib.Path(dir)
    filenames = []  # TODO: Should this be named `filenames` or `paths` instead?
    for file in dir.iterdir():
        if file.is_file():
            filenames.append(file.name)
        else:
            offset = len(filenames)
            subdir_filenames = traverse_dir(file, depth - 1)
            if len(subdir_filenames) > 0:  # the subdirectory is empty or we reached the depth limit
                for sub_index in range(0, len(subdir_filenames)):
                    subdir_filenames[sub_index] = file.name + \
                        '/' + subdir_filenames[sub_index]
                filenames += subdir_filenames
            else:
                filenames += [file.name + '/']

    return filenames


def get_links(page: str):
    """
    Returns all the links from a webpage.

    args:
        page <str>: The path to an html page.
    """
    with open(page) as f:
        page = BeautifulSoup(f, "html.parser")
        anchor_tag = "a"
        anchors = page.find_all(anchor_tag)
        links = [anchor.get("href") for anchor in anchors]

        return links


def get_broken_links(page: str):
    """
    Returns a list that contains all the broken links in `page`.

    args:
        page <str>: The path to an html page.
    TODO: Should the returned list also contain broken jump links?
    FIXME: (1) The search for broken links and references uses os.path.exist to search for pages and assets. Because
    manager.py runs in the root directory, and all the links it processes are relative, it ends up trying to search
    for links relative to the root directory. For example, `blog/index.html` has an anchor to `../index.html`. The method
    would default to marking this as a broken link because it would search for the referrant relative to the working directory instead
    of relative to `blog/`. 
    """

    os.scandir()


    links = get_links(page)
    broken_links = []
    for link in links:
        # FIXME (1)
        # if not os.path.exists(link):
        #     broken_links += [link]

    return broken_links


if __name__ == "__main__":
    root = pathlib.Path(".")

    depth = 1
    if len(sys.argv) > 1:
        depth = int(sys.argv[1])

    # Get the HTML files
    files = traverse_dir(root, depth=depth)

    # Iterate over the HTML, and get the broken links
    html_files = list(filter(lambda filename: ".html" in filename, files))

    # Get the broken links in the file
    broken_links = dict()
    for file in html_files:
        print(file)

        broken_links[file] = get_broken_links(file)
    pprint(broken_links)

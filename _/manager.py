#! /usr/local/bin/python3.8
import os
import os.path
import pathlib
import sys
from pprint import pprint
from bs4 import BeautifulSoup

def get_paths(dir: str, depth: int = 1, exclude=[".git", ".gitignore", "node_modules"]):
    """Traverses the contents of the directory `dir`, and returns the paths of each file system 
    object relative to `dir`. 

    Positional args:
        - dir <str>: The directory to traverse. If `dir` doesn't exist in working directory, 
            the programs raises a `FileExistsError`.
        - depth <int>: The depth of the traversal.
        - exclude <list>: A list of files and directories to exclude from the returned list. By
        default, ignores `.git/`, `.gitignore`, and `node_modules/`.

    Returns a list of files and directories.

    FIXME: Update the name of the function to `get_paths` so it reflects its actual functionality
    TODO: Update `exclude` parameter so that the list items can be regex (or globs?).
    TODO: Add `excludedefault` to optinally exclude the files that are excluded by default (mouthful, lol)
    """

    if not os.path.exists(dir):
        raise FileExistsError("'%s does not exist" % dir)

    # If we've reached the depth limit of the traversal, return; don't traverse anymore
    if depth == 0:
        return []

    dir = pathlib.Path(dir)
    paths = []  # TODO: Should this be named `filenames` or `paths` instead?
    for file in dir.iterdir():
        # Ignore that paths listed in `exclude`.
        if file.name in exclude:
            continue
        
        if file.is_file():
            paths.append(file.name)
        else:
            subdir_paths = get_paths(file, depth - 1)
            # If the subdirectory is empty or we reached the depth limit
            if len(subdir_paths) == 0:
                paths += [file.name + '/']

            # Concatenate the directory path to the returned list of subdirectories
            else:
                for sub_index in range(0, len(subdir_paths)):
                    subdir_paths[sub_index] = file.name + \
                        '/' + subdir_paths[sub_index]
                paths += subdir_paths

    return paths


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
        ...

    return broken_links


if __name__ == "__main__":
    root = pathlib.Path(".")

    depth = 1
    if len(sys.argv) > 1:
        depth = int(sys.argv[1])

    # Get the HTML files
    files = get_paths(root, depth=depth)

    # Iterate over the HTML, and get the broken links
    html_files = list(filter(lambda filename: ".html" in filename, files))

    # Get the broken links in the file
    broken_links = dict()
    for file in html_files:
        print(file)

        broken_links[file] = get_broken_links(file)
    pprint(broken_links)

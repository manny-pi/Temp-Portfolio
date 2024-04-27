#! /usr/local/bin/python3.8
import os
import os.path
import pathlib
import argparse
import sys
from pprint import pprint
from bs4 import BeautifulSoup


def get_paths(dir: str, depth: int = 1, exclude=[".git", ".gitignore", "node_modules"]):
    """Traverses the directory `dir`, and returns a list of paths relative to `dir`. 

    Positional args:
        - dir <str>: The directory to traverse. If `dir` doesn't exist in working directory, 
            the programs raises a `FileExistsError`.
        - depth <int>: The depth of the traversal; -1 to traverse all subdirectories.
        - exclude <list>: A list of files and directories to exclude from the returned list. By
        default, ignores `.git/`, `.gitignore`, and `node_modules/`.

    Returns a list of files and directories.

    TODO: Update `exclude` parameter so that the list items can be regex (or globs?).
    TODO: Add `excludedefault` to optionally exclude the files that are excluded by default (mouthful, lol)
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
    Returns an array of links in a webpage.

    Positional args:
        page <str>: The path to an HTML page that contains anchors.
    """
    with open(page) as f:
        page = BeautifulSoup(f, "html.parser")
        anchor_tag = "a"
        anchors = page.find_all(anchor_tag)
        links = [anchor.get("href") for anchor in anchors]

        return links


def get_broken_links(path: str):
    """
    Returns a list that contains all the broken links in `page`.

    args:
        path <str>: The path to an html page.
    TODO: Should the returned list also contain broken jump links?
    TODO: (1) Turn this into a logging detail.
    """
    links = get_links(path)
    broken_links = []
    for link in links:
        dirname = os.path.dirname(path)
        basename = os.path.basename(path)
        parent = link.count("..")
        truncated_link = link.split('/')[parent:]
        # print(path, ' <', dirname, '> ', link,
        #       ' ', truncated_link, parent)  # (1)

        if not parent:
            if dirname != "": 
                resolved_path = '/'.join([dirname, link])
            else: 
                resolved_path = link
            if not os.path.exists(resolved_path):
                broken_links += [link]
        else:
            # split the directory into its components
            dirname = dirname.split('/')
            # Create a search path
            try:
                # Get the parent directory of the referrant
                search_path = dirname[:-(parent + 1)]
            except IndexError:
                # If the search goes out of bounds, the search directory is the root of the project
                search_path = []

            resource_path = '/'.join(search_path + truncated_link)
            if not os.path.exists(resource_path):
                broken_links += [link]
    return broken_links

def scan_directory(path: str):
    """Scans a directory for pages that contain broken links.
    
    Positional args:
        path <str>: A path to the HTML page. 

    TODO: The funcion relies on get_paths(); Upd the function so that it knows how depth
    to traverse. {Actually, is the `depth` parameter even necessary in that function?} 
    """
    paths = get_paths(path,)

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
        broken_links[file] = get_broken_links(file)
    pprint(broken_links)

# manager.py

This module provides functions for managing links on my website.

*Motivation*

I'm in the early stages of writing my blog in pure HTML and CSS. So, naturally, I'm
constantly restructuring the filesystem, and constantly renaming pages and assets. As
a result, I have to manually update links and references to assets. This process gets
tedious, and is becoming very time consuming - even though I've only written a few pages!
.

To eliminate this unnecessary labor, I've decided to automate the process of resolving
links and references to pages and assets. The next section describes this problem in context, and
also details my solution to the problem.

## How the manager.py works

manager.py does the following:

1. *Scans* the directory, and searches for links that refer to missing or non-existent referrants
2. *Reports* the results of the search, and creates a "database" of links and their associated referrents

### 1. Scanning

### 2. Reporting

## Usage

I wholly believe in the philosophy that "just because you 'can' do something doesn't mean you should." I haven't
tested every conceivable edge case of this program, so the curious among you will likely try to do things with
this program that, at the time of writing, it was designed to do, or you simply use it in the wrong context. So, to
help you avoid using this program wrongly, this sections discusses:

1. What you should be doing with this program and how to do it, and
2. How NOT to use this program :)

## Glossary

* File:
* Directory:
* Subdirectory:
* Path:
* Filename:
* Pathname:
* Basename:
* Tree:
* Page: An HTML file; (as a parameter, a filename or path)
* File system object: A generic name for files, directories, symbolic links, e.t.c.
* Referrant: A page, a stylesheet, or an asset that - presumably exists in the repository, and - is referred
    to by a .html page in the directory.
* Broken link: Any link (the `href` attribute of the `<a>` element in an HTML page) that points to a missing
    referrant.

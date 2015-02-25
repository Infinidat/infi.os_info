Overview
========
This module provides functions to get the name of the current operating system and platform.

Usage
-----
After installing this script, either run `infi-uname` to print the detected os/platform name, or
use

    from infi.os_info import get_platform_string
    print get_platform_string()

Examples for returned strings:

    linux-ubuntu-trusty-x86
    solaris-11-x64

etc.

Checking out the code
=====================
Run the following commands:

    easy_install -U infi.projector
    projector devenv build


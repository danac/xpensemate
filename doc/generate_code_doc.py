#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2014 Dana Christen
#
# This file is part of XpenseMate, a tool for managing shared expenses and
# hosted at https://github.com/danac/xpensemate.
#
# XpenseMate is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import os
import pprint

SOURCE_ROOT = os.path.join(os.path.dirname(__file__), '..', 'xpensemate')
DOC_ROOT = os.path.join(os.path.dirname(__file__), 'backend', 'code_doc')
#DOC_ROOT = os.path.join('/tmp', 'backend')

SPHINX_FILE_PATTERN = """
{}
=================================================

.. toctree::
    :maxdepth: 10

    {}


.. automodule:: {}
    :members:
    :undoc-members:
    :show-inheritance:

"""

def find_source_files():
    hierarchy = dict()
    
    for root, dirs, files in os.walk(SOURCE_ROOT):
        if "__pycache__" in root:
            continue

        folder = os.path.relpath(root, os.path.join(SOURCE_ROOT, '..'))
        package = folder.replace(os.sep, '.')
        modules = [f.split('.')[0] for f in files if f[-2:] == 'py' and "__" not in f]
        
        if "__init__.py" not in files:
            continue
        
        hierarchy[package] = modules
    return hierarchy


def create_rst_files():
    
    package_list = find_source_files()
    file_list = list()
    
    for package in package_list:
        file_list.append(package + ".rst")
        for sub_module in package_list[package]:
            file_list.append(".".join([package, sub_module]) + ".rst")
    
    sub_package_list = dict()
    
    for f in file_list:
        package_name = f[:-4]
        sub_package_list[package_name] = list()
        for f2 in file_list:
            if not package_name in f2:
                continue
            sub_package_name = f2.replace(package_name, "")[:-4]
            if len(sub_package_name.split(".")) == 2:
                sub_package_list[package_name].append(f2[:-4])
            
    for f in file_list:
        with open(os.path.join(DOC_ROOT, f), 'w') as f_hdl:
            package_name = f[:-4]
            sub_packages = '\n    '.join(sub_package_list[package_name])
            f_hdl.write(SPHINX_FILE_PATTERN.format(package_name, sub_packages, package_name))
    
if __name__ == "__main__":
    create_rst_files()

        

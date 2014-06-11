#!/usr/bin/python

# Copyright 2014 Florian Bruhin (The Compiler) <me@the-compiler.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import shutil
import os.path
import os
import tarfile

import requests


MAINTAINER="The-Compiler"
DOMAIN="https://aur.archlinux.org/"


def download_and_extract(url, dirname):
    basename = os.path.basename(url)
    req = requests.get(url, stream=True)
    filename = os.path.join(dirname, basename)
    with open(filename, 'wb') as f:
        for chunk in req.iter_content(1024):
            f.write(chunk)
    tar = tarfile.open(filename)
    tar.extractall()
    os.remove(filename)


def get_all_packages():
    payload = {'type': 'msearch', 'arg': MAINTAINER}
    json = requests.get(DOMAIN + 'rpc.php', params=payload).json()
    names = []
    for result in json['results']:
        name = result['Name']
        print("Downloading/extracting {}...".format(name))
        names.append(name)
        url = DOMAIN + result['URLPath']
        if os.path.exists(name):
            shutil.rmtree(name)
        os.mkdir(name)
        download_and_extract(url, name)
    return names


def print_lint(names):
    whitelist = [os.path.basename(sys.argv[0]), '.git']
    for d in os.listdir(os.getcwd()):
        if d not in names and d not in whitelist:
            print("Unknown file/directory {}!".format(d))


if __name__ == '__main__':
    names = get_all_packages()
    print()
    print_lint(names)

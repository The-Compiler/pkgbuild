#!/usr/bin/python

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

#!/usr/bin/python3
"""A fab file for webserver deployment"""
from fabric.api import *
from datetime import datetime
import os


def do_pack():
    """ generates a .tgz archive from the contents of the web_static folder"""
    now = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    name = "versions/web_static_{}.tgz".format(now)
    if not os.path.isdir("versions"):
        local("mkdir versions")
    with settings(warn_only=True):
        res = local("tar -cvzf {} web_static 2>&1".format(name), capture=True)
    if res.failed:
        return None
    return name

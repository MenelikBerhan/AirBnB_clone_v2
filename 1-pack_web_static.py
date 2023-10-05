#!/usr/bin/python3
"""A fab file for webserver deployment"""
from fabric.api import *
from datetime import datetime
import os


def do_pack():
    """ generates a .tgz archive from the contents of the web_static folder"""
    now = datetime.now()
    name = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)

    if not os.path.isdir("versions"):
        local("mkdir versions")
    with settings(warn_only=True):
        err = local("tar -cvzf {} web_static 2>&1".format(name), capture=True)
    if 'failure' not in err:
        return name

    return None

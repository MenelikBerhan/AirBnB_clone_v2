#!/usr/bin/python3
"""A fab file for webserver deployment"""
from fabric.api import *
import os

env.hosts = ['18.206.208.78', '54.162.233.113']
env.user = 'ubuntu'
# env.use_ssh_config = True


def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        put(archive_path, "/tmp/")
        archive = archive_path.split("/")[1]
        file = archive.split(".")[0]
        release = "/data/web_static/releases/"
        folder = "/data/web_static/releases/{}".format(file)
        run("mkdir -p {}".format(folder))
        run(" tar -xzf /tmp/{} -C {}".format(archive, folder))
        run("rm /tmp/{}".format(archive))
        run("mv {}{}/web_static/* {}{}/".format(release, file, release, file))
        run("rm -rf /data/web_static/releases/{}/web_static".format(file))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder))
        print("New version deployed!")
        return True
    except Exception:
        return False

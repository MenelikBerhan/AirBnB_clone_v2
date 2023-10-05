#!/usr/bin/python3
"""Creates and distributes an archive to my web servers"""
from datetime import datetime
from fabric.api import *
import os
# env.use_ssh_config = True
env.hosts = ['18.206.208.78', '54.162.233.113']
env.user = 'ubuntu'


@runs_once
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


def do_deploy(archive_path):
    """distributes an archive to my web servers"""
    if not os.path.exists(archive_path):
        return False

    with settings(warn_only=True):
        if put(archive_path, "/tmp/").failed:
            return False
        archive_name = archive_path.split("/")[-1]
        extract_path = "/data/web_static/releases/"\
            + archive_name.split(".")[0] + "/"
        # create extraction folder
        if run("mkdir -p {}".format(extract_path)).failed:
            return False
        # extract to extract_path
        if run("tar -xzf /tmp/{} -C {}"
                .format(archive_name, extract_path)).failed:
            # clean up incase of extraction failure
            run("rm -rf /tmp/{}".format(archive_name))
            run("rm -rf {}".format(extract_path))
            return False
        # remvoe archive
        if run("rm -rf /tmp/{}".format(archive_name)).failed:
            return False
        # copy content from new web_static version to parent folder
        # if there are files in parent update if file is newer
        if run("cp -uR {}web_static/* {}"
                .format(extract_path, extract_path)).failed:
            return False
        # remove empty folder web_static
        if run("rm -rf {}web_static".format(extract_path)).failed:
            return False
        # remove current symbolic link
        if run("rm -rf /data/web_static/current").failed:
            return False
        # create a new symbolic link of the new version inplace of deleted
        if run("ln -fs {} /data/web_static/current"
                .format(extract_path)).failed:
            return False
    print("New version deployed!")
    return True


def deploy():
    """Deploys an archive to web servers after creating it"""
    arch_path = do_pack()
    if not arch_path:
        return False
    return do_deploy(arch_path)

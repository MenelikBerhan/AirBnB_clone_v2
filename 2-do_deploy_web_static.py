#!/usr/bin/python3
"""A fab file for webserver deployment"""
from fabric.api import *
import os

env.hosts = ['18.206.208.78', '54.162.233.113']
env.user = 'ubuntu'
# env.use_ssh_config = True


def do_deploy(archive_path):
    """distributes an archive to my web servers"""
    if not os.path.isfile(archive_path):
        return False

    with settings(warn_only=True):
        create_tmp = run('mkdir -p /tmp/')
        if create_tmp.failed:
            return False
        with cd('/tmp'):
            if put(archive_path, '/tmp/').failed:
                return False
            archive_name = archive_path.split('/')[-1]
            extract_path = '/data/web_static/releases/'\
                + archive_name.split('.')[0] + '/'
            # create extraction folder
            if run('mkdir -p {}'.format(extract_path)).failed:
                return False
            # extract to extract_path
            if run('tar -xzf /tmp/{} -C {}'
                   .format(archive_name, extract_path)).failed:
                return False
            # remvoe archive
            if run('rm /tmp/{}'.format(archive_name)).failed:
                return False
            # move content from web_static to parent folder
            if run('mv {}web_static/* {}'
                   .format(extract_path, extract_path)).failed:
                return False
            # remove empty folder web_static
            if run('rm -rf {}web_static'.format(extract_path)).failed:
                return False
            # remove current symbolic link
            if run('rm -rf /data/web_static/current').failed:
                return False
            # create a new symbolic link of new the version inplace of deleted
            if run('ln -s {} /data/web_static/current'
                   .format(extract_path)).failed:
                return False
    print('New version deployed!')
    return True

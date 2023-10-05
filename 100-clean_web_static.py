#!/usr/bin/python3
"""deletes out-of-date archives, using the function do_clean"""
from fabric.api import *
# env.use_ssh_config = True
env.hosts = ['18.206.208.78', '54.162.233.113']
env.user = 'ubuntu'


@runs_once
def do_local_clean(number=0):
    """deletes out-of-date local archives keeping
    'number' amount of recent archives"""
    number = int(number)
    to_keep = number + 1 if number == 0 else number
    with settings(warn_only=True):
        # get archive file names sorted by modification time (newest first)
        result = local('ls -t versions/web_static_* ', capture=True)
    if result.failed:
        print('No archives to delete!')
    else:
        archives = result.split('\n')
        if to_keep >= len(archives):
            print('No archives to delete!')
        else:
            for archive in archives[to_keep:]:
                with settings(warn_only=True):
                    res = local('rm {}'.format(archive), capture=True)
                if res.failed:
                    print('Failed to delete archive: {}'.format(archive))
                    continue


def do_clean(number=0):
    """deletes out-of-date archives keeping
    'number' amount of recent archives"""
    do_local_clean(number)
    number = int(number)
    to_keep = number + 1 if number == 0 else number
    remote_versions = '/data/web_static/releases/web_static_*'
    with settings(warn_only=True):
        # get archive directory names sorted by modification time
        result = run('ls -td {}'.format(remote_versions))
    if result.failed:
        print('No archive folders to delete!')
    else:
        archives = result.split('\n')
        if to_keep >= len(archives):
            print('No archive folders to delete!')
        else:
            for archive in archives[to_keep:]:
                with settings(warn_only=True):
                    res = run('rm -r {}'.format(archive.strip()))
                if res.failed:
                    print('Failed 2 delete archive folder: {}'.format(archive))
                    continue

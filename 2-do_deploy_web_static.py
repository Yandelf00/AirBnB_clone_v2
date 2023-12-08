#!/usr/bin/python3
"""fabric script that distributes archive to web"""

from fabric.api import put, run, env
import os

env.hosts = ['35.153.193.137', '18.207.235.211']


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        file = archive_path.split("/")[-1]
        ext_d = file.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {path}{ext_d}/')
        run('tar -xzf /tmp/{file} -C {path}{ext_d}/'.format(file, path, ext_d))
        run(f'rm /tmp/{file}')
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, ext_d))
        run(f'rm -rf {path}{ext_d}/web_static')
        run('rm -rf /data/web_static/current')
        run(f"ln -s {path}{ext_d}/ /data/web_static/current")
        return True
    except Exception as e:
        return False

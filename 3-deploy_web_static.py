#!/usr/bin/python3
"""fabric script that distributes
that creates and balbla your web servers"""

from fabric.api import put, run, env
from fabric.api import local
from datetime import datetime
import os

env.hosts = ['35.153.193.137', '18.207.235.211']


def do_pack():
    """
    Generate a .tgz archive from the contents of the web_static folder.

    Returns:
        str: Archive path if generated successfully, None otherwise.
    """
    src_dir = 'web_static'
    dest_dir = 'versions'
    if not os.path.exists(dest_dir):
        local(f'mkdir -p {dest_dir}')
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    output_name = f'web_static_{timestamp}.tgz'

    result = local(
        f"tar -cvzf {dest_dir}/{output_name} {src_dir}", capture=True)
    if result.succeeded:
        return os.path.join(dest_dir, output_name)
    else:
        return None


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


def deploy():
    """deploy function that does do_pack and do_deploy_web"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

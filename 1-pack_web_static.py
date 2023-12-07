#!/usr/bin/python3
"""script that generates a .tgz"""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generate a .tgz archive from the contents of the web_static folder.
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

#!/usr/bin/python3
"""Importing necessary modules"""

from datetime import datetime
from fabric.api import *
import os


env.hosts = ['54.162.95.185', '54.210.59.144']
env.user = "ubuntu"

def do_pack():
    """Generates a .tgz archive from the contents
    of the web_static folder of this repository.
    """

    date = datetime.now()
    now = date.strftime('%Y%m%d%H%M%S')

    local("mkdir -p versions")
    local("tar -czvf versions/web_static_{}.tgz web_static".format(now))


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    # In case the file at the path archive_path doesn't exist
    if not os.path.exists(archive_path):
        return False

    else:
        archive_filename = archive_path.split('/')[-1]
        archive_name_no_extension = archive_filename.split('.')[0]

        a_path = "/tmp/{}".format(archive_filename)
        put(archive_path, a_path)

        target_folder = "/data/web_static/releases/"

        full_path = target_folder + archive_name_no_extension + "/"

        run("mkdir -p {}".format(full_path))
        run("tar -xzf {} -C {}".format(a_path, full_path))
        run("rm {}".format(a_path))
        run("mv -f {}/web_static/* {}".format(full_path, full_path))
        run("rm -rf {}/web_static".format(full_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(full_path))
        return True

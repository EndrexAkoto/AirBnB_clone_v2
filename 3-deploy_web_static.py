#!/usr/bin/python3
"""
Fabric script create and distribute archive to web servers
"""

import os
from fabric.api import env, local, put, run
from datetime import datetime

env.hosts = ["34.207.121.49", "54.90.56.41"]


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                         dt.month,
                                                         dt.day,
                                                         dt.hour,
                                                         dt.minute,
                                                         dt.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file


def do_deploy(archive_path):
    """
    Deploy the archive to the web servers
    """
    if not archive_path:
        return False
    archive_name = os.path.basename(archive_path)
    remote_path = "/data/web_static/releases/{}/".format(archive_name[:-4])
    try:
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(remote_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_name, remote_path))
        run("rm /tmp/{}".format(archive_name))
        run("mv {}/web_static/* {}".format(remote_path, remote_path))
        run("rm -rf {}/web_static".format(remote_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(remote_path))
        return True
    except Exception:
        return False


def deploy():
    """
    Create and deploy the web_static archive
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)

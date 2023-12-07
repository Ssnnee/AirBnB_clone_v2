#!/usr/bin/python3
"""Fabric script that generates a .tgz archive"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """Compresses files in .tgz format"""

    local("mkdir -p versions")

    date = datetime.now()
    archive_name = "versions/web_static_{}.tgz".format(date)
    try:
        local("tar -cvzf {} web_static".format(archive_name))
        return archive_name
    except:
        return None


import os
import shutil
from collections import defaultdict

from loguru import logger

# os shortcuts
sep = os.sep
walk = os.walk
rmdir = os.rmdir
rename = os.rename
remove = os.remove
getcwd = os.getcwd
listdir = os.listdir
isdir = os.path.isdir
split = os.path.split
makedirs = os.makedirs
isfile = os.path.isfile
path_join = os.path.join
abspath = os.path.abspath
dirname = os.path.dirname
normpath = os.path.normpath
basename = os.path.basename
expanduser = os.path.expanduser


@logger.catch
def create_folder(folder_path):
    """Creates folder if not exists"""
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path, exist_ok=True)
        logger.debug(f'Create folder: {folder_path}')
    else:
        logger.debug(f'Folder exists: {folder_path}')


@logger.catch
def copytree(src, dst, symlinks=False, ignore=None):
    """Copy files and folders recursive"""
    for item in os.listdir(src):
        src_file = os.path.join(src, item)
        dst_file = os.path.join(dst, item)
        if os.path.isdir(src_file):
            shutil.copytree(src_file, dst_file, symlinks, ignore)
        else:
            shutil.copy2(src_file, dst_file)
    logger.debug(f'Copy folder structure, src: {src}, dst: {dst}')


class NestedDefaultDict(defaultdict):
    """Nested dict, which can be dynamically expanded"""

    def __init__(self, *args, **kwargs):
        super().__init__(NestedDefaultDict, *args, **kwargs)

    def __repr__(self):
        return repr(dict(self))

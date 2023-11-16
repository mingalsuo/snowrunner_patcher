#!/usr/bin/env python3

'''A tool to apply SnowRunner-mods with'''

import os
import sys
import shutil
import zipfile

__author__ = "Markus Ingalsuo"
__copyright__ = "Copyright 2023, Markus Ingalsuo"
__credits__ = ["Markus Ingalsuo",]
__license__ = "GNU General Public License v3.0"
__version__ = "0.9"
__maintainer__ = "Markus Ingalsuo"
__email__ = "markus.ingalsuo@gmail.com"
__status__ = "Development"

home = os.path.expanduser("~")

SNOWRUNNER_PATH = os.path.join(
    home,
    '.steam/steam/steamapps/common/SnowRunner/preload/paks/client/initial.pak'
)

PATCH_PATH = os.path.abspath(sys.argv[1])

if not PATCH_PATH.lower().endswith('.zip'):
    sys.exit('\n usage: python3 snowrunner_patcher.py path/to/patch.zip\n')

TMP_PATH_BASE = '/tmp/snowrunner_patcher/'
TMP_PATH_ORIG = TMP_PATH_BASE + 'orig'
TMP_PATH_PATCH = TMP_PATH_BASE + 'patch'
TMP_PATH_PATCH_LEN = len(os.path.split(TMP_PATH_PATCH)) + 2

if not os.path.isfile(SNOWRUNNER_PATH):
    sys.exit('Could not find SnowRunner.')

if os.path.isdir(TMP_PATH_BASE):
    shutil.rmtree(TMP_PATH_BASE)

with zipfile.ZipFile(SNOWRUNNER_PATH, 'r') as zip_ref:
    zip_ref.extractall(TMP_PATH_ORIG)

with zipfile.ZipFile(PATCH_PATH, 'r') as zip_ref:
    zip_ref.extractall(TMP_PATH_PATCH)

os.chdir(TMP_PATH_PATCH)
for root, dirs, files in os.walk(TMP_PATH_PATCH):
    for file in files:
        FILE_PATH = os.path.join(root, file)
        DUMB_NAME = '\\'.join(FILE_PATH.split('/')[TMP_PATH_PATCH_LEN:])
        shutil.copyfile(FILE_PATH, TMP_PATH_ORIG + '/' + DUMB_NAME)

os.chdir(TMP_PATH_ORIG)
with zipfile.ZipFile(SNOWRUNNER_PATH, 'w') as zip_ref:
    for file in os.listdir(TMP_PATH_ORIG):
        zip_ref.write(file)

if os.path.isdir(TMP_PATH_BASE):
    shutil.rmtree(TMP_PATH_BASE)

import os
import sys

import cliapp
from yarnutils import *

import yarnhelper

srcdir = os.environ['SRCDIR']
datadir = os.environ['DATADIR']

helper = yarnhelper.YarnHelper()

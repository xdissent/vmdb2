import os
import sys

import cliapp
from yarnutils import *

import yarnhelper

srcdir = os.environ['SRCDIR']
datadir = os.environ['DATADIR']

vars = Variables(datadir)

helper = yarnhelper.YarnHelper()

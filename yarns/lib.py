import os
import sys

import cliapp
from yarnutils import *

srcdir = os.environ['SRCDIR']
datadir = os.environ['DATADIR']

vars = Variables(datadir)

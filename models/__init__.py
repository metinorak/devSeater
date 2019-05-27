from os.path import dirname, basename, isfile
import glob
modules = glob.glob(dirname(__file__)+"/*.py")
moduleNames = [ basename(f)[:-3] for f in modules if isfile(f) and f.endswith('Model.py') ]

import importlib

Objects = dict()

def upperFirst(s):
  return s[0].capitalize() + s[1:]


for moduleName in moduleNames:
  module = importlib.import_module("models." + moduleName)
  the_class = getattr(module, upperFirst(moduleName))
  Objects[moduleName] = the_class()


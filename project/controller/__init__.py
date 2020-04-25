import importlib
from os.path import dirname, basename, isfile
import glob

# Auto load controllers
modules = glob.glob(dirname(__file__)+"/*.py")
moduleNames = [ basename(f)[:-3] for f in modules if isfile(f) ]
for moduleName in moduleNames:
  importlib.import_module("project.controller." + moduleName)
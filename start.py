from common import *
import os
import importlib


#Import all controllers

moduleNames = []

for r, d, f in os.walk("."):
    for file in f:
        if 'Controller.py' in file:
            moduleNames.append(os.path.join(r, file)[2:-3])

for moduleName in moduleNames:
  importlib.import_module(moduleName)

if __name__ == "__main__":
  app.run(debug=True)
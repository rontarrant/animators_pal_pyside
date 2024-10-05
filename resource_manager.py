## python libs
import os
import sys

class ResourceManager:
   def __init__(self, base_path) -> None:
      self.base_path = base_path
      
   def get_resource_path(self, relative_path):
      if getattr(sys, 'frozen', False):
         ## running in a PyInstaller bundle
         return os.path.join(sys._MEIPASS, relative_path)
      else:
         ## running in a normal Python environment
         return os.path.join(self.base_path, relative_path)


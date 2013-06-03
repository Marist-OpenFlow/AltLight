import json
import requests

class ControllerHelper:
   def __init__(self, address, port):
      self.uri = "http://" + address + ":" + port
   def getReq(self, location):
      return requests.get(self.uri + location).json()
   def getHealth(self):
      return self.getReq("/wm/core/health/json")
   def getMemory(self):
      return self.getReq("/wm/core/memory/json")
   def getLoadedModules(self):
      return self.getReq("/wm/core/module/loaded/json")

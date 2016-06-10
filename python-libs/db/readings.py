from sqlite import Sqlite

class Readings(Sqlite):
   
  table = "readings"
  
  device_bathroom = "bathroom-light"
  device_door = "door"
  devices = [device_bathroom,device_door]
  
  def __init__(self):
    Sqlite.__init__(self)
    #This table must be included in the default schema (see evolutions)
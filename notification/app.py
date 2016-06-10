#!/usr/bin/python
import time
from services.gmail import Gmail
import ConfigParser
from db.readings import Readings
from services.network import Network

config = ConfigParser.ConfigParser()
config.read("config.cfg")

nmap_enabled = config.getboolean('network','nmap_enabled')
network = Network(nmap_enabled)
readings = Readings()

user =config.get('gmail', 'user')
password =config.get('gmail', 'password')

gmail = Gmail(user,password)

email_freq = config.get('config','email-frequency')
email_to = [config.get('config','notification-email')]
notification_warning = config.get('config','notification-warning')

last_missing_bathroom_email = 0
last_door_email = 0
last_bathroom_email = 0

bathroom_threshold = config.get('bathroom','value-threshold')

def empty_home():
  #Search by mac
  '''
  for phone in config.items("macs"):
    name = phone[0]
    mac = phone[1]
    device =  network.get(mac)
    if device is not None and device.is_up(): return False
  return True
  '''
  #Search by local ip
  for phone in config.items("ips"):
    name = phone[0]
    ip = phone[1]
    device =  network.get_ip(ip)
    if device is not None: return False
  return True

def time_format(timestamp):
  return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
  
#TODO Unify both sensors using boolean checks in config
def bathroom_light(timestamp, value): 
        
  if (last_missing_bathroom_email + email_freq * 3600 < now and
      timestamp < now - notification_warning * 60):
    print "Device {} is not sending new values since {}".format(device,timestamp)
    
    gmail.send(email_to, "Device {} is not sending readings".format('bathroom_light'), 
               """The device {} is not sending new readings since {}""".format('bathroom_light', time_format(timestamp)))
    last_missing_bathroom_email = now
  
  if value > bathroom_threshold and empty_home():
    gmail.send(email_to, "Bathroom light is ON", "Bathroom light is ON and nobody is at home")
    
def door(timestamp, value):
  if empty_home():
    gmail.send(email_to, "Door is OPEN", "Door is OPEN and nobody is at home")
  
try:

  while True:
    
    now = int(time.time())
    last_email = 0
    
    for device in readings.devices:
      read = readings.last(device)
      timestamp = read[1]
      value = read[2]
                    
      print 'Last {} value {} at {}'.format(device, value,time_format(timestamp))     
      
    if device == readings.device_bathroom:
      bathroom_light(timestamp,value)
    elif device == readings.device_door:
      door(timestamp,value)
      
    time.sleep(30)
            
except KeyboardInterrupt:
  pass
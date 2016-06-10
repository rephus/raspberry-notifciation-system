import subprocess

#output = subprocess.check_output("arp -a", shell=True)

#nmap output sample:
"""
Starting Nmap 6.40 ( http://nmap.org ) at 2014-07-01 19:35 BST
Nmap scan report for SkyRouter.Home (192.168.2.1)
Host is up (0.00059s latency).
Nmap scan report for Unknown (192.168.2.100)
Host is up (0.000058s latency).
Nmap done: 256 IP addresses (14 hosts up) scanned in 2.45 seconds
"""

#arp -a output sample:
"""
SkyRouter.Home (192.168.2.1) en 3c:81:d8:aa:75:f7 [ether] en eth0
? (192.168.2.152) en 00:0c:29:4d:17:92 [ether] en eth0
Unknown (192.168.2.172) en 00:0c:29:06:3b:97 [ether] en eth0

#ping -c 1 output sample:
PING 192.168.0.105 (192.168.0.105) 56(84) bytes of data.
From 192.168.0.137 icmp_seq=1 Destination Host Unreachable

--- 192.168.0.105 ping statistics ---
1 packets transmitted, 0 received, +1 errors, 100% packet loss, time 0ms

"""

class Network:
  
  def __init__(self, nmap = False): 
    
    if nmap: 
      print "Initializing nmap scan"
      self._nmap()
    #print "List of devices in network:"
    #print self.list()
    
  def _nmap(self):
    output = subprocess.check_output("nmap -sP 192.168.2.*| grep -v 'Starting\|done:' ", shell=True)
    for line in output.split("Nmap scan report for "):
      info = line.replace("\n"," ").split(" ")
      host = info[0]
      if self.is_ip(host):
        ip = host
      else: 
        ip = info[1].replace("(","").replace(")","")
      
      print "Listing nmap devices: Host {} IP {} ".format(host,ip)

  def get(self,mac):
    command = "arp -a | grep '{}' || /bin/true".format(mac)
    output = subprocess.check_output(command, stderr=subprocess.STDOUT,shell=True)
    if not output: return None
    info = output.split(" ")
    return Device(host = info[0],
                  ip = info[1].replace("(","").replace(")",""),
                  mac = info[3])
  
  def get_ip(self,ip):
    command = "ping -c 1 {} | grep ttl || /bin/true".format(ip)
    output = subprocess.check_output(command, stderr=subprocess.STDOUT,shell=True)
    if not output: return None
    info = output.split(" ")
    return Device(host = "",
                  ip = info[1],
                  mac = "")
    
  
  def list(self):
    output = subprocess.check_output("arp -a", shell=True)
    devices = []
    for line in output.split("\n"):
      if not line: break
      info = line.split(" ")
      devices.append(Device(host = info[0],
                            ip = info[1].replace("(","").replace(")",""),
                            mac = info[3]))
    return devices
    
  def is_ip(self, text):
    return len(text.split('.')) == 4
  

class Device:
   def __repr__(self):
     return "Host: {}, IP: {}, MAC: {}".format(self.host,self.ip,self.mac)
   def __init__(self, host,ip,mac):
     self.host = host
     self.ip = ip
     self.mac = mac
     
   def is_up(self):
     command = "nmap -sP {} | grep 'Host is up' | wc -l".format(self.ip)
     output = subprocess.check_output(command, shell=True)
     return "1" in output 
     
     

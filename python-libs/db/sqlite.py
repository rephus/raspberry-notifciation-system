#https://docs.python.org/2/library/sqlite3.html
import sqlite3

#TODO: This class must be a singleton (1 connection)
class Sqlite:
  
  _db = "/var/sqlite/rf24.db"
  def __init__(self):
    self._conn = sqlite3.connect(self._db, check_same_thread=False)
    
  def all(self, limit = 1000):
    c = self._conn.cursor()
    c.execute('SELECT * FROM {}  order by id desc LIMIT {}'.format(self.table, limit = 1000))
    result = c.fetchall()
    c.close()
    return result
  
  def last(self):
    c = self._conn.cursor()
    c.execute('SELECT * FROM {} ORDER BY id DESC LIMIT 1'.format(self.table))
    result = c.fetchone()
    c.close()
    return result
  
  def last(self, device):
    c = self._conn.cursor()
    c.execute("SELECT * FROM {} WHERE device = '{}' ORDER BY id DESC LIMIT 1".format(self.table,device))
    result = c.fetchone()
    c.close()
    return result
    
  def count(self):
    c = self._conn.cursor()
    c.execute('SELECT COUNT(*) FROM {}'.format(self.table))
    result = c.fetchone()
    c.close()
    return result[0]
  
  def destroy(self):
    self._conn.close()
import mysql.connector
from models.config import *
from mysql.connector import pooling
import time

class Database(): 
  dbconfig = {
      "host": DB_HOST,
      "user": DB_USER,
      "password": DB_PASSWORD,
      "database": DB_NAME
    }

  cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "devseater", pool_size = 1, **dbconfig)
  
  def getConnection(self):
    while(True):
      try:
        return self.cnxpool.get_connection()
      except Exception as e:
        time.sleep(0.5)
        print(e)

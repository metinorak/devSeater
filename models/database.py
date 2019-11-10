import mysql.connector
from models.config import *
from mysql.connector import pooling
import time

class Database(): 
  try:
    dbconfig
  except NameError:
    dbconfig = {
        "host": DB_HOST,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "database": DB_NAME
      }

  try:
    cnxpool
  except NameError:  
    cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "devseater", pool_size = 8, **dbconfig)
  
  def getConnection(self):
    while(True):
      try:
        return self.cnxpool.get_connection()
      except Exception as e:
        print(e)

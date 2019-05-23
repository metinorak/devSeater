import mysql.connector
from models.config import *
from mysql.connector import pooling


def decorator(f):
  def decorated_function(*args, **kwargs):
      try:
        return f(*args, **kwargs)
      except Exception as e:
        print(e)
  return decorated_function



class Database():
  dbconfig = {
      "host": DB_HOST,
      "user": DB_USER,
      "password": DB_PASSWORD,
      "database": DB_NAME
    }

  cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "devseater", pool_size = 32, **dbconfig)
  
  def getConnection(self):
    return self.cnxpool.get_connection()


  





    


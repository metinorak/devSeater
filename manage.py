from project.lib.database import Database
from project.config import DB_NAME
import sys

params = sys.argv[1:]

for param in params:
    if param == "migrate":
        try:
            connection = Database.getConnection()
            cursor = connection.cursor()         

            # Read sql file
            sql_file = open("sql/devseater.sql", "r")
            query = sql_file.read()
            
            # Execute the queries in the sql file
            for result in cursor.execute(query, multi=True):
                print(result)
            connection.commit()
        
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()
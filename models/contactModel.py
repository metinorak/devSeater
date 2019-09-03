from models.database import *

class ContactModel(Database):

  def addContactMessage(self, msg):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "INSERT INTO contactMessages(name, subject, email, message) VALUES(%s, %s, %s, %s)"
      cursor.execute(query, (msg["name"], msg["subject"], msg["email"], msg["message"]) )
      connection.commit()
    except Exception as e:
      print(e)
      return
    finally:
      cursor.close()
      connection.close()

  def getLastContactMessages(self, page, messageNumberPerPage):
    previousMessageNumber = (page - 1) * messageNumberPerPage

    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM contactMessages ORDER BY time DESC LIMIT %s,%s"
      cursor.execute(query, (previousMessageNumber, messageNumberPerPage))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return
    finally:
      cursor.close()
      connection.close()
    return result
  
  def removeContactMessage(self, cmid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "DELETE FROM contactMessages WHERE cmid = %s"
      cursor.execute(query, (cmid,) )
      connection.commit()
    except Exception as e:
      print(e)
      return
    finally:
      cursor.close()
      connection.close()
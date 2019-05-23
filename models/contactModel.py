from models.database import *

class ContactModel(Database):
  def addContactMessage(self, msg):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO contactMessages(name, email, message) VALUES(%s, %s, %s)"
    cursor.execute(query, (msg["name"], msg["email"], msg["message"]) )
    self.commit()
    cursor.close()
    connection.close()

  def getLastContactMessages(self, page, messageNumberPerPage):
    previousMessageNumber = (page - 1) * messageNumberPerPage

    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM contactMessages ORDER BY time DESC LIMIT %s,%s"
    cursor.execute(query, (uid, previousMessageNumber, messageNumberPerPage))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result
  
  def removeContactMessage(self, cmid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM contactMessages WHERE cmid = %s"
    cursor.execute(query, (cmid,) )
    self.commit()
    cursor.close()
    connection.close()
from models.database import *

class ContactModel(Database):
  @exception_handling
  def addContactMessage(self, msg):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO contactMessages(name, subject, email, message) VALUES(%s, %s, %s, %s)"
    cursor.execute(query, (msg["name"], msg["subject"], msg["email"], msg["message"]) )
    connection.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def getLastContactMessages(self, page, messageNumberPerPage):
    previousMessageNumber = (page - 1) * messageNumberPerPage

    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM contactMessages ORDER BY time DESC LIMIT %s,%s"
    cursor.execute(query, (previousMessageNumber, messageNumberPerPage))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result
  
  @exception_handling
  def removeContactMessage(self, cmid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM contactMessages WHERE cmid = %s"
    cursor.execute(query, (cmid,) )
    connection.commit()
    cursor.close()
    connection.close()
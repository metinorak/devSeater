from project.lib.database import Database

class ContactModel():

  @staticmethod
  def addContactMessage(msg):
    connection = Database.getConnection()
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

  @staticmethod
  def getLastContactMessages(page, messageNumberPerPage):
    previousMessageNumber = (page - 1) * messageNumberPerPage

    connection = Database.getConnection()
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
  
  @staticmethod
  def removeContactMessage(cmid):
    connection = Database.getConnection()
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
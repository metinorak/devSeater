from models.database import *

class SeaterModel(Database):
  @exception_handling
  def getAllProjectSeaters(self, pid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM seaters WHERE pid = %s"
    cursor.execute(query, (pid,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

  @exception_handling
  def getEmptyProjectSeaters(self, pid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM seaters WHERE pid = %s AND uid = NULL"
    cursor.execute(query, (pid,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

  @exception_handling
  def getFilledProjectSeaters(self, pid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM seaters WHERE pid = %s AND uid IS NOT NULL"
    cursor.execute(query, (pid,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result
  
  @exception_handling
  def getProjectSeaterNumber(self, pid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM seaters WHERE pid = %s"
    cursor.execute(query, (pid,))
    cursor.fetchall()
    count = cursor.rowcount()
    cursor.close()
    connection.close()
    return count

  @exception_handling
  def getUserSeaters(self, uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM seaters WHERE uid = %s"
    cursor.execute(query, (uid,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

  @exception_handling
  def getUserSeaterNumber(self, uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT COUNT(*) AS number FROM seaters WHERE pid = %s"
    cursor.execute(query, (pid,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result["number"]
  
  @exception_handling
  def getSeater(self, sid, currentUser):
    isAspirated = self.isThereSeaterAspiration(currentUser, sid)

    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT seaters.* FROM seaters WHERE sid = %s"
    cursor.execute(query, (sid,))
    result = cursor.fetchone()
    result["isAspirated"] = isAspirated
    cursor.close()
    connection.close()
    return result

  @exception_handling
  def createSeater(self, pid, seater):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO seaters(pid, title, description) VALUES(%s, %s, %s)"
    cursor.execute(query, (seater["pid"], seater["title"], seater["description"]) )
    connection.commit()
    cursor.close()
    connection.close()
  
  @exception_handling
  def removeSeater(self, sid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM seaters WHERE sid = %s"
    cursor.execute(query, (sid,) )
    connection.commit()
    cursor.close()
    connection.close()
  
  @exception_handling
  def dismissUser(self, sid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE seaters SET uid = NULL WHERE sid = %s"
    cursor.execute(query, (sid,) )
    connection.commit()
    cursor.close()
    connection.close()
  
  @exception_handling
  def updateSeater(self, sid, title, description):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE seaters SET title = %s, description = %s WHERE sid = %s"
    cursor.execute(query, (title, description, sid) )
    connection.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def assignUser(self, uid, sid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE seaters SET uid = %s WHERE sid = %s"
    cursor.execute(query, (uid, sid) )
    connection.commit()
    cursor.close()
    connection.close()
  
  @exception_handling
  def unassignUser(self, sid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE seaters SET uid = NULL WHERE sid = %s"
    cursor.execute(query, (sid) )
    connection.commit()
    cursor.close()
    connection.close()
  
  @exception_handling
  def aspireSeater(self, uid, sid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO seaterAspirations(pid, title, description) VALUES(%s, %s, %s)"
    cursor.execute(query, (seater["pid"], seater["title"], seater["description"]) )
    connection.commit()
    cursor.close()
    connection.close()
  
  @exception_handling
  def cancelAspirationToSeater(self, uid, sid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM seaterAspirations WHERE uid = %s AND sid = %s"
    cursor.execute(query, (uid, sid) )
    connection.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def getSeaterAspirations(self, pid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT * FROM seaterAspirations WHERE isRejected = 0 AND sid IN 
    (SELECT sid FROM seaters WHERE pid = %s)"""
    cursor.execute(query, (pid,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result
  
  @exception_handling
  def isThereSeaterAspiration(self, uid, sid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM seaterAspirations WHERE uid = %s AND sid = %s AND isRejected = 0"
    cursor.execute(query, (uid, sid))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return (result != None)

  @exception_handling
  def rejectSeaterAspiration(self, uid, sid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE seaterAspirations SET isRejected = 1 WHERE  uid = %s AND sid = %s"
    cursor.execute(query, (uid, sid) )
    connection.commit()
    cursor.close()
    connection.close()
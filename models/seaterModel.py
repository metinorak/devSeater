from models.database import *

class SeaterModel(Database):
  @exception_handling
  def getAllProjectSeaters(self, pid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT seaters.*, projects.project_name 
    FROM seaters INNER JOIN projects ON seaters.pid = projects.pid WHERE projects.pid = %s"""
    cursor.execute(query, (pid,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

  @exception_handling
  def getEmptyProjectSeaters(self, pid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT seaters.*, projects.project_name 
    FROM seaters INNER JOIN projects ON seaters.pid = projects.pid WHERE projects.pid = %s AND uid IS NULL"""
    cursor.execute(query, (pid,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

  @exception_handling
  def getFilledProjectSeaters(self, pid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT seaters.*, projects.project_name,
    (SELECT username FROM users WHERE uid = seaters.uid) AS username  
    FROM seaters INNER JOIN projects ON seaters.pid = projects.pid WHERE projects.pid = %s AND uid IS NOT NULL"""
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
  def getProjectEmptySeaterNumber(self, pid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT COUNT(*) AS number FROM seaters WHERE pid = %s AND uid IS NULL"
    cursor.execute(query, (pid,))
    number = cursor.fetchone()["number"]
    cursor.close()
    connection.close()
    return number

  @exception_handling
  def getProjectFilledSeaterNumber(self, pid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT COUNT(*) AS number FROM seaters WHERE pid = %s AND uid IS NOT NULL"
    cursor.execute(query, (pid,))
    number = cursor.fetchone()["number"]
    cursor.close()
    connection.close()
    return number

  @exception_handling
  def getUserSeaters(self, uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT seaters.*, projects.project_name 
    FROM seaters INNER JOIN projects ON seaters.pid = projects.pid WHERE uid = %s"""
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
  def getSeater(self, sid, currentUser=None):
    isAspirated = self.isThereSeaterAspiration(currentUser, sid)

    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT seaters.*, projects.project_name 
    FROM seaters INNER JOIN projects ON seaters.pid = projects.pid WHERE sid = %s"""
    cursor.execute(query, (sid,))
    result = cursor.fetchone()
    result["isAspirated"] = isAspirated
    cursor.close()
    connection.close()

    if currentUser != None:
      result["isAssigned"] = (result["uid"] == currentUser)
    else:
      result["isAssigned"] = False
      
    return result

  @exception_handling
  def createSeater(self, pid, seater):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO seaters(pid, title, short_description, full_description) VALUES(%s, %s, %s, %s)"
    cursor.execute(query, (seater["pid"], seater["title"], seater["short_description"], seater["full_description"]) )
    sid = cursor.lastrowid
    connection.commit()
    cursor.close()
    connection.close()
    return sid
  
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
  def aspireSeater(self, uid, sid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO seaterAspirations(sid, uid) VALUES(%s, %s)"
    cursor.execute(query, (sid, uid) )
    connection.commit()
    cursor.close()
    connection.close()
  
  @exception_handling
  def cancelAspirationToTheSeater(self, uid, sid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM seaterAspirations WHERE uid = %s AND sid = %s"
    cursor.execute(query, (uid, sid) )
    connection.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def getSeaterAspirations(self, sid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT * FROM seaterAspirations WHERE isRejected = 0 AND sid = %s"""
    cursor.execute(query, (pid,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

  @exception_handling
  def getSeaterAspirationsByPid(self, sid):
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
    result = cursor.fetchone()
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
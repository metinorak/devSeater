from project.lib.database import Database

class SeaterModel():
  
  @staticmethod
  def getAllProjectSeaters(pid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT seaters.*, projects.project_name,
      (SELECT COUNT(*) FROM seaterAspirations WHERE sid = seaters.sid AND isRejected = 0) AS aspirationNumber 
      FROM seaters INNER JOIN projects ON seaters.pid = projects.pid WHERE projects.pid = %s"""
      cursor.execute(query, (pid,))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  @staticmethod
  def getEmptyProjectSeaters(pid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT seaters.*, projects.project_name,
      (SELECT COUNT(*) FROM seaterAspirations WHERE sid = seaters.sid AND isRejected = 0) AS aspirationNumber 
      FROM seaters INNER JOIN projects ON seaters.pid = projects.pid WHERE projects.pid = %s AND uid IS NULL"""
      cursor.execute(query, (pid,))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result
  
  @staticmethod
  def getFilledProjectSeaters(pid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT seaters.*, projects.project_name,
      (SELECT username FROM users WHERE uid = seaters.uid) AS username  
      FROM seaters INNER JOIN projects ON seaters.pid = projects.pid WHERE projects.pid = %s AND uid IS NOT NULL"""
      cursor.execute(query, (pid,))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result
  
  @staticmethod
  def getProjectSeaterNumber(pid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM seaters WHERE pid = %s"
      cursor.execute(query, (pid,))
      cursor.fetchall()
      count = cursor.rowcount()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return count

  @staticmethod
  def getProjectEmptySeaterNumber(pid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT COUNT(*) AS number FROM seaters WHERE pid = %s AND uid IS NULL"
      cursor.execute(query, (pid,))
      number = cursor.fetchone()["number"]
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return number
  
  @staticmethod
  def getProjectFilledSeaterNumber(pid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT COUNT(*) AS number FROM seaters WHERE pid = %s AND uid IS NOT NULL"
      cursor.execute(query, (pid,))
      number = cursor.fetchone()["number"]
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return number
  
  @staticmethod
  def getSeaterAspirationNumber(sid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT COUNT(*) AS number FROM seaterAspirations WHERE sid = %s AND isRejected = 0"
      cursor.execute(query, (sid,))
      number = cursor.fetchone()["number"]
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return number
  
  @staticmethod
  def getUserSeaters(uid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT seaters.*, projects.project_name 
      FROM seaters INNER JOIN projects ON seaters.pid = projects.pid WHERE uid = %s"""
      cursor.execute(query, (uid,))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  @staticmethod
  def getUserSeaterNumber(uid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT COUNT(*) AS number FROM seaters WHERE uid = %s"
      cursor.execute(query, (uid,))
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result["number"]
  
  @staticmethod
  def getSeater(sid, currentUser=None):
    isAspirated = SeaterModel.isThereSeaterAspiration(currentUser, sid)

    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT seaters.*, projects.project_name 
      FROM seaters INNER JOIN projects ON seaters.pid = projects.pid WHERE sid = %s"""
      cursor.execute(query, (sid,))
      result = cursor.fetchone()
      result["isAspirated"] = isAspirated

      if currentUser != None:
        result["isAssigned"] = (result["uid"] == currentUser)
      else:
        result["isAssigned"] = False
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
      
    return result

  @staticmethod
  def createSeater(pid, seater):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "INSERT INTO seaters(pid, title, short_description, full_description) VALUES(%s, %s, %s, %s)"
      cursor.execute(query, (seater["pid"], seater["title"], seater["short_description"], seater["full_description"]) )
      sid = cursor.lastrowid
      connection.commit()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return sid
  
  @staticmethod
  def removeSeater(sid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "DELETE FROM seaters WHERE sid = %s"
      cursor.execute(query, (sid,) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  @staticmethod
  def dismissUser(sid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "UPDATE seaters SET uid = NULL WHERE sid = %s"
      cursor.execute(query, (sid,) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  @staticmethod
  def updateSeater(sid, title, description):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "UPDATE seaters SET title = %s, description = %s WHERE sid = %s"
      cursor.execute(query, (title, description, sid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()

  @staticmethod
  def assignUser(uid, sid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "UPDATE seaters SET uid = %s WHERE sid = %s"
      cursor.execute(query, (uid, sid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  @staticmethod
  def aspireSeater(uid, sid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "INSERT INTO seaterAspirations(sid, uid) VALUES(%s, %s)"
      cursor.execute(query, (sid, uid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  @staticmethod
  def cancelAspirationToTheSeater(uid, sid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "DELETE FROM seaterAspirations WHERE uid = %s AND sid = %s"
      cursor.execute(query, (uid, sid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()

  @staticmethod
  def getSeaterAspirations(sid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT seaterAspirations.*, users.username, users.uid, users.photo, users.full_name
      FROM seaterAspirations 
      INNER JOIN users ON seaterAspirations.uid = users.uid
      WHERE isRejected = 0 AND sid = %s"""
      cursor.execute(query, (sid,))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  @staticmethod
  def getSeaterAspirationsByPid(pid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT * FROM seaterAspirations WHERE isRejected = 0 AND sid IN 
      (SELECT sid FROM seaters WHERE pid = %s)"""
      cursor.execute(query, (pid,))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result
  
  @staticmethod
  def isThereSeaterAspiration(uid, sid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM seaterAspirations WHERE uid = %s AND sid = %s AND isRejected = 0"
      cursor.execute(query, (uid, sid))
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return (result != None)

  @staticmethod
  def rejectSeaterAspiration(uid, sid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "UPDATE seaterAspirations SET isRejected = 1 WHERE  uid = %s AND sid = %s"
      cursor.execute(query, (uid, sid) )
      connection.commit()
    except Exception as e:
      print(e)
    cursor.close()
    connection.close()
from project.lib.database import Database

class ProjectModel():
  
  @staticmethod
  def createProject(project, founder_uid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "INSERT INTO projects(project_name, short_description, full_description) VALUES(%s, %s, %s)"
      cursor.execute(query, (project["project_name"], project["short_description"], project["full_description"]) )

      query = "INSERT INTO projectAdmins(uid, pid) VALUES(%s, %s)"
      pid = cursor.lastrowid
      cursor.execute(query, (founder_uid, pid))
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  @staticmethod
  def getUserProjects(uid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT * FROM projects WHERE pid IN (SELECT DISTINCT pid FROM seaters WHERE uid = %s)
      UNION
      SELECT * FROM projects WHERE pid IN (SELECT pid FROM projectAdmins WHERE uid = %s)"""
      cursor.execute(query, (uid, uid) )
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result
  
  @staticmethod
  def getProject(pid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM projects WHERE pid = %s"
      cursor.execute(query, (pid,) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  @staticmethod
  def getLastProjects(count):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT * FROM projects ORDER BY pid DESC LIMIT %s"""
      cursor.execute(query, (count, ) )
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  @staticmethod
  def getProjectByProjectName(name):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM projects WHERE project_name = %s"
      cursor.execute(query, (name,) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result
  
  @staticmethod
  def getMembers(pid, currentUserId):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """
      (SELECT users.*, 
      (SELECT COUNT(*) FROM followers WHERE flwrid = %s AND flwdid = users.uid) AS isFollowed
      FROM users WHERE uid IN 
      (SELECT uid FROM seaters JOIN projects ON(projects.pid = seaters.pid) WHERE uid IS NOT NULL AND projects.pid = %s))
      UNION
      (SELECT users.*, 
      (SELECT COUNT(*) FROM followers WHERE flwrid = %s AND flwdid = users.uid) AS isFollowed
      FROM users WHERE uid IN 
      (SELECT uid FROM projectAdmins JOIN projects ON(projects.pid = projectAdmins.pid) WHERE projects.pid = %s))
      """
      cursor.execute(query, (currentUserId, pid, currentUserId, pid) )
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result
  
  @staticmethod
  def getNumberOfMembers(pid):
    #By team member number
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """
      (SELECT * FROM users WHERE uid IN 
      (SELECT uid FROM seaters JOIN projects ON(projects.pid = seaters.pid) WHERE uid IS NOT NULL AND projects.pid = %s))
      UNION
      (SELECT * FROM users WHERE uid IN 
      (SELECT uid FROM projectAdmins JOIN projects ON(projects.pid = projectAdmins.pid) WHERE projects.pid = %s))
      """
      cursor.execute(query, (pid, pid) )
      cursor.fetchall()
      count = cursor.rowcount
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return count 
  
  @staticmethod
  def getPopularProjects(number):
    #By team member number
    #THIS SHOULD BE TESTED
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """
      SELECT projects.*, COUNT(seaters.sid) AS number
      FROM projects LEFT JOIN seaters ON seaters.pid = projects.pid 
      GROUP BY projects.pid ORDER BY number DESC LIMIT %s
      """
      cursor.execute(query, (number,) )
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result 

  @staticmethod
  def updateProjectPhoto(pid, photo):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "UPDATE projects SET photo = %s WHERE pid = %s"
      cursor.execute(query, (photo, pid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()

  @staticmethod
  def updateProjectName(pid, name):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "UPDATE projects SET project_name = %s WHERE pid = %s"
      cursor.execute(query, (name, pid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  @staticmethod
  def updateShortDescription(pid, shortDescription):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "UPDATE projects SET short_description = %s WHERE pid = %s"
      cursor.execute(query, (shortDescription, pid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  @staticmethod
  def updateFullDescription(pid, fullDescription):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE projects SET full_description = %s WHERE pid = %s"
    cursor.execute(query, (fullDescription, pid) )
    connection.commit()
    cursor.close()
    connection.close()

  @staticmethod
  def searchProjects(keyword, number):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM projects WHERE project_name LIKE %s LIMIT %s"
      result = cursor.execute(query, ("%" + keyword + "%", number))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  #PROJECT ADMINS
  
  @staticmethod
  def getProjectAdmins(pid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM users WHERE uid IN (SELECT uid FROM projectAdmins WHERE pid = %s)"
      result = cursor.execute(query, (pid,) )
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result
  
  @staticmethod
  def isProjectAdmin(uid, pid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM projectAdmins WHERE uid = %s AND pid = %s"
      result = cursor.execute(query, (uid, pid) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
    return (result != None)

  @staticmethod
  def isProjectMember(uid, pid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """
      (SELECT * FROM users WHERE uid IN 
      (SELECT uid FROM seaters JOIN projects ON(projects.pid = seaters.pid) WHERE uid = %s AND projects.pid = %s))
      UNION
      (SELECT * FROM users WHERE uid IN 
      (SELECT uid FROM projectAdmins JOIN projects ON(projects.pid = projectAdmins.pid) WHERE uid = %s AND projects.pid = %s))"""
      cursor.execute(query, (uid, pid, uid, pid) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
    return (result != None)
  
  @staticmethod
  def isThereThisProjectName(name):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM projects WHERE project_name = %s)"
      result = cursor.execute(query, (name,) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
    return (result != None)
  
  @staticmethod
  def removeProjectAdmin(pid, uid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "DELETE FROM projectAdmins WHERE pid = %s AND uid = %s"
      cursor.execute(query, (pid, uid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()

  #PROJECT LINKS

  @staticmethod
  def getProjectLinks(pid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM projectLinks WHERE pid = %s"
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
  def getProjectLink(plid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM projectLinks WHERE plid = %s"
      cursor.execute(query, (plid,))
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  @staticmethod
  def addProjectLink(pid, name, link):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "INSERT INTO projectLinks(pid, name, link) VALUES(%s, %s, %s)"
      cursor.execute(query, (pid, name, link))
      plid = cursor.lastrowid
      connection.commit()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return plid
  
  @staticmethod
  def removeProjectLink(plid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "DELETE FROM projectLinks WHERE plid = %s"
      cursor.execute(query, (plid,) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()

  @staticmethod
  def updateProjectLink(plid, name, link):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "UPDATE projectLinks SET name = %s, link = %s WHERE plid = %s"
      cursor.execute(query, (name, link, plid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
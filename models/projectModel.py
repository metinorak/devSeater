from models.database import *

class ProjectModel(Database):
  @exception_handling
  def createProject(self, project, founder_uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO projects(project_name, short_description, full_description) VALUES(%s, %s, %s)"
    cursor.execute(query, (project["project_name"], project["short_description"], project["full_description"]) )

    query = "INSERT INTO projectAdmins(uid, pid) VALUES(%s, %s)"
    pid = cursor.lastrowid
    cursor.execute(query, (founder_uid, pid))

    connection.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def getUserProjects(self, uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT * FROM projects WHERE pid IN (SELECT DISTINCT pid FROM seaters WHERE uid = %s)
    UNION
    SELECT * FROM projects WHERE pid IN (SELECT pid FROM projectAdmins WHERE uid = %s)"""
    cursor.execute(query, (uid, uid) )
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result
  
  @exception_handling
  def getProject(self, pid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM projects WHERE pid = %s"
    cursor.execute(query, (pid,) )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

  @exception_handling
  def getProjectByProjectName(self, name):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM projects WHERE project_name = %s"
    cursor.execute(query, (name,) )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result
  
  @exception_handling
  def getMembers(self, pid, currentUser):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
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
    cursor.execute(query, (currentUser, pid, currentUser, pid) )
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result
  
  @exception_handling
  def getNumberOfMembers(self, pid):
    #By team member number
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
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
    cursor.close()
    connection.close()
    return count 
  
  @exception_handling
  def getPopularProjects(self, number):
    #By team member number
    #THIS SHOULD BE TESTED
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT projects.*, COUNT(seaters.pid) AS number
    FROM projects INNER JOIN seaters ON seaters.pid = projects.pid GROUP BY seaters.pid ORDER BY number DESC LIMIT %s
    """
    cursor.execute(query, (number,) )
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result 

  @exception_handling
  def updateProjectPhoto(self, pid, photo):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE projects SET photo = %s WHERE pid = %s"
    cursor.execute(query, (photo, pid) )
    connection.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def updateProjectName(self, pid, name):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE projects SET name = %s WHERE pid = %s"
    cursor.execute(query, (name, pid) )
    connection.commit()
    cursor.close()
    connection.close()
  
  @exception_handling
  def updateShortDescription(self, pid, shortDescription):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE projects SET short_description = %s WHERE pid = %s"
    cursor.execute(query, (shortDescription, pid) )
    connection.commit()
    cursor.close()
    connection.close()
  
  @exception_handling
  def updateFullDescription(self, pid, fullDescription):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE projects SET full_description = %s WHERE pid = %s"
    cursor.execute(query, (fullDescription, pid) )
    connection.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def searchProjects(self, keyword, number):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM projects WHERE project_name LIKE %s LIMIT %s"
    result = cursor.execute(query, ("%" + keyword + "%", number))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

  #PROJECT ADMINS
  @exception_handling
  def getProjectAdmins(self, pid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE uid IN (SELECT uid FROM projectAdmins WHERE pid = %s)"
    result = cursor.execute(query, (pid,) )
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result
  
  @exception_handling
  def isProjectAdmin(self, uid, pid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM projectAdmins WHERE uid = %s AND pid = %s"
    result = cursor.execute(query, (uid, pid) )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return (result != None)

  @exception_handling
  def isProjectMember(self, uid, pid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """
    (SELECT * FROM users WHERE uid IN 
    (SELECT uid FROM seaters JOIN projects ON(projects.pid = seaters.pid) WHERE uid = %s AND projects.pid = %s))
    UNION
    (SELECT * FROM users WHERE uid IN 
    (SELECT uid FROM projectAdmins JOIN projects ON(projects.pid = projectAdmins.pid) WHERE uid = %s AND projects.pid = %s))"""
    cursor.execute(query, (uid, pid, uid, pid) )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return (result != None)
  
  @exception_handling
  def isThereThisProjectName(self, name):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM projects WHERE project_name = %s)"
    result = cursor.execute(query, (name,) )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return (result != None)
  
  @exception_handling
  def removeProjectAdmin(self, pid, uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM projectAdmins WHERE pid = %s AND uid = %s"
    cursor.execute(query, (pid, uid) )
    connection.commit()
    cursor.close()
    connection.close()

  #PROJECT LINKS
  @exception_handling
  def getProjectLinks(self, pid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM projectLinks WHERE pid = %s"
    cursor.execute(query, (pid,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result
  
  @exception_handling
  def getProjectLink(self, plid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM projectLinks WHERE plid = %s"
    cursor.execute(query, (plid,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

  @exception_handling
  def addProjectLink(self, pid, name, link):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO projectLinks(pid, name, link) VALUES(%s, %s, %s)"
    cursor.execute(query, (pid, name, link))
    connection.commit()
    cursor.close()
    connection.close()
  
  @exception_handling
  def removeProjectLink(self, plid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM projectLinks WHERE plid = %s"
    cursor.execute(query, (plid,) )
    connection.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def updateProjectLink(self, plid, name, link):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE projectLinks SET name = %s, link = %s WHERE plid = %s"
    cursor.execute(query, (name, link, plid) )
    connection.commit()
    cursor.close()
    connection.close()
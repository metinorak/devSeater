from models.database import *

class SkillModel(Database):
  @exception_handling
  def getUserSkills(self, uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT * FROM userSkills
    INNER JOIN skills ON skills.skid = userSkills.skid WHERE uid = %s"""
    result = cursor.execute(query, (uid,) )
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result
  
  @exception_handling
  def getUserSkill(self, skid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT * FROM userSkills
    INNER JOIN skills ON skills.skid = userSkills.skid WHERE skid = %s"""
    result = cursor.execute(query, (skid,) )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

  @exception_handling
  def getSeaterSkill(self, skid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT * FROM seaterSkills
    INNER JOIN skills ON skills.skid = seaterSkills.skid WHERE skid = %s"""
    result = cursor.execute(query, (skid,) )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

  @exception_handling
  def getSeaterSkills(self, sid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT * FROM seaterSkills
    INNER JOIN skills ON skills.skid = seaterSkills.skid WHERE uid = %s"""
    result = cursor.execute(query, (sid,) )
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result
  
  @exception_handling
  def getSkillByName(self, name):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM skills WHERE name = %s"
    result = cursor.execute(query, (name,) )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

  @exception_handling
  def addUserSkill(self, uid, skill):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)

    if self.isThereThisSkill(skill):
      skid = self.getSkillByName(skill)
      
    else:
      #Adding skill to the skills table
      query = "INSERT INTO skills(name) VALUES(%s)"
      cursor.execute(query, (skill,) )
      
      #Getting new added skill id
      skid = cursor.lastrowid

    #Adding user skill
    query = "INSERT INTO userSkills(uid, skid) VALUES(%s, %s)"
    cursor.execute(query, (uid, skid) )

    connection.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def addSeaterSkill(self, sid, skill):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)

    if self.isThereThisSkill(skill):
      skid = self.getSkillByName(skill)
    
    else:
      #Adding skill to the skills table
      query = "INSERT INTO skills(name) VALUES(%s)"
      cursor.execute(query, (skill,) )
      
      #Getting new added skill id
      skid = cursor.lastrowid

    #Adding user skill
    query = "INSERT INTO seaterSkills(uid, skid) VALUES(%s, %s)"
    cursor.execute(query, (uid, skid) )

    connection.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def removeUserSkill(self, skid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM userSkills WHERE skid = %s"
    cursor.execute(query, (skid,) )
    connection.commit()

    cursor.close()
    connection.close()
  
  @exception_handling
  def removeSeaterSkill(self, skid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM seaterSkills WHERE skid = %s"
    cursor.execute(query, (skid,) )
    connection.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def searchSkills(self, keyword, number):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM skills WHERE name LIKE %s LIMIT %s"
    result = cursor.execute(query, ("%" + keyword + "%", number))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

  @exception_handling
  def isThereThisSkill(self, skillName):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM skills WHERE skill = %s"
    result = cursor.execute(query, (skillName,) )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return (result != None)

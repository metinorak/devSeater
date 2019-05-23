from models.database import *

class SkillModel(Database):
  def getUserSkills(self, uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM skills WHERE skid IN (SELECT skid FROM userSkills WHERE uid = %s)"
    result = cursor.execute(query, (uid,) )
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result
  
  def getUserSkill(self, skid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM userSkills WHERE skid = %s"
    result = cursor.execute(query, (skid,) )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result


  def getSeaterSkill(self, skid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM seaterSkills WHERE skid = %s"
    result = cursor.execute(query, (skid,) )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

  
  def getSeaterSkills(self, sid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM skills WHERE skid IN (SELECT skid FROM seaterSkills WHERE sid = %s)"
    result = cursor.execute(query, (sid,) )
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result
  
  def getSkillByName(self, skill):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM skills WHERE name = %s"
    result = cursor.execute(query, (skill,) )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

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

  
  def removeUserSkill(self, skid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM userSkills WHERE skid = %s"
    cursor.execute(query, (skid,) )
    connection.commit()

    cursor.close()
    connection.close()
  
  def removeSeaterSkill(self, skid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM seaterSkills WHERE skid = %s"
    cursor.execute(query, (skid,) )
    connection.commit()
    cursor.close()
    connection.close()

  def searchSkills(self, keyword, number):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM skills WHERE name LIKE %s LIMIT %s"
    result = cursor.execute(query, ("%" + keyword + "%", number))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

  def isThereThisSkill(self, skillName):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM skills WHERE skill = %s"
    result = cursor.execute(query, (skillName,) )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return (result != None)

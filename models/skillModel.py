from models.database import *

class SkillModel(Database):
  
  def getUserSkills(self, uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT * FROM userSkills
      INNER JOIN skills ON skills.skid = userSkills.skid WHERE uid = %s"""
      result = cursor.execute(query, (uid,) )
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result
  
  def getUserSkill(self, skid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT * FROM userSkills
      INNER JOIN skills ON skills.skid = userSkills.skid WHERE skid = %s"""
      result = cursor.execute(query, (skid,) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  def getSeaterSkill(self, skid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT * FROM seaterSkills
      INNER JOIN skills ON skills.skid = seaterSkills.skid WHERE skid = %s"""
      result = cursor.execute(query, (skid,) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  
  def getSeaterSkills(self, sid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT * FROM seaterSkills
      INNER JOIN skills ON skills.skid = seaterSkills.skid WHERE sid = %s"""
      result = cursor.execute(query, (sid,) )
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result
  
  def getSkillByName(self, name):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM skills WHERE name = %s"
      result = cursor.execute(query, (name,) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  def addUserSkill(self, uid, skill):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)

    try:
      if self.isThereThisSkill(skill):
        skid = self.getSkillByName(skill)["skid"]
      
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
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return skid

  
  def addSeaterSkill(self, sid, skill):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)

    try:
      if self.isThereThisSkill(skill):
        skid = self.getSkillByName(skill)["skid"]
      
      else:
        #Adding skill to the skills table
        query = "INSERT INTO skills(name) VALUES(%s)"
        cursor.execute(query, (skill,) )
        
        #Getting new added skill id
        skid = cursor.lastrowid

      #Adding seater skill
      query = "INSERT INTO seaterSkills(sid, skid) VALUES(%s, %s)"
      cursor.execute(query, (sid, skid) )

      connection.commit()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return skid

  def removeUserSkill(self, uid, skid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "DELETE FROM userSkills WHERE uid = %s AND skid = %s"
      cursor.execute(query, (uid, skid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  def removeSeaterSkill(self, sid, skid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "DELETE FROM seaterSkills WHERE sid = %s AND skid = %s"
      cursor.execute(query, (sid, skid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()

  def searchSkills(self, keyword, number):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM skills WHERE name LIKE %s LIMIT %s"
      result = cursor.execute(query, ("%" + keyword + "%", number))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  def isThereThisSkill(self, skillName):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM skills WHERE name = %s"
      result = cursor.execute(query, (skillName,) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return (result != None)

from models.database import *
from passlib.hash import sha256_crypt

class UserModel(Database):
  def getUser(self, uid, currentUser = None):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    
    query = """SELECT
    (SELECT COUNT(*) FROM followers WHERE flwrid = %s AND flwdid = users.uid) AS isFollowed,
    users.* FROM users WHERE uid = %s"""
    cursor.execute(query, (currentUser, uid) )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result
  
  def getUserByUsername(self, username, currentUser = None):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT 
    (SELECT COUNT(*) FROM followers WHERE flwrid = %s AND flwdid = users.uid) AS isFollowed,
    users.* FROM users WHERE username = %s"""
    cursor.execute(query, (currentUser, username))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

  def getUserByEmail(self, email, currentUser = None):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT 
    (SELECT COUNT(*) FROM followers WHERE flwrid = %s AND flwdid = users.uid) AS isFollowed,
    users.* FROM users WHERE email = %s"""
    cursor.execute(query, (currentUser, email))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

  def addUser(self, user):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO users(email, username, password, full_name) VALUES(%s, %s, %s, %s)"
    cursor.execute(query, (user["email"], user["username"], user["password"], user["full_name"]) )
    connection.commit()
    cursor.close()
    connection.close()

  def removeUser(self, uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM users WHERE uid = %s"
    cursor.execute(query, (uid,) )
    connection.commit()
    cursor.close()
    connection.close()

  
  #CHECKING
  def login(self, email, password):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,) )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result != None:
      hashed_password = result["password"]
      if sha256_crypt.verify(password, hashed_password):
        return True
    
    return False
  
  def isThereThisUsername(self, username):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return (result != None)

  def isThereThisEmail(self, email):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return (result != None)
  
  def isEmailVerified(self, email):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE email = %s AND isEmailVerified = 1"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return (result != None)
  
  def isGlobalAdmin(self, uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM globalAdmins WHERE uid = %s"
    cursor.execute(query, (uid,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return (result != None)

  #UPDATE
  def updateFullname(self, uid, fullname):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE users SET full_name = %s WHERE uid = %s"
    cursor.execute(query, (fullname, uid))
    connection.commit()
    cursor.close()
    connection.close()
  
  def updateUsername(self, uid, username):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE users SET username = %s WHERE uid = %s"
    cursor.execute(query, (username, uid))
    connection.commit()
    cursor.close()
    connection.close()
  
  def updatePassword(self, uid, password):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE users SET password = %s WHERE uid = %s"
    cursor.execute(query, (password, uid))
    connection.commit()
    cursor.close()
    connection.close()
  
  def updateProfilePhoto(self, uid, photo):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE users SET photo = %s WHERE uid = %s"
    cursor.execute(query, (photo, uid))
    connection.commit()
    cursor.close()
    connection.close()

  def updateEmail(self, uid, email):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE users SET email = %s WHERE uid = %s"
    cursor.execute(query, (email, uid))
    connection.commit()
    cursor.close()
    connection.close()
  
  def updateBio(self, uid, bio):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE users SET bio = %s WHERE uid = %s"
    cursor.execute(query, (bio, uid))
    connection.commit()
    cursor.close()
    connection.close()
  
  
  def verifyEmail(self, email):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE users SET isEmailVerified = 1 WHERE email = %s"
    cursor.execute(query, (email,) )
    connection.commit()
    cursor.close()
    connection.close()
  
  
  #FOLLOW ACTIONS
  def follow(self, followerId, followedId):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO followers(flwrid, flwdid) VALUES(%s, %s)"
    cursor.execute(query, (followerId, followedId))
    connection.commit()
    cursor.close()
    connection.close()
  
  def unFollow(self, followerId, followedId):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM followers WHERE flwrid = %s AND flwdid = %s"
    cursor.execute(query, (followerId, followedId))
    connection.commit()
    cursor.close()
    connection.close()


  #USER LINKS
  def getUserLinks(self, uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM userLinks WHERE uid = %s"
    cursor.execute(query, (uid,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result
  
  def getUserLink(self, ulid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM userLinks WHERE ulid = %s"
    cursor.execute(query, (ulid,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

  def addUserLink(self, uid, name, link):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO userLinks(uid, name, link) VALUES(%s, %s, %s)"
    cursor.execute(query, (uid, name, link))
    connection.commit()
    cursor.close()
    connection.close()
  
  def removeUserLink(self, ulid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM userLinks WHERE ulid = %s"
    cursor.execute(query, (ulid,) )
    connection.commit()
    cursor.close()
    connection.close()

  def updateUserLink(self, ulid, name, link):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE userLinks SET name = %s, link = %s WHERE ulid = %s"
    cursor.execute(query, (name, link, ulid) )
    connection.commit()
    cursor.close()
    connection.close()
  
  def searchUsers(self, keyword, number):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE full_name LIKE %s OR username LIKE %s LIMIT %s"
    result = cursor.execute(query, ("%" + keyword + "%", "%" + keyword + "%", number))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

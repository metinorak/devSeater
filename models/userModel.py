from models.database import *
from passlib.hash import sha256_crypt

class UserModel(Database):
  @exception_handling
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

  @exception_handling
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

  @exception_handling
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

  @exception_handling
  def addUser(self, user):
    user["password"] = sha256_crypt.encrypt(user["password"])
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO users(email, username, password, full_name) VALUES(%s, %s, %s, %s)"
    cursor.execute(query, (user["email"], user["username"], user["password"], user["full_name"]) )
    connection.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def removeUser(self, uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM users WHERE uid = %s"
    cursor.execute(query, (uid,) )
    connection.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def getWhoToFollowList(self, number, currentUser = None):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT users.*, 
    (SELECT COUNT(*) FROM userPosts WHERE userPosts.uid = users.uid AND time > (DATE(NOW()) - INTERVAL 7 DAY) ) 
    AS postNumber 
    FROM users 
    WHERE uid NOT IN (SELECT flwdid FROM followers WHERE flwrid = %s)
    AND uid != %s
    ORDER BY postNumber DESC LIMIT %s"""
    cursor.execute(query, (currentUser, currentUser, number))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

  
  #CHECKING
  @exception_handling
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
  
  @exception_handling
  def checkPassword(self, uid, password):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE uid = %s"
    cursor.execute(query, (uid,) )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result != None:
      hashed_password = result["password"]
      if sha256_crypt.verify(password, hashed_password):
        return True
    return False

  @exception_handling
  def isThereThisUsername(self, username):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return (result != None)

  @exception_handling
  def isThereThisEmail(self, email):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return (result != None)
  
  @exception_handling
  def isEmailVerified(self, email):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE email = %s AND isEmailVerified = 1"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return (result != None)
  
  @exception_handling
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
  @exception_handling
  def updateFullname(self, uid, fullname):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE users SET full_name = %s WHERE uid = %s"
    cursor.execute(query, (fullname, uid))
    connection.commit()
    cursor.close()
    connection.close()
  
  @exception_handling
  def updateUsername(self, uid, username):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE users SET username = %s WHERE uid = %s"
    cursor.execute(query, (username, uid))
    connection.commit()
    cursor.close()
    connection.close()
  
  @exception_handling
  def updatePassword(self, uid, password):
    password = sha256_crypt.encrypt(password)
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE users SET password = %s WHERE uid = %s"
    cursor.execute(query, (password, uid))
    connection.commit()
    cursor.close()
    connection.close()
  
  @exception_handling
  def updateProfilePhoto(self, uid, photo):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE users SET photo = %s WHERE uid = %s"
    cursor.execute(query, (photo, uid))
    connection.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def updateEmail(self, uid, email):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE users SET email = %s, isEmailVerified = 0 WHERE uid = %s"
    cursor.execute(query, (email, uid))
    connection.commit()
    cursor.close()
    connection.close()
  
  @exception_handling
  def updateBio(self, uid, bio):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE users SET bio = %s WHERE uid = %s"
    cursor.execute(query, (bio, uid))
    connection.commit()
    cursor.close()
    connection.close()
  
  @exception_handling
  def verifyEmail(self, email):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE users SET isEmailVerified = 1 WHERE email = %s"
    cursor.execute(query, (email,) )
    connection.commit()
    cursor.close()
    connection.close()
  
  
  #FOLLOW ACTIONS
  @exception_handling
  def follow(self, followerId, followedId):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO followers(flwrid, flwdid) VALUES(%s, %s)"
    cursor.execute(query, (followerId, followedId))
    connection.commit()
    cursor.close()
    connection.close()
  
  @exception_handling
  def unFollow(self, followerId, followedId):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM followers WHERE flwrid = %s AND flwdid = %s"
    cursor.execute(query, (followerId, followedId))
    connection.commit()
    cursor.close()
    connection.close()


  #USER LINKS
  @exception_handling
  def getUserLinks(self, uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM userLinks WHERE uid = %s"
    cursor.execute(query, (uid,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result
  
  @exception_handling
  def getUserLink(self, ulid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM userLinks WHERE ulid = %s"
    cursor.execute(query, (ulid,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

  @exception_handling
  def addUserLink(self, uid, name, link):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO userLinks(uid, name, link) VALUES(%s, %s, %s)"
    cursor.execute(query, (uid, name, link))
    ulid = cursor.lastrowid
    connection.commit()
    cursor.close()
    connection.close()
    return ulid
  
  @exception_handling
  def removeUserLink(self, ulid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM userLinks WHERE ulid = %s"
    cursor.execute(query, (ulid,) )
    connection.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def updateUserLink(self, ulid, name, link):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE userLinks SET name = %s, link = %s WHERE ulid = %s"
    cursor.execute(query, (name, link, ulid) )
    connection.commit()
    cursor.close()
    connection.close()
  
  @exception_handling
  def searchUsers(self, keyword, number):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE full_name LIKE %s OR username LIKE %s LIMIT %s"
    result = cursor.execute(query, ("%" + keyword + "%", "%" + keyword + "%", number))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

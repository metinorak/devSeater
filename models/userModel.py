from models.database import *
from passlib.hash import sha256_crypt

class UserModel(Database):
  
  def getUser(self, uid, currentUser = None):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    
    try:
      query = """SELECT
      (SELECT COUNT(*) FROM followers WHERE flwrid = %s AND flwdid = users.uid) AS isFollowed,
      users.* FROM users WHERE uid = %s"""
      cursor.execute(query, (currentUser, uid) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result
  
  def getLastUsers(self, count):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    
    try:
      query = """SELECT * FROM users ORDER BY uid DESC LIMIT %s"""
      cursor.execute(query, (count, ) )
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  
  def getUserByUsername(self, username, currentUser = None):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM followers WHERE flwrid = %s AND flwdid = users.uid) AS isFollowed,
      users.* FROM users WHERE username = %s"""
      cursor.execute(query, (currentUser, username))
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  def getUserByEmail(self, email, currentUser = None):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM followers WHERE flwrid = %s AND flwdid = users.uid) AS isFollowed,
      users.* FROM users WHERE email = %s"""
      cursor.execute(query, (currentUser, email))
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  def addUser(self, user):
    user["password"] = sha256_crypt.encrypt(user["password"])
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "INSERT INTO users(email, username, password, full_name) VALUES(%s, %s, %s, %s)"
      cursor.execute(query, (user["email"], user["username"], user["password"], user["full_name"]) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()

  
  def removeUser(self, uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      cursor.execute(query, (uid,) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  def getWhoToFollowList(self, number, currentUser = None):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT users.*, 
      (SELECT COUNT(*) FROM userPosts WHERE userPosts.uid = users.uid AND time > (DATE(NOW()) - INTERVAL 7 DAY)) 
      AS postNumber,
      (SELECT COUNT(*) FROM userPostComments WHERE userPostComments.uid = users.uid AND time > (DATE(NOW()) - INTERVAL 7 DAY))
      AS postCommentNumber,
      (SELECT COUNT(*) FROM followers WHERE (followers.flwrid = users.uid OR followers.flwdid = users.uid) AND time > (DATE(NOW()) - INTERVAL 7 DAY))
      AS followNumber
      FROM users 
      WHERE uid NOT IN (SELECT flwdid FROM followers WHERE flwrid = %s)
      AND uid != %s
      ORDER BY (postNumber + postCommentNumber + followNumber) DESC, uid DESC LIMIT %s"""
      cursor.execute(query, (currentUser, currentUser, number))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  
  #CHECKING
  
  def login(self, email, password):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM users WHERE email = %s"
      cursor.execute(query, (email,) )
      result = cursor.fetchone()
      if result != None:
        hashed_password = result["password"]
        if sha256_crypt.verify(password, hashed_password):
          return True
      return False
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
  
  def checkPassword(self, uid, password):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM users WHERE uid = %s"
      cursor.execute(query, (uid,) )
      result = cursor.fetchone()
      if result != None:
        hashed_password = result["password"]
        if sha256_crypt.verify(password, hashed_password):
          return True
      return False
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()

  def isThereThisUsername(self, username):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM users WHERE username = %s"
      cursor.execute(query, (username,))
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return (result != None)

  def isThereThisEmail(self, email):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM users WHERE email = %s"
      cursor.execute(query, (email,))
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return (result != None)
  
  def isEmailVerified(self, email):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM users WHERE email = %s AND isEmailVerified = 1"
      cursor.execute(query, (email,))
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return (result != None)
  
  def isGlobalAdmin(self, uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM globalAdmins WHERE uid = %s"
      cursor.execute(query, (uid,))
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return (result != None)

  #UPDATE
  
  def updateFullname(self, uid, fullname):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "UPDATE users SET full_name = %s WHERE uid = %s"
      cursor.execute(query, (fullname, uid))
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  def updateUsername(self, uid, username):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "UPDATE users SET username = %s WHERE uid = %s"
      cursor.execute(query, (username, uid))
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  def updatePassword(self, uid, password):
    password = sha256_crypt.encrypt(password)
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "UPDATE users SET password = %s WHERE uid = %s"
      cursor.execute(query, (password, uid))
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  def updateProfilePhoto(self, uid, photo):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "UPDATE users SET photo = %s WHERE uid = %s"
      cursor.execute(query, (photo, uid))
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()

  def updateEmail(self, uid, email):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "UPDATE users SET email = %s, isEmailVerified = 0 WHERE uid = %s"
      cursor.execute(query, (email, uid))
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  def updateBio(self, uid, bio):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "UPDATE users SET bio = %s WHERE uid = %s"
      cursor.execute(query, (bio, uid))
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  def verifyEmail(self, email):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "UPDATE users SET isEmailVerified = 1 WHERE email = %s"
      cursor.execute(query, (email,) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  #FOLLOW ACTIONS
  
  def follow(self, followerId, followedId):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "INSERT INTO followers(flwrid, flwdid) VALUES(%s, %s)"
      cursor.execute(query, (followerId, followedId))
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  def unFollow(self, followerId, followedId):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "DELETE FROM followers WHERE flwrid = %s AND flwdid = %s"
      cursor.execute(query, (followerId, followedId))
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()

  #USER LINKS
  
  def getUserLinks(self, uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM userLinks WHERE uid = %s"
      cursor.execute(query, (uid,))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result
  
  def getUserLink(self, ulid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM userLinks WHERE ulid = %s"
      cursor.execute(query, (ulid,))
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  def addUserLink(self, uid, name, link):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "INSERT INTO userLinks(uid, name, link) VALUES(%s, %s, %s)"
      cursor.execute(query, (uid, name, link))
      ulid = cursor.lastrowid
      connection.commit()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return ulid
  
  def removeUserLink(self, ulid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "DELETE FROM userLinks WHERE ulid = %s"
      cursor.execute(query, (ulid,) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  def updateUserLink(self, ulid, name, link):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "UPDATE userLinks SET name = %s, link = %s WHERE ulid = %s"
      cursor.execute(query, (name, link, ulid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  def searchUsers(self, keyword, number):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM users WHERE full_name LIKE %s OR username LIKE %s LIMIT %s"
      result = cursor.execute(query, ("%" + keyword + "%", "%" + keyword + "%", number))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

from models.database import *

class UserPostModel(Database):
  
  def addUserPost(self, uid, post):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = "INSERT INTO userPosts(uid, post) VALUES(%s, %s)"
      cursor.execute(query, (uid, post) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
    
  def getUserPost(self, upid, currentUser = None):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM userPostLikes WHERE upid = userPosts.upid AND uid = %s) AS isLiked,
      (SELECT COUNT(*) FROM userPostLikes WHERE upid = userPosts.upid) AS likeNumber,
      (SELECT COUNT(*) FROM userPostComments WHERE upid = userPosts.upid) AS commentNumber,
      userPosts.* FROM userPosts WHERE upid = %s """
      cursor.execute(query, (currentUser, upid,) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  def getLastUserPosts(self, uid, number, currentUser = None):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM userPostLikes WHERE upid = userPosts.upid AND uid = %s) AS isLiked,
      (SELECT COUNT(*) FROM userPostLikes WHERE upid = userPosts.upid) AS likeNumber,
      (SELECT COUNT(*) FROM userPostComments WHERE upid = userPosts.upid) AS commentNumber,
      userPosts.*, users.full_name, users.photo, users.username 
      FROM userPosts INNER JOIN users ON users.uid = userPosts.uid  WHERE userPosts.uid = %s 
      ORDER BY time DESC LIMIT %s"""
      cursor.execute(query, (currentUser, uid, number))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  def getPreviousUserPosts(self, uid, upid, number, currentUser = None):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM userPostLikes WHERE upid = userPosts.upid AND uid = %s) AS isLiked,
      (SELECT COUNT(*) FROM userPostLikes WHERE upid = userPosts.upid) AS likeNumber,
      (SELECT COUNT(*) FROM userPostComments WHERE upid = userPosts.upid) AS commentNumber,
      userPosts.*, users.full_name, users.photo, users.username 
      FROM userPosts INNER JOIN users ON users.uid = userPosts.uid  WHERE userPosts.uid = %s AND upid < %s 
      ORDER BY time DESC LIMIT %s"""
      cursor.execute(query, (currentUser, uid, upid, number))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  def removeUserPost(self, upid):
    connection = self.getConnection()
    try:
    cursor = connection.cursor(dictionary=True)
      query = "DELETE FROM userPosts WHERE upid = %s"
      cursor.execute(query, (upid,) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  def updateUserPost(self, upid, post):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = "UPDATE userPosts SET post = %s WHERE upid = %s"
      cursor.execute(query, (post, upid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
    
  def getLastFollowingPosts(self, uid, number):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM userPostLikes WHERE upid = userPosts.upid AND uid = %s) AS isLiked,
      (SELECT COUNT(*) FROM userPostLikes WHERE upid = userPosts.upid) AS likeNumber,
      (SELECT COUNT(*) FROM userPostComments WHERE upid = userPosts.upid) AS commentNumber,
      userPosts.*, users.full_name, users.photo, users.username 
      FROM userPosts INNER JOIN users ON users.uid = userPosts.uid  WHERE userPosts.uid = %s OR
      userPosts.uid IN (SELECT flwdid FROM followers WHERE flwrid = %s) ORDER BY time DESC LIMIT %s"""
      cursor.execute(query, (uid, uid, uid, number))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  def getNewFollowingPosts(self, uid, upid):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM userPostLikes WHERE upid = userPosts.upid AND uid = %s) AS isLiked,
      (SELECT COUNT(*) FROM userPostLikes WHERE upid = userPosts.upid) AS likeNumber,
      (SELECT COUNT(*) FROM userPostComments WHERE upid = userPosts.upid) AS commentNumber,
      userPosts.*, users.full_name, users.photo, users.username 
      FROM userPosts INNER JOIN users ON users.uid = userPosts.uid  WHERE (userPosts.uid = %s OR
      userPosts.uid IN (SELECT flwdid FROM followers WHERE flwrid = %s)) AND upid > %s 
      ORDER BY time ASC"""
      cursor.execute(query, (uid, uid, uid, upid))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result
  
  def getNewFollowingPostNumber(self, uid, upid):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT * FROM userPosts 
      WHERE (uid = %s OR uid IN (SELECT flwdid FROM followers WHERE flwrid = %s)) AND upid > %s"""
      cursor.execute(query, (uid, uid, upid))
      result = cursor.fetchall()
      count = cursor.rowcount
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return count

  def getPreviousFollowingPosts(self, uid, upid, number):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)

    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM userPostLikes WHERE upid = userPosts.upid AND uid = %s) AS isLiked,
      (SELECT COUNT(*) FROM userPostLikes WHERE upid = userPosts.upid) AS likeNumber,
      (SELECT COUNT(*) FROM userPostComments WHERE upid = userPosts.upid) AS commentNumber,
      userPosts.*, users.full_name, users.photo, users.username 
      FROM userPosts INNER JOIN users ON users.uid = userPosts.uid  WHERE (userPosts.uid = %s OR
      userPosts.uid IN (SELECT flwdid FROM followers WHERE flwrid = %s)) AND upid < %s 
      ORDER BY time DESC LIMIT %s"""
      cursor.execute(query, (uid, uid, uid, upid, number))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  def likeUserPost(self, uid, upid):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = "INSERT INTO userPostLikes(uid, upid) VALUES(%s, %s)"
      cursor.execute(query, (uid, upid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  def unlikeUserPost(self, uid, upid):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = "DELETE FROM userPostLikes WHERE uid = %s AND upid = %s"
      cursor.execute(query, (uid, upid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()

  def getUserPostLikeNumber(self, upid):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT COUNT(*) AS number FROM userPostLikes WHERE upid = %s"
      cursor.execute(query, (upid,) )
      result = cursor.fetchone()["number"]
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  def getUserPostCommentNumber(self, upid):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT COUNT(*) AS number FROM userPostComments WHERE upid = %s"
      cursor.execute(query, (upid,) )
      result = cursor.fetchone()["number"]
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  def isPostLiked(self,uid, upid):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM userPostLikes WHERE uid = %s AND upid = %s"
      cursor.execute(query, (uid, upid))
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return (result != None)

  #COMMENT OPERATIONS
  
  def addUserPostComment(self, uid, upid, comment):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = "INSERT INTO userPostComments(uid, upid, comment) VALUES(%s, %s, %s)"
      cursor.execute(query, (uid, upid, comment) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  def getUserPostComment(self, upcid, currentUser = None):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM userPostCommentLikes WHERE upcid = userPostComments.upcid AND uid = %s) AS isLiked, 
      (SELECT COUNT(*) FROM userPostCommentLikes WHERE upcid = userPostComments.upcid) AS likeNumber,
      userPostComments.*, users.username, users.full_name, users.photo
      FROM userPostComments 
      INNER JOIN users ON users.uid = userPostComments.uid
      WHERE upcid = %s"""
      cursor.execute(query, (currentUser, upcid,) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  def removeUserPostComment(self, upcid):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = "DELETE FROM userPostComments WHERE upcid = %s"
      cursor.execute(query, (upcid,) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()

  def updateUserPostComment(self, upcid, comment):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = "UPDATE userPostComments SET comment = %s WHERE upcid = %s"
      cursor.execute(query, (comment, upcid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()

  def getLastUserPostComments(self, upid, number, currentUser = None):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM userPostCommentLikes WHERE upcid = userPostComments.upcid AND uid = %s) AS isLiked, 
      (SELECT COUNT(*) FROM userPostCommentLikes WHERE upcid = userPostComments.upcid) AS likeNumber,
      userPostComments.*, users.username, users.full_name, users.photo
      FROM userPostComments 
      INNER JOIN users ON users.uid = userPostComments.uid
      WHERE upid = %s ORDER BY time DESC LIMIT %s"""
      cursor.execute(query, (currentUser, upid, number))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result
  
  def getPreviousUserPostComments(self, upid, upcid, number, currentUser = None):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM userPostCommentLikes WHERE upcid = userPostComments.upcid AND uid = %s) AS isLiked, 
      (SELECT COUNT(*) FROM userPostCommentLikes WHERE upcid = userPostComments.upcid) AS likeNumber,
      userPostComments.*, users.username, users.full_name, users.photo
      FROM userPostComments 
      INNER JOIN users ON users.uid = userPostComments.uid
      WHERE upid = %s AND upcid < %s ORDER BY time DESC LIMIT %s"""
      cursor.execute(query, (currentUser, upid, upcid, number))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  def getLastUserPostComment(self, upid, currentUser = None):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM userPostCommentLikes WHERE upcid = userPostComments.upcid AND uid = %s) AS isLiked, 
      (SELECT COUNT(*) FROM userPostCommentLikes WHERE upcid = userPostComments.upcid) AS likeNumber, 
      userPostComments.*, users.username, users.full_name, users.photo
      FROM userPostComments 
      INNER JOIN users ON users.uid = userPostComments.uid
      WHERE upid = %s ORDER BY time DESC LIMIT 1"""
      cursor.execute(query, (currentUser, upid) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  def likeUserPostComment(self, uid, upcid):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = "INSERT INTO userPostCommentLikes(uid, upcid) VALUES(%s, %s)"
      cursor.execute(query, (uid, upcid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  def unlikeUserPostComment(self, uid, upcid):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = "DELETE FROM userPostCommentLikes WHERE uid = %s AND upcid = %s"
      cursor.execute(query, (uid, upcid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()

  def getUserPostCommentLikeNumber(self, upcid):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT COUNT(*) AS number FROM userPostCommentLikes WHERE upcid = %s"
      cursor.execute(query, (upcid,) )
      result = cursor.fetchone()["number"]
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result
  
  def isCommentLiked(self, uid, upcid):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM userPostCommentLikes WHERE uid = %s AND upcid = %s"
      cursor.execute(query, (uid, upcid))
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return (result != None)
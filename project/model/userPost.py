from project.lib.database import Database

class UserPostModel():
  
  @staticmethod
  def addUserPost(uid, post):
    connection = Database.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = "INSERT INTO userPosts(uid, post) VALUES(%s, %s)"
      cursor.execute(query, (uid, post) )
      upid = cursor.lastrowid
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
    return upid
    
  @staticmethod
  def getUserPost(upid, currentUserId = None):
    connection = Database.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM userPostLikes WHERE upid = userPosts.upid AND uid = %s) AS isLiked,
      (SELECT COUNT(*) FROM userPostLikes WHERE upid = userPosts.upid) AS likeNumber,
      (SELECT COUNT(*) FROM userPostComments WHERE upid = userPosts.upid) AS commentNumber,
      userPosts.* FROM userPosts WHERE upid = %s """
      cursor.execute(query, (currentUserId, upid,) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  @staticmethod
  def getLastUserPosts(uid, number, currentUserId = None):
    connection = Database.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM userPostLikes WHERE upid = userPosts.upid AND uid = %s) AS isLiked,
      (SELECT COUNT(*) FROM userPostLikes WHERE upid = userPosts.upid) AS likeNumber,
      (SELECT COUNT(*) FROM userPostComments WHERE upid = userPosts.upid) AS commentNumber,
      userPosts.*, users.full_name, users.photo, users.username 
      FROM userPosts INNER JOIN users ON users.uid = userPosts.uid  WHERE userPosts.uid = %s 
      ORDER BY time DESC LIMIT %s"""
      cursor.execute(query, (currentUserId, uid, number))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  @staticmethod
  def getPreviousUserPosts(uid, upid, number, currentUserId = None):
    connection = Database.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM userPostLikes WHERE upid = userPosts.upid AND uid = %s) AS isLiked,
      (SELECT COUNT(*) FROM userPostLikes WHERE upid = userPosts.upid) AS likeNumber,
      (SELECT COUNT(*) FROM userPostComments WHERE upid = userPosts.upid) AS commentNumber,
      userPosts.*, users.full_name, users.photo, users.username 
      FROM userPosts INNER JOIN users ON users.uid = userPosts.uid  WHERE userPosts.uid = %s AND upid < %s 
      ORDER BY time DESC LIMIT %s"""
      cursor.execute(query, (currentUserId, uid, upid, number))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  @staticmethod
  def removeUserPost(upid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "DELETE FROM userPosts WHERE upid = %s"
      cursor.execute(query, (upid,) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  @staticmethod
  def updateUserPost(upid, post):
    connection = Database.getConnection() 
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
    
  @staticmethod
  def getLastFollowingPosts(uid, number):
    connection = Database.getConnection() 
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

  @staticmethod
  def getNewFollowingPosts(uid, upid):
    connection = Database.getConnection() 
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
  
  @staticmethod
  def getNewFollowingPostNumber(uid, upid):
    connection = Database.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT * FROM userPosts 
      WHERE (uid = %s OR uid IN (SELECT flwdid FROM followers WHERE flwrid = %s)) AND upid > %s"""
      cursor.execute(query, (uid, uid, upid))
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
  def getPreviousFollowingPosts(uid, upid, number):
    connection = Database.getConnection() 
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

  @staticmethod
  def likeUserPost(uid, upid):
    connection = Database.getConnection() 
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
  
  @staticmethod
  def unlikeUserPost(uid, upid):
    connection = Database.getConnection() 
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

  @staticmethod
  def getUserPostLikeNumber(upid):
    connection = Database.getConnection() 
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

  @staticmethod
  def getUserPostCommentNumber(upid):
    connection = Database.getConnection() 
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

  @staticmethod
  def isPostLiked(self,uid, upid):
    connection = Database.getConnection() 
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
  
  @staticmethod
  def addUserPostComment(uid, upid, comment):
    connection = Database.getConnection() 
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
  
  @staticmethod
  def getUserPostComment(upcid, currentUserId = None):
    connection = Database.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM userPostCommentLikes WHERE upcid = userPostComments.upcid AND uid = %s) AS isLiked, 
      (SELECT COUNT(*) FROM userPostCommentLikes WHERE upcid = userPostComments.upcid) AS likeNumber,
      userPostComments.*, users.username, users.full_name, users.photo
      FROM userPostComments 
      INNER JOIN users ON users.uid = userPostComments.uid
      WHERE upcid = %s"""
      cursor.execute(query, (currentUserId, upcid,) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  @staticmethod
  def removeUserPostComment(upcid):
    connection = Database.getConnection() 
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

  @staticmethod
  def updateUserPostComment(upcid, comment):
    connection = Database.getConnection() 
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

  @staticmethod
  def getLastUserPostComments(upid, number, currentUserId = None):
    connection = Database.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM userPostCommentLikes WHERE upcid = userPostComments.upcid AND uid = %s) AS isLiked, 
      (SELECT COUNT(*) FROM userPostCommentLikes WHERE upcid = userPostComments.upcid) AS likeNumber,
      userPostComments.*, users.username, users.full_name, users.photo
      FROM userPostComments 
      INNER JOIN users ON users.uid = userPostComments.uid
      WHERE upid = %s ORDER BY time DESC LIMIT %s"""
      cursor.execute(query, (currentUserId, upid, number))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result
  
  @staticmethod
  def getPreviousUserPostComments(upid, upcid, number, currentUserId = None):
    connection = Database.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM userPostCommentLikes WHERE upcid = userPostComments.upcid AND uid = %s) AS isLiked, 
      (SELECT COUNT(*) FROM userPostCommentLikes WHERE upcid = userPostComments.upcid) AS likeNumber,
      userPostComments.*, users.username, users.full_name, users.photo
      FROM userPostComments 
      INNER JOIN users ON users.uid = userPostComments.uid
      WHERE upid = %s AND upcid < %s ORDER BY time DESC LIMIT %s"""
      cursor.execute(query, (currentUserId, upid, upcid, number))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  @staticmethod
  def getLastUserPostComment(upid, currentUserId = None):
    connection = Database.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM userPostCommentLikes WHERE upcid = userPostComments.upcid AND uid = %s) AS isLiked, 
      (SELECT COUNT(*) FROM userPostCommentLikes WHERE upcid = userPostComments.upcid) AS likeNumber, 
      userPostComments.*, users.username, users.full_name, users.photo
      FROM userPostComments 
      INNER JOIN users ON users.uid = userPostComments.uid
      WHERE upid = %s ORDER BY time DESC LIMIT 1"""
      cursor.execute(query, (currentUserId, upid) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  @staticmethod
  def likeUserPostComment(uid, upcid):
    connection = Database.getConnection() 
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
  
  @staticmethod
  def unlikeUserPostComment(uid, upcid):
    connection = Database.getConnection() 
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

  @staticmethod
  def getUserPostCommentLikeNumber(upcid):
    connection = Database.getConnection() 
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
  
  @staticmethod
  def isCommentLiked(uid, upcid):
    connection = Database.getConnection() 
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
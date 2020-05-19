from project.lib.database import Database

class ProjectPostModel():
  
  @staticmethod
  def addProjectPost(uid, pid, post):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "INSERT INTO projectPosts(uid, pid, post) VALUES(%s, %s, %s)"
      cursor.execute(query, (uid, pid, post) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  @staticmethod
  def getProjectPost(ppid, currentUserId):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM projectPostLikes WHERE ppid = projectPosts.ppid AND uid = %s) AS isLiked, 
      (SELECT COUNT(*) FROM projectPostLikes WHERE ppid = projectPosts.ppid) AS likeNumber,
      (SELECT COUNT(*) FROM projectPostComments WHERE ppid = projectPosts.ppid) AS commentNumber, 
      projectPosts.* FROM projectPosts 
      INNER JOIN users ON users.uid = projectPosts.uid
      WHERE ppid = %s"""
      cursor.execute(query, (currentUserId, ppid) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  @staticmethod
  def getLastProjectPosts(pid, number, currentUserId):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM projectPostLikes WHERE ppid = projectPosts.ppid AND uid = %s) AS isLiked,
      (SELECT COUNT(*) FROM projectPostLikes WHERE ppid = projectPosts.ppid) AS likeNumber,
      (SELECT COUNT(*) FROM projectPostComments WHERE ppid = projectPosts.ppid) AS commentNumber,
      projectPosts.*, users.full_name, users.photo, users.username 
      FROM projectPosts INNER JOIN users ON users.uid = projectPosts.uid  WHERE projectPosts.pid = %s 
      ORDER BY time DESC LIMIT %s"""
      cursor.execute(query, (currentUserId, pid, number))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  @staticmethod
  def getPreviousProjectPosts(pid, ppid, number, currentUserId):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)

    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM projectPostLikes WHERE ppid = projectPosts.ppid AND uid = %s) AS isLiked,
      (SELECT COUNT(*) FROM projectPostLikes WHERE ppid = projectPosts.ppid) AS likeNumber,
      (SELECT COUNT(*) FROM projectPostComments WHERE ppid = projectPosts.ppid) AS commentNumber,
      projectPosts.*, users.photo, users.full_name, users.username 
      FROM projectPosts 
      INNER JOIN users ON users.uid = projectPosts.uid
      WHERE pid = %s AND ppid < %s ORDER BY time DESC LIMIT %s"""
      cursor.execute(query, (currentUserId, pid, ppid, number))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  @staticmethod
  def removeProjectPost(ppid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "DELETE FROM projectPosts WHERE ppid = %s"
      cursor.execute(query, (ppid,) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  @staticmethod
  def updateProjectPost(ppid, post):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "UPDATE projectPosts SET post = %s WHERE ppid = %s"
      cursor.execute(query, (post, ppid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()

  @staticmethod
  def likeProjectPost(uid, ppid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "INSERT INTO projectPostLikes(uid, ppid) VALUES(%s, %s)"
      cursor.execute(query, (uid, ppid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  @staticmethod
  def unlikeProjectPost(uid, ppid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "DELETE FROM projectPostLikes WHERE uid = %s AND ppid = %s"
      cursor.execute(query, (uid, ppid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()

  @staticmethod
  def getProjectPostLikeNumber(ppid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT COUNT(*) AS number FROM projectPostLikes WHERE ppid = %s"
      cursor.execute(query, (ppid,) )
      result = cursor.fetchone()["number"]
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  @staticmethod
  def getProjectPostCommentNumber(ppid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT COUNT(*) AS number FROM projectPostComments WHERE ppid = %s"
      cursor.execute(query, (ppid,) )
      result = cursor.fetchone()["number"]
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
    return result

  @staticmethod
  def isPostLiked(uid, ppid):
    connection = Database.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM projectPostCommentLikes WHERE uid = %s AND ppid = %s"
      cursor.execute(query, (uid, ppid))
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
  def addProjectPostComment(uid, ppid, comment):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "INSERT INTO projectPostComments(uid, ppid, comment) VALUES(%s, %s, %s)"
      cursor.execute(query, (uid, ppid, comment) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()

  @staticmethod
  def removeProjectPostComment(ppcid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "DELETE FROM projectPostComments WHERE ppcid = %s"
      cursor.execute(query, (ppcid,) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()

  @staticmethod
  def updateProjectPostComment(ppcid, comment):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "UPDATE projectPostComments SET comment = %s WHERE ppcid = %s"
      cursor.execute(query, (comment, ppcid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()

  @staticmethod
  def getProjectPostComment(ppcid, currentUserId):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM projectPostCommentLikes WHERE ppcid = PPC.ppcid AND uid = %s) AS isLiked,
      (SELECT COUNT(*) FROM projectPostCommentLikes WHERE ppcid = PPC.ppcid) AS likeNumber,
      PPC.*, users.username, users.full_name, users.photo
      FROM projectPostComments PPC 
      INNER JOIN users ON users.uid = PPC.uid 
      WHERE ppcid = %s"""
      cursor.execute(query, (currentUserId, ppcid) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
    return result
  
  @staticmethod
  def getLastProjectPostComments(ppid, number, currentUserId):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM projectPostCommentLikes WHERE ppcid = PPC.ppcid AND uid = %s) AS isLiked,
      (SELECT COUNT(*) FROM projectPostCommentLikes WHERE ppcid = PPC.ppcid) AS likeNumber,
      PPC.*, users.username, users.full_name, users.photo
      FROM projectPostComments PPC 
      INNER JOIN users ON users.uid = PPC.uid 
      WHERE ppid = %s ORDER BY time DESC LIMIT %s"""
      cursor.execute(query, (currentUserId, ppid, number))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result
  
  @staticmethod
  def getPreviousProjectPostComments(ppid, ppcid, number, currentUserId):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """SELECT 
      (SELECT COUNT(*) FROM projectPostCommentLikes WHERE ppcid = PPC.ppcid AND uid = %s) AS isLiked,
      (SELECT COUNT(*) FROM projectPostCommentLikes WHERE ppcid = PPC.ppcid) AS likeNumber,
      PPC.*, users.username, users.full_name, users.photo
      FROM projectPostComments PPC 
      INNER JOIN users ON users.uid = PPC.uid 
      WHERE ppid = %s AND ppcid < %s ORDER BY time DESC LIMIT %s"""
      cursor.execute(query, (currentUserId, ppid, ppcid, number))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  @staticmethod
  def likeProjectPostComment(uid, ppcid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "INSERT INTO projectPostCommentLikes(uid, ppcid) VALUES(%s, %s)"
      cursor.execute(query, (uid, ppcid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
  
  @staticmethod
  def unlikeProjectPostComment(uid, ppcid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "DELETE FROM projectPostCommentLikes WHERE uid = %s AND ppcid = %s"
      cursor.execute(query, (uid, ppcid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()

  @staticmethod
  def getProjectPostCommentLikeNumber(ppcid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT COUNT(*) AS number FROM projectPostCommentLikes WHERE ppcid = %s"
      cursor.execute(query, (ppcid,) )
      result = cursor.fetchone()["number"]
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  @staticmethod
  def isCommentLiked(uid, ppcid):
    connection = Database.getConnection() 
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM projectPostCommentLikes WHERE uid = %s AND ppcid = %s"
      cursor.execute(query, (uid, ppcid))
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return (result != None)
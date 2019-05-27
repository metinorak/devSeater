from models.database import *

class ProjectPostModel(Database):
  @exception_handling
  def addProjectPost(self, uid, pid, post):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO projectPosts(uid, pid, post) VALUES(%s, %s, %s)"
    cursor.execute(query, (uid, pid, post) )
    connection.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def getProjectPost(self, ppid, currentUser):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT 
    (SELECT COUNT(*) FROM projectPostLikes WHERE ppid = projectPosts.ppid AND uid = %s) AS isLiked, 
    (SELECT COUNT(*) FROM projectPostLikes WHERE ppid = projectPosts.ppid) AS likeNumber,
    (SELECT COUNT(*) FROM projectPostComments WHERE ppid = projectPosts.ppid) AS commentNumber, 
    projectPosts.* FROM projectPosts 
    INNER JOIN users ON users.uid = projectPosts.uid
    WHERE ppid = %s"""
    cursor.execute(query, (currentUser, ppid) )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

  @exception_handling
  def getLastProjectPosts(self, pid, number, currentUser):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT 
    (SELECT COUNT(*) FROM projectPostLikes WHERE ppid = projectPosts.ppid AND uid = %s) AS isLiked,
    (SELECT COUNT(*) FROM projectPostLikes WHERE ppid = projectPosts.ppid) AS likeNumber,
    (SELECT COUNT(*) FROM projectPostComments WHERE ppid = projectPosts.ppid) AS commentNumber,
    projectPosts.*, users.full_name, users.photo, users.username 
    FROM projectPosts INNER JOIN users ON users.uid = projectPosts.uid  WHERE projectPosts.pid = %s 
    ORDER BY time DESC LIMIT %s"""
    cursor.execute(query, (currentUser, pid, number))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

  @exception_handling
  def getPreviousProjectPosts(self, pid, ppid, number, currentUser):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT 
    (SELECT COUNT(*) FROM projectPostCommentLikes WHERE ppid = projectPosts.ppid AND uid = %s) AS isLiked, 
    (SELECT COUNT(*) FROM projectPostLikes WHERE ppid = projectPosts.ppid) AS likeNumber,
    (SELECT COUNT(*) FROM projectPostComments WHERE ppid = projectPosts.ppid AND uid = %s) AS commentNumber,
    projectPosts.* FROM projectPosts 
    INNER JOIN users ON users.uid = projectPosts.uid
    WHERE pid = %s AND ppid < %s ORDER BY time DESC LIMIT %s"""
    cursor.execute(query, (currentUser, pid, ppid, number))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

  @exception_handling
  def removeProjectPost(self, ppid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM projectPosts WHERE ppid = %s"
    cursor.execute(query, (ppid,) )
    connection.commit()
    cursor.close()
    connection.close()
  
  @exception_handling
  def updateProjectPost(self, ppid, post):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE projectPosts SET post = %s WHERE ppid = %s"
    cursor.execute(query, (post, ppid) )
    connection.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def likeProjectPost(self, uid, ppid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO projectPostLikes(uid, ppid) VALUES(%s, %s)"
    cursor.execute(query, (uid, ppid) )
    connection.commit()
    cursor.close()
    connection.close()
  
  @exception_handling
  def unlikeProjectPost(self, uid, ppid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM projectPostLikes WHERE uid = %s AND ppid = %s"
    cursor.execute(query, (uid, ppid) )
    connection.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def getProjectPostLikeNumber(self, ppid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT COUNT(*) AS number FROM projectPostLikes WHERE ppid = %s"
    cursor.execute(query, (ppid,) )
    result = cursor.fetchone()["number"]
    cursor.close()
    connection.close()
    return result

  @exception_handling
  def getProjectPostCommentNumber(self, ppid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT COUNT(*) AS number FROM projectPostComments WHERE ppid = %s"
    cursor.execute(query, (ppid,) )
    result = cursor.fetchone()["number"]
    cursor.close()
    connection.close()
    return result

  @exception_handling
  def isPostLiked(uid, ppid):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM projectPostCommentLikes WHERE uid = %s AND ppid = %s"
    cursor.execute(query, (uid, ppid))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return (result != None)
  

  #COMMENT OPERATIONS
  @exception_handling
  def addProjectPostComment(self, uid, ppid, comment):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO projectPostComments(uid, ppid, comment) VALUES(%s, %s, %s)"
    cursor.execute(query, (uid, ppid, comment) )
    connection.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def removeProjectPostComment(self, ppcid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM projectPostComments WHERE ppcid = %s"
    cursor.execute(query, (ppcid,) )
    connection.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def updateProjectPostComment(self, ppcid, comment):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE projectPostComments SET comment = %s WHERE ppcid = %s"
    cursor.execute(query, (comment, ppcid) )
    connection.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def getProjectPostComment(self, ppcid, currentUser):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT 
    (SELECT COUNT(*) FROM projectPostCommentLikes WHERE ppcid = PPC.ppcid AND uid = %s) AS isLiked,
    (SELECT COUNT(*) FROM projectPostCommentLikes WHERE ppcid = PPC.ppcid) AS likeNumber,
    PPC.* 
    FROM projectPostComments PPC
    INNER JOIN users ON users.uid = PPC.uid
    WHERE ppcid = %s"""
    cursor.execute(query, (currentUser, ppcid) )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

  @exception_handling
  def getLastProjectPostComments(self, ppid, number, currentUser):

    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT 
    (SELECT COUNT(*) FROM projectPostCommentLikes WHERE ppcid = PPC.ppcid AND uid = %s) AS isLiked,
    (SELECT COUNT(*) FROM projectPostCommentLikes WHERE ppcid = PPC.ppcid) AS likeNumber,
    PPC.*, users.username, users.full_name 
    FROM projectPostComments PPC 
    INNER JOIN users ON users.uid = PPC.uid 
    WHERE ppid = %s ORDER BY time DESC LIMIT %s"""
    cursor.execute(query, (currentUser, ppid, number))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result
  
  @exception_handling
  def getPreviousProjectPostComments(self, ppid, ppcid, number, currentUser):

    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT 
    (SELECT COUNT(*) FROM projectPostCommentLikes WHERE ppcid = PPC.ppcid AND uid = %s) AS isLiked,
    (SELECT COUNT(*) FROM projectPostCommentLikes WHERE ppcid = PPC.ppcid) AS likeNumber,
    PPC.*, users.username, users.full_name 
    FROM projectPostComments PPC 
    INNER JOIN users ON users.uid = PPC.uid 
    WHERE ppid = %s AND ppcid < %s ORDER BY time DESC LIMIT %s"""
    cursor.execute(query, (currentUser, ppid, ppcid, number))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

  @exception_handling
  def likeProjectPostComment(self, uid, ppcid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO projectPostCommentLikes(uid, ppcid) VALUES(%s, %s)"
    cursor.execute(query, (uid, ppcid) )
    connection.commit()
    cursor.close()
    connection.close()
  
  @exception_handling
  def unlikeProjectPostComment(self, uid, ppcid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM projectPostCommentLikes WHERE uid = %s AND ppcid = %s"
    cursor.execute(query, (uid, ppcid) )
    connection.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def getProjectPostCommentLikeNumber(self, ppid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT COUNT(*) AS number FROM projectPostCommentLikes WHERE ppcid = %s"
    cursor.execute(query, (ppcid,) )
    result = cursor.fetchone["number"]
    cursor.close()
    connection.close()
    return result

  @exception_handling
  def isCommentLiked(uid, ppcid):
    connection = self.getConnection() 
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM projectPostCommentLikes WHERE uid = %s AND ppcid = %s"
    cursor.execute(query, (uid, ppcid))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return (result != None)

  
from models.database import *

class MessageModel(Database):
  @exception_handling
  def sendMessage(self, senderId, receiverId, message):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO messages(sender_id, receiver_id, message) VALUES(%s, %s, %s)"
    cursor.execute(query, (senderId, receiverId, message) )
    mid = cursor.lastrowid
    connection.commit()
    cursor.close()
    connection.close()
    return mid
  
  @exception_handling
  def isTheUserMessageOwner(self, uid, mid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM messages WHERE mid = %s AND (receiver_id = %s OR sender_id = %s)"
    cursor.execute(query, (mid, uid, uid) )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return (result != None)
  
  @exception_handling
  def deleteMessage(self, uid, mid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)

    #Delete by receiver if the user is receiver
    query = "UPDATE messages SET isDeletedByReceiver = 1 WHERE receiver_id = %s AND mid = %s"
    cursor.execute(query, (uid, mid) )

    #Delete by sender if the user is sender
    query = "UPDATE messages SET isDeletedBySender = 1 WHERE sender_id = %s AND mid = %s"
    cursor.execute(query, (uid, mid) )

    connection.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def getNewMessageNumberInDialog(self, current_uid, other_uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT COUNT(*) AS number FROM messages WHERE receiver_id = %s AND sender_id = %s AND isRead = 0"
    cursor.execute(query, (current_uid, other_uid) )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result["number"]
  
  @exception_handling
  def getNewMessageDialogNumber(self, uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM messages WHERE receiver_id = %s AND isRead = 0 AND isDeletedByReceiver = 0 GROUP BY sender_id"
    cursor.execute(query, (uid,) )
    cursor.fetchall()
    count = cursor.rowcount
    cursor.close()
    connection.close()
    return count
  
  @exception_handling
  def getDialogList(self, uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT U.*, M.isRead=1 FROM 
    (SELECT sender_id AS uid, mid, isRead FROM messages WHERE receiver_id = %s AND isDeletedByReceiver = 0
    UNION
    SELECT receiver_id AS uid, mid, isRead FROM messages WHERE sender_id = %s AND isDeletedBySender = 0) M, users U
    WHERE U.uid = M.uid
    GROUP BY M.uid ORDER BY M.mid DESC
    """
    cursor.execute(query, (uid, uid) )
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result
  
  @exception_handling
  def getDialogLastMessages(self, current_uid, other_uid, number):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT * FROM messages WHERE
    (
      (receiver_id = %s AND sender_id = %s AND isDeletedByReceiver = 0)
      OR 
      (receiver_id = %s AND sender_id = %s AND isDeletedBySender = 0) 
    ) 
    ORDER BY mid DESC LIMIT %s"""
    cursor.execute(query, (current_uid, other_uid, other_uid, current_uid, number))
    result = cursor.fetchall()

    #Marks as read
    query = """
    UPDATE messages SET isRead = 1
    WHERE
    receiver_id = %s AND sender_id = %s 
    AND isDeletedByReceiver = 0"""
    cursor.execute(query, (current_uid, other_uid))
    connection.commit()

    cursor.close()
    connection.close()
    return result

  @exception_handling
  def getDialogPreviousMessages(self, current_uid, other_uid, mid, number):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT * FROM messages WHERE
    ((receiver_id = %s AND sender_id = %s AND isDeletedByReceiver = 0)
    OR
    (receiver_id = %s AND sender_id = %s AND isDeletedBySender = 0) ) 
    AND mid < %s
    ORDER BY mid DESC LIMIT %s"""

    cursor.execute(query, (current_uid, other_uid, other_uid, current_uid, mid, number))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

  @exception_handling
  def deleteDialog(self, current_uid, other_uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)

    #Delete by receiver if the user is receiver
    query = "UPDATE messages SET isDeletedByReceiver = 1 WHERE receiver_id = %s AND sender_id = %s"
    cursor.execute(query, (current_uid, other_uid) )

    #Delete by sender if the user is sender
    query = "UPDATE messages SET isDeletedBySender = 1 WHERE sender_id = %s AND receiver_id = %s"
    cursor.execute(query, (current_uid, other_uid) )

    connection.commit()
    cursor.close()
    connection.close()
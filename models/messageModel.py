from models.database import *

class MessageModel(Database):
  @exception_handling
  def sendMessage(self, senderId, receiverId, message):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO messages(sender_id, receiver_id, message) VALUES(%s, %s, %s)"
    cursor.execute(query, (senderId, receiverId, message) )
    self.commit()
    cursor.close()
    connection.close()
  
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

    self.commit()
    cursor.close()
    connection.close()

  @exception_handling
  def getNewMessageNumberInDialog(self, receiver_id, sender_id):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT COUNT(*) AS number FROM messages WHERE receiver_id = %s AND sender_id = %s AND isRead = 0"
    cursor.execute(query, (receiver_id, sender_id) )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result["number"]
  
  @exception_handling
  def getNewMessageDialogNumber(self, uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM messages WHERE receiver_id = %s AND isRead = 0 GROUP BY sender_id"
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
    query = """SELECT * FROM users WHERE uid IN(
    (SELECT sender_id AS uid FROM messages WHERE receiver_id = %s AND isDeletedByReceiver = 0 )
    UNION
    (SELECT receiver_id AS uid FROM messages WHERE sender_id = %s AND isDeletedBySender = 0) ORDER BY time DESC LIMIT 1)
    """
    cursor.execute(query, (uid, uid) )
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result
  
  @exception_handling
  def getDialog(self, current_uid, other_uid, page, messageNumberPerPage):
    previousMessageNumber = (page - 1) * messageNumberPerPage

    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM messages WHERE receiver_id = %s AND isDeletedByReceiver = 0 ORDER BY time DESC LIMIT %s,%s"
    cursor.execute(query, (pid, previousMessageNumber, messageNumberPerPage))
    result = cursor.fetchall()

    #Marks as read
    query = """UPDATE messages SET isRead = 1 WHERE mid IN 
    (SELECT mid FROM messages WHERE receiver_id = %s AND isDeletedByReceiver = 0 ORDER BY time DESC LIMIT %s,%s)"""
    cursor.execute(query, (current_uid, previousMessageNumber, messageNumberPerPage))  
    self.commit()

    cursor.close()
    connection.close()
    return result
  
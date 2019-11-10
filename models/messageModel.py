from models.database import Database

class MessageModel(Database):

  def sendMessage(self, senderId, receiverId, message):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "INSERT INTO messages(sender_id, receiver_id, message) VALUES(%s, %s, %s)"
      cursor.execute(query, (senderId, receiverId, message) )
      mid = cursor.lastrowid
      connection.commit()
    except Exception as e:
      print(e)
      return
    finally:
      cursor.close()
      connection.close()
    return mid
  
  def isTheUserMessageOwner(self, uid, mid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM messages WHERE mid = %s AND (receiver_id = %s OR sender_id = %s)"
      cursor.execute(query, (mid, uid, uid) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return
    finally:
      cursor.close()
      connection.close()
    return (result != None)
  
  def deleteMessage(self, uid, mid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
  
    try:
      #Delete by receiver if the user is receiver
      query = "UPDATE messages SET isDeletedByReceiver = 1 WHERE receiver_id = %s AND mid = %s"
      cursor.execute(query, (uid, mid) )

      #Delete by sender if the user is sender
      query = "UPDATE messages SET isDeletedBySender = 1 WHERE sender_id = %s AND mid = %s"
      cursor.execute(query, (uid, mid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()


  def getNewMessageNumberInDialog(self, current_uid, other_uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT COUNT(*) AS number FROM messages WHERE receiver_id = %s AND sender_id = %s AND isRead = 0"
      cursor.execute(query, (current_uid, other_uid) )
      result = cursor.fetchone()
    except Exception as e:
      print(e)
      return
    finally:
      cursor.close()
      connection.close()
    return result["number"]
  

  def getNewMessageDialogNumber(self, uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM messages WHERE receiver_id = %s AND isRead = 0 AND isDeletedByReceiver = 0 GROUP BY sender_id"
      cursor.execute(query, (uid,) )
      cursor.fetchall()
      count = cursor.rowcount
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return count
  

  def getDialogList(self, uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """
      SELECT U.* FROM 
      (SELECT sender_id AS uid, time FROM messages WHERE receiver_id = %s AND isDeletedByReceiver = 0
      UNION
      SELECT receiver_id AS uid, time FROM messages WHERE sender_id = %s AND isDeletedBySender = 0) M, users U
      WHERE U.uid = M.uid
      GROUP BY M.uid ORDER BY M.time DESC
      """
      cursor.execute(query, (uid, uid) )
      users = cursor.fetchall()

      result = []

      for user in users:
        query = """
        SELECT * FROM messages 
        WHERE 
        (sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s)
        ORDER BY mid DESC LIMIT 1
        """
        cursor.execute(query, ( uid, user["uid"], user["uid"], uid) )
        dialog = cursor.fetchone()
        user["max_mid"] = dialog["mid"]

        if dialog["sender_id"] == uid:
          user["isRead"] = 1
        else:
          user["isRead"] = dialog["isRead"]

        result.append(user)

      result = sorted(result, key = lambda i: i['max_mid'],reverse=True) 
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()

    return result
  

  def getDialogLastMessages(self, current_uid, other_uid, number):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
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
      """
      cursor.execute(query, (current_uid, other_uid))
      connection.commit()
    except Exception as e:
      print(e)
      return None

    finally:
      cursor.close()
      connection.close()
    return result


  def getDialogPreviousMessages(self, current_uid, other_uid, mid, number):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = """
      SELECT * FROM messages WHERE
      ((receiver_id = %s AND sender_id = %s AND isDeletedByReceiver = 0)
      OR
      (receiver_id = %s AND sender_id = %s AND isDeletedBySender = 0) ) 
      AND mid < %s
      ORDER BY mid DESC LIMIT %s"""

      cursor.execute(query, (current_uid, other_uid, other_uid, current_uid, mid, number))
      result = cursor.fetchall()
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result

  def deleteDialog(self, current_uid, other_uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    
    try:
      #Delete by receiver if the user is receiver
      query = "UPDATE messages SET isDeletedByReceiver = 1 WHERE receiver_id = %s AND sender_id = %s"
      cursor.execute(query, (current_uid, other_uid) )

      #Delete by sender if the user is sender
      query = "UPDATE messages SET isDeletedBySender = 1 WHERE sender_id = %s AND receiver_id = %s"
      cursor.execute(query, (current_uid, other_uid) )
      connection.commit()
    except Exception as e:
      print(e)
    finally:
      cursor.close()
      connection.close()
from models.database import *

class NotificationModel(Database):
  @exception_handling
  def getNotifications(self, uid, number):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM notifications WHERE uid = %s ORDER BY time DESC LIMIT %s"
    cursor.execute(query, (uid, number) )
    result = cursor.fetchall()

    #Mark as read
    query = "UPDATE notifications SET isRead = 1"
    cursor.execute(query, (uid,) )

    cursor.close()
    connection.close()
    return result

  @exception_handling
  def getNewNotifications(self, uid, number):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM notifications WHERE uid = %s AND isRead = 0 ORDER BY time DESC LIMIT %s"
    cursor.execute(query, (uid, number) )
    result = cursor.fetchall()

    #Mark as read
    query = """UPDATE notifications SET isRead = 1 WHERE nfid IN 
    (SELECT nfid FROM notifications WHERE uid = %s AND isRead = 0 ORDER BY time DESC LIMIT %s)"""
    cursor.execute(query, (uid, number) )

    cursor.close()
    connection.close()
    return result
  
  @exception_handling
  def getNewNotificationNumber(self, uid):
    connection = self.getConnection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM notifications WHERE uid = %s AND isRead = 0"
    cursor.execute(query, (uid,) )
    cursor.fetchall()
    count = cursor.rowcount
    cursor.close()
    connection.close()
    return count
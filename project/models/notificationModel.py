from project.models.database import Database

class NotificationModel(Database):
  
  @staticmethod
  def getNotifications(uid, number):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM notifications WHERE uid = %s ORDER BY time DESC LIMIT %s"
      cursor.execute(query, (uid, number) )
      result = cursor.fetchall()

      #Mark as read
      query = "UPDATE notifications SET isRead = 1"
      cursor.execute(query, (uid,) )
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()

    return result

  @staticmethod
  def getNewNotifications(uid, number):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM notifications WHERE uid = %s AND isRead = 0 ORDER BY time DESC LIMIT %s"
      cursor.execute(query, (uid, number) )
      result = cursor.fetchall()

      #Mark as read
      query = """UPDATE notifications SET isRead = 1 WHERE nfid IN 
      (SELECT nfid FROM notifications WHERE uid = %s AND isRead = 0 ORDER BY time DESC LIMIT %s)"""
      cursor.execute(query, (uid, number) )
    except Exception as e:
      print(e)
      return None
    finally:
      cursor.close()
      connection.close()
    return result
  
  @staticmethod
  def getNewNotificationNumber(uid):
    connection = Database.getConnection()
    cursor = connection.cursor(dictionary=True)
    try:
      query = "SELECT * FROM notifications WHERE uid = %s AND isRead = 0"
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
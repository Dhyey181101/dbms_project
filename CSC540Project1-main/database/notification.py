class NotificationCRUD:
    
    def __init__(self, connection) -> None:
        # Check if the connection is active using DatabaseConnectionManager
        if DatabaseConnectionManager.check_if_connected():
            self.connection = connection

    def create_notification(self, user_id, message):
        """
        Creates a new notification for a user.
        """
        if self.connection:
            try:
                cursor = self.connection.cursor()
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get the current timestamp
                query = """
                INSERT INTO Notification (UserID, Message, Timestamp)
                VALUES (%s, %s, %s)
                """
                cursor.execute(query, (user_id, message, timestamp))
                self.connection.commit()
                print("Notification created successfully.")
            except Exception as e:
                print(f"Error creating notification: {e}")
            finally:
                cursor.close()

    def read_notification(self, notification_id):
        """
        Reads a specific notification by NotificationID.
        """
        if self.connection:
            cursor = self.connection.cursor()
            try:
                query = "SELECT * FROM Notification WHERE NotificationID = %s"
                cursor.execute(query, (notification_id,))
                notification = cursor.fetchone()
                if notification:
                    print(notification)
                else:
                    print("Notification not found.")
            except Exception as e:
                print(f"Error reading notification: {e}")
            finally:
                cursor.close()

    def read_notifications_by_user(self, user_id):
        """
        Reads all notifications for a specific user.
        """
        if self.connection:
            cursor = self.connection.cursor()
            try:
                query = "SELECT * FROM Notification WHERE UserID = %s ORDER BY Timestamp DESC"
                cursor.execute(query, (user_id,))
                notifications = cursor.fetchall()
                if notifications:
                    for notification in notifications:
                        print(notification)
                else:
                    print(f"No notifications found for user {user_id}.")
            except Exception as e:
                print(f"Error reading notifications: {e}")
            finally:
                cursor.close()

    def update_notification(self, notification_id, new_message):
        """
        Updates the message of an existing notification by NotificationID.
        """
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = """
                UPDATE Notification
                SET Message = %s, Timestamp = %s
                WHERE NotificationID = %s
                """
                # Update the timestamp when modifying the message
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(query, (new_message, timestamp, notification_id))
                self.connection.commit()
                print("Notification updated successfully.")
            except Exception as e:
                print(f"Error updating notification: {e}")
            finally:
                cursor.close()

    def delete_notification(self, notification_id):
        """
        Deletes a notification by NotificationID.
        """
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = "DELETE FROM Notification WHERE NotificationID = %s"
                cursor.execute(query, (notification_id,))
                self.connection.commit()
                print(f"Notification {notification_id} deleted successfully.")
            except Exception as e:
                print(f"Error deleting notification: {e}")
            finally:
                cursor.close()
from utils.db_connector import DatabaseConnectionManager

class ActivitiesCRUD:
    def __init__(self, connection) -> None:
        if DatabaseConnectionManager.check_if_connected():
            self.connection = connection

    def get_activity_by_block_id(self, content_block_id):
        """Retrieve the activity ID associated with a specific content block."""
        query = "SELECT activity_id FROM Activities WHERE content_block_id = %s LIMIT 1"
        try:
            cursor = self.connection.cursor(dictionary=True, buffered=True)  # Use buffered cursor
            cursor.execute(query, (content_block_id,))
            activity = cursor.fetchone()  # Fetch one result, or None if no result is found
            if activity:
                print(f"Activity fetched by content_block_id {content_block_id}: {activity}")
            else:
                print(f"No activity found for content_block_id {content_block_id}")
            return activity  # Returns activity ID if found, else None
        except Exception as e:
            print(f"Error fetching activity by content_block_id: {e}")
            return None
        finally:
            if cursor:
                cursor.close()  # Ensure cursor is closed in the finally block

    def hide_activity(self, activity_id):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = "UPDATE Activities SET hidden = TRUE WHERE activity_id = %s"
                cursor.execute(query, (activity_id,))
                self.connection.commit()
                return True
            except Exception as e:
                print(f"Error hiding activity: {e}")
                return False
            finally:
                cursor.close()

    def delete_activity(self, activity_id):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = "DELETE FROM Activities WHERE activity_id = %s"
                cursor.execute(query, (activity_id,))
                self.connection.commit()
                return True
            except Exception as e:
                print(f"Error deleting activity: {e}")
                return False
            finally:
                cursor.close()

    def add_activity(self, activity_id, content_block_id, section_id, chapter_id, textbook_id):
            if self.connection:
                try:
                    cursor = self.connection.cursor()
                    query = """
                    INSERT INTO Activities (activity_id, content_block_id, section_id, chapter_id, textbook_id)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (activity_id, content_block_id, section_id, chapter_id, textbook_id))
                    self.connection.commit()
                    print("Activity added successfully.")
                    return True
                except Exception as e:
                    print(f"Error adding activity: {e}")
                    self.connection.rollback()
                    return False
                finally:
                    cursor.close()
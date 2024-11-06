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
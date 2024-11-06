from utils.db_connector import DatabaseConnectionManager

class StudentActivityCRUD:
    def __init__(self, connection) -> None:
        if DatabaseConnectionManager.check_if_connected():
            self.connection = connection

    def update_or_insert_student_activity(self, student_id, course_id, textbook_id, section_id, chapter_id, block_id, unique_activity_id, question_id, points):
        """Update or insert student activity record with participation points."""
        query = """
        INSERT INTO StudentActivities (student_id, course_id, textbook_id, section_id, chapter_id, block_id, unique_activity_id, question_id, points)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE points = VALUES(points)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (student_id, course_id, textbook_id, section_id, chapter_id, block_id, unique_activity_id, question_id, points))
            self.connection.commit()
        except Exception as e:
            print(f"Error updating/inserting student activity: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    def get_total_participation_points(self, student_id, course_id):
        """Retrieve the total participation points for a student in a specific course."""
        query = """
        SELECT SUM(points) AS total_points
        FROM StudentActivities
        WHERE student_id = %s AND course_id = %s
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, (student_id, course_id))
            result = cursor.fetchone()
            return result['total_points'] if result else 0
        except Exception as e:
            print(f"Error retrieving total participation points: {e}")
            return 0
        finally:
            cursor.close()

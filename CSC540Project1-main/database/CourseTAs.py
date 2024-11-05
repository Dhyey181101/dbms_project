from utils.db_connector import DatabaseConnectionManager

class CourseTACRUD:
    
    def __init__(self, connection):
        if DatabaseConnectionManager.check_if_connected():
            self.connection = connection

    def assign_ta_to_course(self, course_ta_id, course_id, faculty_id):
        """Assign a TA to a course with specific IDs."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = """
                INSERT INTO CourseTAs (course_ta_id, course_id, faculty_id)
                VALUES (%s, %s, %s)
                """
                cursor.execute(query, (course_ta_id, course_id, faculty_id))
                self.connection.commit()
                print("TA assigned to course successfully.")
            except Exception as e:
                print(f"Error assigning TA to course: {e}")
            finally:
                cursor.close()

    def modify_ta_assignment(self, course_ta_id, course_id=None, faculty_id=None):
        """Modify an existing TA assignment in a course."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                updates = []
                values = []
                
                if course_id:
                    updates.append("course_id = %s")
                    values.append(course_id)
                if faculty_id:
                    updates.append("faculty_id = %s")
                    values.append(faculty_id)

                if updates:
                    query = f"UPDATE CourseTAs SET {', '.join(updates)} WHERE course_ta_id = %s"
                    values.append(course_ta_id)
                    cursor.execute(query, tuple(values))
                    self.connection.commit()
                    print("TA assignment modified successfully.")
                else:
                    print("No modifications provided.")
            except Exception as e:
                print(f"Error modifying TA assignment: {e}")
            finally:
                cursor.close()

    def get_all_course_tas(self):
        """Fetch all TA assignments for courses from the database."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = "SELECT course_ta_id, course_id, faculty_id FROM CourseTAs"
                cursor.execute(query)
                course_tas = cursor.fetchall()
                return course_tas
            except Exception as e:
                print(f"Error fetching course TA assignments: {e}")
                return []
            finally:
                cursor.close()
        return []

    def delete_ta_assignment(self, course_ta_id):
        """Deletes a TA assignment by its ID."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = "DELETE FROM CourseTAs WHERE course_ta_id = %s"
                cursor.execute(query, (course_ta_id,))
                self.connection.commit()
                print("TA assignment deleted successfully.")
            except Exception as e:
                print(f"Error deleting TA assignment: {e}")
            finally:
                cursor.close()

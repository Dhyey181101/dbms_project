from utils.db_connector import DatabaseConnectionManager

class CourseTACRUD:
    
    def __init__(self, connection):
        if DatabaseConnectionManager.check_if_connected():
            self.connection = connection

    def assign_ta_to_course(self, course_id, ta_id):
        """Assign a TA to a course."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = """
                INSERT INTO CourseTA (CourseID, TA_ID)
                VALUES (%s, %s)
                """
                cursor.execute(query, (course_id, ta_id))
                self.connection.commit()
                print("TA assigned to course successfully.")
            except Exception as e:
                print(f"Error assigning TA to course: {e}")
            finally:
                cursor.close()

    def modify_ta_assignment(self, course_ta_id, course_id=None, ta_id=None):
        """Modify an existing TA assignment to a course."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                updates = []
                values = []
                
                if course_id:
                    updates.append("CourseID = %s")
                    values.append(course_id)
                if ta_id:
                    updates.append("TA_ID = %s")
                    values.append(ta_id)

                if updates:
                    query = f"UPDATE CourseTA SET {', '.join(updates)} WHERE CourseTAID = %s"
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
                query = "SELECT CourseTAID, CourseID, TA_ID FROM CourseTA"
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
                query = "DELETE FROM CourseTA WHERE CourseTAID = %s"
                cursor.execute(query, (course_ta_id,))
                self.connection.commit()
                print("TA assignment deleted successfully.")
            except Exception as e:
                print(f"Error deleting TA assignment: {e}")
            finally:
                cursor.close()

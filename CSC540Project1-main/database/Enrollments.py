from utils.db_connector import DatabaseConnectionManager

class EnrollmentCRUD:
    
    def __init__(self, connection):
        if DatabaseConnectionManager.check_if_connected():
            self.connection = connection

    def enroll_student(self, course_id, student_user_id, enrollment_status="Pending"):
        """Enrolls a student in a course with an initial status (default: Pending)."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = """
                INSERT INTO Enrollments (course_id, student_user_id, enrollment_status)
                VALUES (%s, %s, %s)
                """
                cursor.execute(query, (course_id, student_user_id, enrollment_status))
                self.connection.commit()
                print("Student enrolled successfully.")
                return True
            except Exception as e:
                print(f"Error enrolling student: {e}")
            finally:
                cursor.close()
        return False

    def modify_enrollment_status(self, course_id, student_user_id, status):
        """Updates the enrollment status (e.g., to 'Enrolled' or 'Pending')."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = """
                UPDATE Enrollments
                SET enrollment_status = %s
                WHERE course_id = %s AND student_user_id = %s
                """
                cursor.execute(query, (status, course_id, student_user_id))
                self.connection.commit()
                print("Enrollment status updated successfully.")
            except Exception as e:
                print(f"Error updating enrollment status: {e}")
            finally:
                cursor.close()

    def get_all_enrollments(self):
        """Fetches all enrollments with details from the database."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = """
                SELECT course_id, student_user_id, enrollment_status 
                FROM Enrollments
                """
                cursor.execute(query)
                enrollments = cursor.fetchall()
                return enrollments
            except Exception as e:
                print(f"Error fetching enrollments: {e}")
                return []
            finally:
                cursor.close()
        return []

    def get_course_enrollment(self, course_id, status="Pending"):
        """Fetches all enrollments for a specific course with a given status."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = """
                SELECT 
                    u.user_id,
                    u.first_name
                FROM 
                    Users u
                JOIN 
                    Enrollments e ON u.user_id = e.student_user_id
                WHERE 
                    e.enrollment_status = %s 
                    AND e.course_id = %s
                    AND u.role = 'Student';
                """
                cursor.execute(query, (status, course_id))
                enrollments = cursor.fetchall()
                return enrollments
            except Exception as e:
                print(f"Error fetching enrollments: {e}")
                return []
            finally:
                cursor.close()
        return []

    def delete_enrollment(self, course_id, student_user_id):
        """Deletes an enrollment record by course and student ID."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = "DELETE FROM Enrollments WHERE course_id = %s AND student_user_id = %s"
                cursor.execute(query, (course_id, student_user_id))
                self.connection.commit()
                print("Enrollment deleted successfully.")
            except Exception as e:
                print(f"Error deleting enrollment: {e}")
            finally:
                cursor.close()

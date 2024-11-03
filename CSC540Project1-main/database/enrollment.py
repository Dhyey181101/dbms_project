from utils.db_connector import DatabaseConnectionManager

class EnrollmentCRUD:
    
    def __init__(self, connection):
        if DatabaseConnectionManager.check_if_connected():
            self.connection = connection

    def enroll_student(self, course_id, user_id, status="pending"):
        """Enrolls a student in a course with an initial status (default: pending)."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = """
                INSERT INTO Enrollment (CourseID, UserID, Status)
                VALUES (%s, %s, %s)
                """
                cursor.execute(query, (course_id, user_id, status))
                self.connection.commit()
                print("Student enrolled successfully.")
                return True
            except Exception as e:
                print(f"Error enrolling student: {e}")
            finally:
                cursor.close()
        return False

    def modify_enrollment_status(self, enrollment_id, status):
        """Updates the enrollment status (e.g., to 'approved' or 'rejected')."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = """
                UPDATE Enrollment
                SET Status = %s
                WHERE EnrollmentID = %s
                """
                cursor.execute(query, (status, enrollment_id))
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
                SELECT EnrollmentID, CourseID, UserID, Status 
                FROM Enrollment
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

    def get_course_enrollment(self, course_id, status="pending"):
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = """
                SELECT 
                    u.UserID,
                    u.FirstName
                FROM 
                    User u
                JOIN 
                    Enrollment e ON u.UserID = e.UserID
                WHERE 
                    e.Status = %s 
                    AND e.CourseID = %s
                    AND u.Role = 'student';
                """
                cursor.execute(query, (status,course_id))
                enrollments = cursor.fetchall()
                return enrollments
            except Exception as e:
                print(f"Error fetching enrollments: {e}")
                return []
            finally:
                cursor.close()
        return []


    def delete_enrollment(self, enrollment_id):
        """Deletes an enrollment record by its ID."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = "DELETE FROM Enrollment WHERE EnrollmentID = %s"
                cursor.execute(query, (enrollment_id,))
                self.connection.commit()
                print("Enrollment deleted successfully.")
            except Exception as e:
                print(f"Error deleting enrollment: {e}")
            finally:
                cursor.close()

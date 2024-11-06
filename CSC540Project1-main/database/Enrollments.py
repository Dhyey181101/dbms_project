from utils.db_connector import DatabaseConnectionManager

class EnrollmentCRUD:
    
    def __init__(self, connection):
        if DatabaseConnectionManager.check_if_connected():
            self.connection = connection

    def enroll_student(self, course_id, student_user_id, enrollment_status="Enrolled"):
        """Updates a student's enrollment status in a course to Enrolled if it was Pending."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                # Check if the student is in pending status
                check_query = """
                SELECT * FROM Enrollments 
                WHERE course_id = %s AND student_user_id = %s AND enrollment_status = 'Pending'
                """
                cursor.execute(check_query, (course_id, student_user_id))
                pending_enrollment = cursor.fetchone()
                
                if pending_enrollment:
                    # Update the enrollment status to "Enrolled"
                    update_query = """
                    UPDATE Enrollments 
                    SET enrollment_status = %s 
                    WHERE course_id = %s AND student_user_id = %s
                    """
                    cursor.execute(update_query, (enrollment_status, course_id, student_user_id))
                    self.connection.commit()
                    print("Student enrollment status updated to Enrolled.")
                    return True
                else:
                    print("No pending enrollment found for this student.")
            except Exception as e:
                print(f"Error updating enrollment status: {e}")
            finally:
                cursor.close()
        return False

    def enroll_student_i(self, course_id, student_user_id, enrollment_status="Pending"):
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

    def get_students_in_course(self, course_id):
        """Fetch students enrolled in a given course."""
        course_id = str(course_id)
        print(course_id)
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = """
                SELECT u.user_id, u.first_name, u.last_name, u.email
                FROM Enrollments e
                JOIN Users u ON e.student_user_id = u.user_id
                WHERE e.course_id = %s AND e.enrollment_status = 'Enrolled'
                """
                cursor.execute(query, (course_id,))
                students = cursor.fetchall()
                return students
            except Exception as e:
                print(f"Error fetching students for course {course_id}: {e}")
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

    def get_enrolled_courses(self, user_id):
            """Retrieve a list of courses that a user is enrolled in."""
            query = """
            SELECT c.course_id, c.course_name
            FROM Courses c
            JOIN Enrollments e ON c.course_id = e.course_id
            WHERE e.student_user_id = %s AND e.enrollment_status = 'Enrolled'
            """
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, (user_id,))
            courses = cursor.fetchall()
            cursor.close()
            return courses
    def get_pending_enrollments(self, course_id):
        """Retrieve students with pending enrollment status for a given course."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = """
                    SELECT student_user_id, enrollment_status
                    FROM Enrollments
                    WHERE course_id = %s AND enrollment_status = 'Pending'
                """
                cursor.execute(query, (course_id,))
                pending_enrollments = cursor.fetchall()
                return pending_enrollments
            except Exception as e:
                print(f"Error fetching pending enrollments for course {course_id}: {e}")
                return []
            finally:
                cursor.close()
        return []

    def get_enrolled_students(self, course_id):
        """Fetch the list of students enrolled in a course with status 'Enrolled'."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = """
                SELECT student_user_id, enrollment_status 
                FROM Enrollments 
                WHERE course_id = %s AND enrollment_status = 'Enrolled'
                """
                cursor.execute(query, (course_id,))
                students = cursor.fetchall()
                return students
            except Exception as e:
                print(f"Error fetching enrolled students: {e}")
                return []
            finally:
                cursor.close()
        return []
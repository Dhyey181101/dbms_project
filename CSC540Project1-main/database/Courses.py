from utils.db_connector import DatabaseConnectionManager

class CourseCRUD:
    
    def __init__(self, connection):
        if DatabaseConnectionManager.check_if_connected():
            self.connection = connection

    def create_course(self, course_id, course_name, textbook_id, faculty_user_id, ta_user_id, start_date, end_date, course_category, access_token, max_enrollment):
        """Creates a new course."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = """
                INSERT INTO Courses (course_id, course_name, textbook_id, faculty_user_id, ta_user_id, start_date, end_date, course_category, access_token, max_enrollment)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (course_id, course_name, textbook_id, faculty_user_id, ta_user_id, start_date, end_date, course_category, access_token, max_enrollment))
                self.connection.commit()
                print("Course created successfully.")
            except Exception as e:
                print(f"Error creating course: {e}")
            finally:
                cursor.close()

    def modify_course(self, course_id, course_name=None, start_date=None, end_date=None, max_enrollment=None):
        """Modifies course details."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                updates = []
                values = []
                
                if course_name:
                    updates.append("course_name = %s")
                    values.append(course_name)
                if start_date:
                    updates.append("start_date = %s")
                    values.append(start_date)
                if end_date:
                    updates.append("end_date = %s")
                    values.append(end_date)
                if max_enrollment:
                    updates.append("max_enrollment = %s")
                    values.append(max_enrollment)

                if updates:
                    query = f"UPDATE Courses SET {', '.join(updates)} WHERE course_id = %s"
                    values.append(course_id)
                    cursor.execute(query, tuple(values))
                    self.connection.commit()
                    print("Course modified successfully.")
                else:
                    print("No modifications provided.")
            except Exception as e:
                print(f"Error modifying course: {e}")
            finally:
                cursor.close()

    def get_all_courses(self):
        """Fetch all courses from the database."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = "SELECT course_id, course_name, faculty_user_id, start_date, end_date, course_category FROM Courses"
                cursor.execute(query)
                courses = cursor.fetchall()
                return courses
            except Exception as e:
                print(f"Error fetching courses: {e}")
                return []
            finally:
                cursor.close()
        return []

    def get_all_active_courses(self):
        """Fetch all active courses from the database."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = """
                    SELECT course_id, course_name, faculty_user_id, start_date, end_date, course_category
                    FROM Courses
                    WHERE course_category = 'Active';
                """
                cursor.execute(query)
                courses = cursor.fetchall()
                return courses
            except Exception as e:
                print(f"Error fetching courses: {e}")
                return []
            finally:
                cursor.close()
        return []


    def find_course_using_token(self, access_token):
        """Finds a course by its access token."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = "SELECT * FROM Courses WHERE access_token = %s"
                cursor.execute(query, (access_token,))
                course = cursor.fetchone()
                print(course)
                return course if course else None
            except Exception as e:
                print(f"Error fetching course using token: {e}")
                return None
            finally:
                cursor.close()
    
    def get_textbook_id_for_course(self, course_id):
        """Fetch the textbook ID for a given course from the database."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = "SELECT textbook_id FROM Courses WHERE course_id = %s"
                cursor.execute(query, (course_id,))
                result = cursor.fetchone()
                return result['textbook_id'] if result else None
            except Exception as e:
                print(f"Error fetching textbook ID: {e}")
                return None
            finally:
                cursor.close()
        return None
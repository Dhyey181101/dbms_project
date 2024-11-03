from utils.db_connector import DatabaseConnectionManager

class CourseCRUD:
    
    def __init__(self, connection):
        if DatabaseConnectionManager.check_if_connected():
            self.connection = connection

    def create_course(self, title, textbook_id, faculty_id, start_date, end_date, course_type, token, capacity):
        """Creates a new course."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = """
                INSERT INTO Course (Title, TextbookID, FacultyID, StartDate, EndDate, CourseType, Token, Capacity)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (title, textbook_id, faculty_id, start_date, end_date, course_type, token, capacity))
                self.connection.commit()
                print("Course created successfully.")
            except Exception as e:
                print(f"Error creating course: {e}")
            finally:
                cursor.close()

    """ def modify_course(self, course_id, title=None, start_date=None, end_date=None, capacity=None):
        # Modifies course details.
        if self.connection:
            try:
                cursor = self.connection.cursor()
                updates = []
                values = []
                
                if title:
                    updates.append("Title = %s")
                    values.append(title)
                if start_date:
                    updates.append("StartDate = %s")
                    values.append(start_date)
                if end_date:
                    updates.append("EndDate = %s")
                    values.append(end_date)
                if capacity:
                    updates.append("Capacity = %s")
                    values.append(capacity)

                if updates:
                    query = f"UPDATE Course SET {', '.join(updates)} WHERE CourseID = %s"
                    values.append(course_id)
                    cursor.execute(query, tuple(values))
                    self.connection.commit()
                    print("Course modified successfully.")
                else:
                    print("No modifications provided.")
            except Exception as e:
                print(f"Error modifying course: {e}")
            finally:
                cursor.close() """

    def get_all_courses(self):
        """Fetch all courses from the database."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = "SELECT CourseID, Title, FacultyID, StartDate, EndDate, CourseType FROM Course"
                cursor.execute(query)
                courses = cursor.fetchall()
                return courses
            except Exception as e:
                print(f"Error fetching courses: {e}")
                return []
            finally:
                cursor.close()
        return []

    def find_course_using_token(self, token):
        """Finds a course by its token."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = "SELECT * FROM Course WHERE Token = %s"
                cursor.execute(query, (token,))
                course = cursor.fetchone()
                print(course)
                return course if course else None
            except Exception as e:
                print(f"Error fetching course using token: {e}")
                return None
            finally:
                cursor.close()

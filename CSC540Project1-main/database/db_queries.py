from utils.db_connector import DatabaseConnectionManager

class DBQueries:

    def __init__(self, connection):
        if DatabaseConnectionManager.check_if_connected():
            self.connection = connection

    def get_first_chapter_section_count(self):
        """Retrieve the number of sections in the first chapter of a textbook."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = """
                SELECT COUNT(*) FROM Section
                WHERE ChapterID = (SELECT ChapterID FROM Chapter WHERE TextbookID = 1 ORDER BY ChapterID LIMIT 1)
                """
                cursor.execute(query)
                result = cursor.fetchone()
                return result[0] if result else 0
            except Exception as e:
                print(f"Error fetching section count: {e}")
            finally:
                cursor.close()

    def get_faculty_and_tas(self):
        """Fetch the names and roles of faculty and TAs for all courses."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = """
                SELECT u.FirstName, u.LastName, 'Faculty' AS Role FROM User u
                JOIN Course c ON u.UserID = c.FacultyID
                UNION ALL
                SELECT u.FirstName, u.LastName, 'TA' AS Role FROM User u
                JOIN CourseTA ta ON u.UserID = ta.TA_ID
                """
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error fetching faculty and TA names: {e}")
            finally:
                cursor.close()

    def get_active_courses_with_faculty_and_student_count(self):
        """For each active course, retrieve the course ID, faculty name, and total student count."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = """
                SELECT c.CourseID, CONCAT(u.FirstName, ' ', u.LastName) AS Faculty, COUNT(e.UserID) AS StudentCount
                FROM Course c
                JOIN User u ON c.FacultyID = u.UserID
                LEFT JOIN Enrollment e ON c.CourseID = e.CourseID AND e.Status = 'approved'
                WHERE c.CourseType = 'active'
                GROUP BY c.CourseID, u.FirstName, u.LastName
                """
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error fetching active courses with student count: {e}")
            finally:
                cursor.close()

    def get_course_with_largest_waiting_list(self):
        """Find the course with the largest waiting list, return course ID and waiting list count."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = """
                SELECT e.CourseID, COUNT(*) AS WaitingListCount
                FROM Enrollment e
                WHERE e.Status = 'pending'
                GROUP BY e.CourseID
                ORDER BY WaitingListCount DESC
                LIMIT 1
                """
                cursor.execute(query)
                return cursor.fetchone()
            except Exception as e:
                print(f"Error fetching course with largest waiting list: {e}")
            finally:
                cursor.close()

    def get_chapter_content(self, textbook_id, chapter_number):
        """Retrieve the contents of a specific chapter in a textbook in proper sequence."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = """
                SELECT cb.Content
                FROM ContentBlock cb
                JOIN Chapter ch ON cb.ChapterID = ch.ChapterID
                WHERE ch.TextbookID = %s AND ch.ChapterID = %s
                ORDER BY cb.SequenceNumber
                """
                cursor.execute(query, (textbook_id, chapter_number))
                return [row['Content'] for row in cursor.fetchall()]
            except Exception as e:
                print(f"Error fetching chapter content: {e}")
            finally:
                cursor.close()

    def get_incorrect_answers_for_activity_question(self, activity_id, question_id):
        """Retrieve incorrect answers and explanations for a specific question in an activity."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = """
                SELECT q.WrongAnswer1, q.WrongExplanation1, q.WrongAnswer2, q.WrongExplanation2,
                       q.WrongAnswer3, q.WrongExplanation3
                FROM Question q
                WHERE q.ActivityID = %s AND q.QuestionID = %s
                """
                cursor.execute(query, (activity_id, question_id))
                return cursor.fetchall()
            except Exception as e:
                print(f"Error fetching incorrect answers: {e}")
            finally:
                cursor.close()

    def find_books_in_different_status_by_instructors(self):
        """Find books in active status by one instructor and evaluation status by another."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = """
                SELECT DISTINCT t1.TextbookID, u1.FirstName AS Instructor1, c1.CourseType AS Status1,
                                u2.FirstName AS Instructor2, c2.CourseType AS Status2
                FROM Course c1
                JOIN Course c2 ON c1.TextbookID = c2.TextbookID AND c1.FacultyID != c2.FacultyID
                JOIN User u1 ON c1.FacultyID = u1.UserID
                JOIN User u2 ON c2.FacultyID = u2.UserID
                WHERE c1.CourseType = 'active' AND c2.CourseType = 'evaluation'
                """
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error fetching books with different statuses by instructors: {e}")
            finally:
                cursor.close()

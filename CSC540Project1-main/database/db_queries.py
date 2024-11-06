from utils.db_connector import DatabaseConnectionManager

class DBQueries:

    def __init__(self, connection):
        if DatabaseConnectionManager.check_if_connected():
            self.connection = connection

    def get_first_chapter_section_count(self, textbook_id):
        """Retrieve the number of sections in the first chapter of a textbook."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = """
                SELECT COUNT(*) AS section_count 
                FROM Sections 
                WHERE chapter_id = (
                    SELECT chapter_id 
                    FROM Chapters 
                    WHERE textbook_id = %s 
                    ORDER BY chapter_id 
                    LIMIT 1
                )
                """
                cursor.execute(query, (textbook_id,))
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
                SELECT CONCAT(u.first_name, ' ', u.last_name) AS name, 'Faculty' AS role 
                FROM Users u
                JOIN Courses c ON u.user_id = c.faculty_user_id
                UNION ALL
                SELECT CONCAT(u.first_name, ' ', u.last_name) AS name, 'TA' AS role 
                FROM Users u
                JOIN CourseTAs ta ON u.user_id = ta.course_ta_id
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
                SELECT c.course_id, CONCAT(u.first_name, ' ', u.last_name) AS faculty, COUNT(e.student_user_id) AS student_count
                FROM Courses c
                JOIN Users u ON c.faculty_user_id = u.user_id
                LEFT JOIN Enrollments e ON c.course_id = e.course_id AND e.enrollment_status = 'Enrolled'
                WHERE c.course_category = 'Active'
                GROUP BY c.course_id, u.first_name, u.last_name
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
                SELECT e.course_id, COUNT(*) AS waiting_list_count
                FROM Enrollments e
                WHERE e.enrollment_status = 'Pending'
                GROUP BY e.course_id
                ORDER BY waiting_list_count DESC
                LIMIT 1
                """
                cursor.execute(query)
                return cursor.fetchone()
            except Exception as e:
                print(f"Error fetching course with largest waiting list: {e}")
            finally:
                cursor.close()

    def get_chapter_content(self, textbook_id, chapter_id):
        """Retrieve the contents of a specific chapter in a textbook in proper sequence."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = """
                SELECT cb.content 
                FROM ContentBlocks cb
                JOIN Chapters ch ON cb.chapter_id = ch.chapter_id
                WHERE ch.textbook_id = %s AND ch.chapter_id = %s
                ORDER BY cb.content_block_id
                """
                cursor.execute(query, (textbook_id, chapter_id))
                return [row['content'] for row in cursor.fetchall()]
            except Exception as e:
                print(f"Error fetching chapter content: {e}")
            finally:
                cursor.close()

    def get_incorrect_answers_for_activity_question(self, textbook_id, chapter_id, section_id, activity_id, question_id):
        """Retrieve incorrect answers and explanations for a specific question in an activity."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = """
                SELECT option_1 AS answer, opt_1_exp AS explanation FROM Questions 
                WHERE textbook_id = %s AND chapter_id = %s AND section_id = %s 
                  AND unique_activity_id = %s AND question_id = %s AND answer != 1
                UNION ALL
                SELECT option_2, opt_2_exp FROM Questions 
                WHERE textbook_id = %s AND chapter_id = %s AND section_id = %s 
                  AND unique_activity_id = %s AND question_id = %s AND answer != 2
                UNION ALL
                SELECT option_3, opt_3_exp FROM Questions 
                WHERE textbook_id = %s AND chapter_id = %s AND section_id = %s 
                  AND unique_activity_id = %s AND question_id = %s AND answer != 3
                UNION ALL
                SELECT option_4, opt_4_exp FROM Questions 
                WHERE textbook_id = %s AND chapter_id = %s AND section_id = %s 
                  AND unique_activity_id = %s AND question_id = %s AND answer != 4
                """
                cursor.execute(query, (textbook_id, chapter_id, section_id, activity_id, question_id) * 4)
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
                SELECT DISTINCT c1.textbook_id, u1.first_name AS instructor1, c1.course_category AS status1,
                                u2.first_name AS instructor2, c2.course_category AS status2
                FROM Courses c1
                JOIN Courses c2 ON c1.textbook_id = c2.textbook_id AND c1.faculty_user_id != c2.faculty_user_id
                JOIN Users u1 ON c1.faculty_user_id = u1.user_id
                JOIN Users u2 ON c2.faculty_user_id = u2.user_id
                WHERE c1.course_category = 'Active' AND c2.course_category = 'Evaluation'
                """
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error fetching books with different statuses by instructors: {e}")
                return None
            finally:
                cursor.close()

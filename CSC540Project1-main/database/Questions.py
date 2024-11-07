from utils.db_connector import DatabaseConnectionManager

class QuestionsCRUD:
    def __init__(self, connection):
        if DatabaseConnectionManager.check_if_connected():
            self.connection = connection

    def add_question(self, question_id, textbook_id, chapter_id, section_id, block_id, unique_activity_id, question_text, options, answer):
        """Add a new question with options to the database."""
        if self.connection:
            try:
                cursor = self.connection.cursor()

                query = """
                INSERT INTO Questions (
                    question_id, textbook_id, chapter_id, section_id, block_id, unique_activity_id, 
                    question_text, option_1, opt_1_exp, option_2, opt_2_exp, 
                    option_3, opt_3_exp, option_4, opt_4_exp, answer
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                # Prepare values for the query
                values = (
                    question_id, textbook_id, chapter_id, section_id, block_id, unique_activity_id,
                    question_text,
                    options[0][0], options[0][1],  # Option 1 text and explanation
                    options[1][0], options[1][1],  # Option 2 text and explanation
                    options[2][0], options[2][1],  # Option 3 text and explanation
                    options[3][0], options[3][1],  # Option 4 text and explanation
                    answer  # Index of the correct answer
                )

                cursor.execute(query, values)
                self.connection.commit()
                print("Question added successfully.")
            except Exception as e:
                print(f"Error adding question: {e}")
            finally:
                cursor.close()

    def get_questions_by_block_id(self, block_id, section_id, chapter_id,textbook_id):
        """Fetch questions associated with a specific content block, section, and chapter."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = """
                SELECT question_id, question_text, option_1, opt_1_exp, option_2, opt_2_exp, 
                       option_3, opt_3_exp, option_4, opt_4_exp, answer
                FROM Questions
                WHERE block_id = %s AND section_id = %s AND chapter_id = %s AND textbook_id=%s
                """
                cursor.execute(query, (block_id, section_id, chapter_id,textbook_id))
                questions = cursor.fetchall()
                return questions
            except Exception as e:
                print(f"Error fetching questions: {e}")
                return []
            finally:
                cursor.close()
        else:
            print("No active database connection.")
        return []

from utils.db_connector import DatabaseConnectionManager

class SectionCRUD:

    def __init__(self, connection) -> None:
        if DatabaseConnectionManager.check_if_connected():
            self.connection = connection

    def get_section_id_by_title(self, section_title, chapter_id, textbook_id):
        """Retrieve the section_id based on the section title, chapter_id, and textbook_id."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = "SELECT section_id FROM Sections WHERE title = %s AND chapter_id = %s AND textbook_id = %s"
                cursor.execute(query, (section_title, chapter_id, textbook_id))
                result = cursor.fetchone()
                if result:
                    return result[0]
                else:
                    print("No section found with that title.")
                    return None
            except Exception as e:
                print(f"Error fetching section ID: {e}")
            finally:
                cursor.close()
        return None

    def add_section(self, textbook_id, chapter_id, section_id, section_title, is_hidden=False):
        """Add a new section under a specific chapter."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = """
                INSERT INTO Sections (textbook_id, section_id, chapter_id, title, hidden)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (textbook_id, section_id, chapter_id, section_title, is_hidden))
                self.connection.commit()
            except Exception as e:
                print(f"Error creating section: {e}")
            finally:
                cursor.close()


    def modify_section(self, section_title, chapter_id, textbook_id, new_section_id=None, new_section_title=None, new_hidden=None):
        """Modify a section's details using the title, chapter_id, and textbook_id as identifiers."""
        section_id = self.get_section_id_by_title(section_title, chapter_id, textbook_id)
        if section_id and self.connection:
            try:
                cursor = self.connection.cursor()
                updates = []
                values = []
                
                if new_section_id:
                    updates.append("section_id = %s")
                    values.append(new_section_id)
                
                if new_section_title:
                    updates.append("title = %s")
                    values.append(new_section_title)
                
                if new_hidden is not None:
                    updates.append("hidden = %s")
                    values.append(new_hidden)
                
                if updates:
                    query = f"UPDATE Sections SET {', '.join(updates)} WHERE section_id = %s AND chapter_id = %s AND textbook_id = %s"
                    values.extend([section_id, chapter_id, textbook_id])
                    cursor.execute(query, tuple(values))
                    self.connection.commit()
                    print("Section modified successfully.")
                else:
                    print("No modifications provided.")
            except Exception as e:
                print(f"Error modifying section: {e}")
            finally:
                cursor.close()

    def delete_section(self, section_id, chapter_id, textbook_id):
        """Delete a section from the database using section_id, chapter_id, and textbook_id as identifiers."""
        if section_id and self.connection:
            try:
                cursor = self.connection.cursor()
                query = "DELETE FROM Sections WHERE section_id = %s AND chapter_id = %s AND textbook_id = %s"
                cursor.execute(query, (section_id, chapter_id, textbook_id))
                self.connection.commit()
                print("Section deleted successfully.")
            except Exception as e:
                print(f"Error deleting section: {e}")
            finally:
                cursor.close()
    
    def get_sections_by_chapter(self, chapter_id, textbook_id, include_hidden=False):
        """Fetch all sections for a given chapter ID and textbook ID."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = "SELECT section_id, title, hidden FROM Sections WHERE chapter_id = %s AND textbook_id = %s"
                if not include_hidden:
                    query += " AND hidden = FALSE"
                cursor.execute(query, (chapter_id, textbook_id))
                sections = cursor.fetchall()
                return sections
            except Exception as e:
                print(f"Error fetching sections: {e}")
                return []
            finally:
                cursor.close()
        return []

    def get_all_sections_associated_with_user(self, user_id):
        """Fetch all sections associated with activities the user has participated in."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = """
                SELECT DISTINCT s.section_id, s.title
                FROM Sections s
                JOIN Chapters ch ON s.textbook_id = ch.textbook_id AND s.chapter_id = ch.chapter_id
                JOIN Courses c ON ch.textbook_id = c.textbook_id
                JOIN StudentActivities sa ON c.course_id = sa.course_id
                WHERE sa.student_id = %s AND s.hidden = FALSE
                """
                cursor.execute(query, (user_id,))
                sections = cursor.fetchall()

                return sections
            except Exception as e:
                print(f"Error fetching sections for user {user_id}: {e}")
                return []
            finally:
                cursor.close()
        return []




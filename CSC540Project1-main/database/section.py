from utils.db_connector import DatabaseConnectionManager

class SectionCRUD:

    def __init__(self, connection) -> None:
        if DatabaseConnectionManager.check_if_connected():
            self.connection = connection

    def get_section_id_by_title(self, section_title):
        """Retrieve the Section ID based on the section title."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = "SELECT SectionID FROM Section WHERE Title = %s"
                cursor.execute(query, (section_title,))
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

    def add_section(self, chapter_id, section_number, section_title):
        """Add a new section under a specific chapter."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = """
                INSERT INTO Section (ChapterID, SectionNumber, Title)
                VALUES (%s, %s, %s)
                """
                cursor.execute(query, (chapter_id, section_number, section_title))
                self.connection.commit()
                print("Section created successfully.")
            except Exception as e:
                print(f"Error creating section: {e}")
            finally:
                cursor.close()

    def modify_section(self, section_title, new_section_number=None, new_section_title=None):
        """Modify a section's details using the title as the identifier."""
        section_id = self.get_section_id_by_title(section_title)
        if section_id and self.connection:
            try:
                cursor = self.connection.cursor()
                updates = []
                values = []
                
                if new_section_number:
                    updates.append("SectionNumber = %s")
                    values.append(new_section_number)
                
                if new_section_title:
                    updates.append("Title = %s")
                    values.append(new_section_title)
                
                if updates:
                    query = f"UPDATE Section SET {', '.join(updates)} WHERE SectionID = %s"
                    values.append(section_id)
                    cursor.execute(query, tuple(values))
                    self.connection.commit()
                    print("Section modified successfully.")
                else:
                    print("No modifications provided.")
            except Exception as e:
                print(f"Error modifying section: {e}")
            finally:
                cursor.close()

    def delete_section(self, section_title):
        """Delete a section from the database using the title as the identifier."""
        section_id = self.get_section_id_by_title(section_title)
        if section_id and self.connection:
            try:
                cursor = self.connection.cursor()
                query = "DELETE FROM Section WHERE SectionID = %s"
                cursor.execute(query, (section_id,))
                self.connection.commit()
                print("Section deleted successfully.")
            except Exception as e:
                print(f"Error deleting section: {e}")
            finally:
                cursor.close()
    
    def get_sections_by_chapter(self, chapter_id):
        """Fetch all sections for a given chapter ID."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = "SELECT SectionID, SectionNumber, Title FROM Section WHERE ChapterID = %s"
                cursor.execute(query, (chapter_id,))
                sections = cursor.fetchall()
                return sections
            except Exception as e:
                print(f"Error fetching sections: {e}")
                return []
            finally:
                cursor.close()
        return []

    def get_all_sections_associated_with_user(self, user_id):
        """Fetch all sections associated with courses the user is enrolled in."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = """
                SELECT s.SectionID, s.Title
                FROM Section s
                JOIN Course c ON s.TextbookID = c.TextbookID
                JOIN Enrollment e ON c.CourseID = e.CourseID
                WHERE e.UserID = %s AND s.IsHidden=False
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

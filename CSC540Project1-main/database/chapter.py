from utils.db_connector import DatabaseConnectionManager

class ChapterCRUD:
    def __init__(self, connection) -> None:
        if DatabaseConnectionManager.check_if_connected():
            self.connection = connection

    def get_chapter_id_by_name(self, chapter_name):
        """Retrieve the Chapter ID based on Chaptername."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = "SELECT ChapterID FROM Chapter WHERE Chaptername = %s"
                cursor.execute(query, (chapter_name,))
                result = cursor.fetchone()
                if result:
                    return result[0]
                else:
                    print("No chapter found with that name.")
                    return None
            except Exception as e:
                print(f"Error fetching chapter ID: {e}")
            finally:
                cursor.close()
        return None

    def add_chapter(self, textbook_id, chapter_title, chapter_name, is_hidden=False):
        """Add a new chapter to a textbook."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = """
                INSERT INTO Chapter (TextbookID, Title, IsHidden)
                VALUES (%s, %s, %s)
                """
                cursor.execute(query, (textbook_id, chapter_title, is_hidden))
                self.connection.commit()
                print("Chapter added successfully.")
            except Exception as e:
                print(f"Error adding chapter: {e}")
            finally:
                cursor.close()

    def get_all_chapters(self, textbook_id, include_hidden=False):
        """Fetch all chapters for a specific textbook, optionally including hidden chapters."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = """
                SELECT ChapterID, Title, IsHidden
                FROM Chapter
                WHERE TextbookID = %s
                """
                if not include_hidden:
                    query += " AND IsHidden = FALSE"
                cursor.execute(query, (textbook_id,))
                chapters = cursor.fetchall()
                return chapters
            except Exception as e:
                print(f"Error fetching chapters: {e}")
                return []
            finally:
                cursor.close()
        return []
      
    def modify_chapter(self, chapter_name, new_title, new_chaptername, new_is_hidden=None):
        """Modify a specific chapter by name, with the option to update its hidden status."""
        chapter_id = self.get_chapter_id_by_name(chapter_name)
        if chapter_id and self.connection:

            try:
                cursor = self.connection.cursor()
                query = """
                UPDATE Chapter
                SET Title = %s,
                """
                params = [new_title]
                
                if new_is_hidden is not None:
                    query += ", IsHidden = %s"
                    params.append(new_is_hidden)

                query += " WHERE ChapterID = %s"
                params.append(chapter_id)
                
                cursor.execute(query, tuple(params))
                self.connection.commit()
                print("Chapter modified successfully.")
            except Exception as e:
                print(f"Error modifying chapter: {e}")
            finally:
                cursor.close()
    
    def hide_chapter(self, chapter_name):
        """Hide a chapter from being displayed by name."""
        chapter_id = self.get_chapter_id_by_name(chapter_name)
        if chapter_id and self.connection:
            try:
                cursor = self.connection.cursor()
                query = "UPDATE Chapter SET IsHidden = %s WHERE ChapterID = %s"
                cursor.execute(query, (True, chapter_id))
                self.connection.commit()
                print("Chapter hidden successfully.")
            except Exception as e:
                print(f"Error hiding chapter: {e}")
            finally:
                cursor.close()

    def show_chapter(self, chapter_name):
        """Show a previously hidden chapter by name."""
        chapter_id = self.get_chapter_id_by_name(chapter_name)
        if chapter_id and self.connection:
            try:
                cursor = self.connection.cursor()
                query = "UPDATE Chapter SET IsHidden = %s WHERE ChapterID = %s"
                cursor.execute(query, (False, chapter_id))
                self.connection.commit()
                print("Chapter is now visible.")
            except Exception as e:
                print(f"Error showing chapter: {e}")
            finally:
                cursor.close()

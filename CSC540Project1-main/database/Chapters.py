from utils.db_connector import DatabaseConnectionManager

class ChapterCRUD:
    def __init__(self, connection) -> None:
        if DatabaseConnectionManager.check_if_connected():
            self.connection = connection

    def get_chapter_id_by_name(self, chapter_name):
        """Retrieve the chapter_id based on the title."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = "SELECT chapter_id FROM Chapters WHERE title = %s"
                cursor.execute(query, (chapter_name,))
                result = cursor.fetchone()
                if result:
                    return result[0]
                else:
                    print("No chapter found with that title.")
                    return None
            except Exception as e:
                print(f"Error fetching chapter ID: {e}")
            finally:
                cursor.close()
        return None

    def add_chapter(self, textbook_id, chapter_id, chapter_title, is_hidden=False):
        """Add a new chapter to a textbook."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = """
                INSERT INTO Chapters (textbook_id, chapter_id, title, hidden)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (textbook_id, chapter_id, chapter_title, is_hidden))
                self.connection.commit()
            except Exception as e:
                print(f"Error adding chapter: {e}")
            finally:
                cursor.close()

    def generate_chapter_id(self, textbook_id):
        """Generate a new chapter_id based on the textbook_id."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = "SELECT MAX(chapter_id) FROM Chapters WHERE textbook_id = %s"
                cursor.execute(query, (textbook_id,))
                result = cursor.fetchone()
                if result and result[0]:
                    # Assuming the chapter ID is something like chap01, chap02, etc.
                    last_id = int(result[0][4:])  # Extract numeric part after 'chap'
                    new_id = f"chap{str(last_id + 1).zfill(2)}"
                else:
                    new_id = "chap01"
                return new_id
            except Exception as e:
                print(f"Error generating chapter ID: {e}")
            finally:
                cursor.close()
        return "chap01"

    def get_all_chapters(self, textbook_id, include_hidden=False):
        """Fetch all chapters for a specific textbook, optionally including hidden chapters."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = "SELECT chapter_id, title, hidden FROM Chapters WHERE textbook_id = %s"
                if not include_hidden:
                    query += " AND hidden = FALSE"
                cursor.execute(query, (textbook_id,))
                chapters = cursor.fetchall()
                return chapters
            except Exception as e:
                print(f"Error fetching chapters: {e}")
                return []
            finally:
                cursor.close()
        return []
        
    def modify_chapter(self, chapter_name, new_title=None, new_is_hidden=None):
        """Modify a specific chapter by title, with the option to update its hidden status."""
        chapter_id = self.get_chapter_id_by_name(chapter_name)
        if chapter_id and self.connection:
            try:
                cursor = self.connection.cursor()
                updates = []
                values = []
                
                if new_title:
                    updates.append("title = %s")
                    values.append(new_title)
                
                if new_is_hidden is not None:
                    updates.append("hidden = %s")
                    values.append(new_is_hidden)

                if updates:
                    query = f"UPDATE Chapters SET {', '.join(updates)} WHERE chapter_id = %s"
                    values.append(chapter_id)
                    cursor.execute(query, tuple(values))
                    self.connection.commit()
                    print("Chapter modified successfully.")
                else:
                    print("No modifications provided.")
            except Exception as e:
                print(f"Error modifying chapter: {e}")
            finally:
                cursor.close()

    def hide_chapter(self, chapter_name):
        """Hide a chapter from being displayed by title."""
        chapter_id = self.get_chapter_id_by_name(chapter_name)
        if chapter_id and self.connection:
            try:
                cursor = self.connection.cursor()
                query = "UPDATE Chapters SET hidden = %s WHERE chapter_id = %s"
                cursor.execute(query, (True, chapter_id))
                self.connection.commit()
                print("Chapter hidden successfully.")
            except Exception as e:
                print(f"Error hiding chapter: {e}")
            finally:
                cursor.close()

    def show_chapter(self, chapter_name):
        """Show a previously hidden chapter by title."""
        chapter_id = self.get_chapter_id_by_name(chapter_name)
        if chapter_id and self.connection:
            try:
                cursor = self.connection.cursor()
                query = "UPDATE Chapters SET hidden = %s WHERE chapter_id = %s"
                cursor.execute(query, (False, chapter_id))
                self.connection.commit()
                print("Chapter is now visible.")
            except Exception as e:
                print(f"Error showing chapter: {e}")
            finally:
                cursor.close()

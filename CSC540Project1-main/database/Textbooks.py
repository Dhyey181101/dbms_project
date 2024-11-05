from utils.db_connector import DatabaseConnectionManager

class TextbookCRUD:
    
    def __init__(self, connection) -> None:
        if DatabaseConnectionManager.check_if_connected():
            self.connection = connection

    def get_textbook_id_by_title(self, title):
        """Retrieve the textbook_id based on the title."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = "SELECT textbook_id FROM Textbooks WHERE title = %s"
                cursor.execute(query, (title,))
                result = cursor.fetchone()
                if result:
                    return result[0]
                else:
                    print("No textbook found with that title.")
                    return None
            except Exception as e:
                print(f"Error fetching textbook ID: {e}")
            finally:
                cursor.close()
        return None

    def create_etextbook(self, title, admin_id, is_hidden=False):
        """Create a new e-textbook with an optional hidden status."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = """
                INSERT INTO Textbooks (title, created_by_admin, hidden)
                VALUES (%s, %s, %s)
                """
                cursor.execute(query, (title, admin_id, is_hidden))
                self.connection.commit()
                print("E-textbook created successfully.")
            except Exception as e:
                print(f"Error creating e-textbook: {e}")
            finally:
                cursor.close()
    
    def modify_etextbook(self, title, new_title=None, is_hidden=None):
        """Modify an e-textbook's details using the title as the identifier."""
        textbook_id = self.get_textbook_id_by_title(title)
        if textbook_id and self.connection:
            try:
                cursor = self.connection.cursor()
                updates = []
                values = []
                
                if new_title:
                    updates.append("title = %s")
                    values.append(new_title)
                
                if is_hidden is not None:
                    updates.append("hidden = %s")
                    values.append(is_hidden)
                
                if updates:
                    query = f"UPDATE Textbooks SET {', '.join(updates)} WHERE textbook_id = %s"
                    values.append(textbook_id)
                    cursor.execute(query, tuple(values))
                    self.connection.commit()
                    print("Textbook modified successfully.")
                else:
                    print("No modifications provided.")
            except Exception as e:
                print(f"Error modifying textbook: {e}")
            finally:
                cursor.close()

    def get_all_textbooks(self, include_hidden=False):
        """Fetch all textbooks, optionally including hidden ones."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = "SELECT textbook_id, title, created_by_admin, hidden FROM Textbooks"
                if not include_hidden:
                    query += " WHERE hidden = FALSE"
                
                cursor.execute(query)
                textbooks = cursor.fetchall()
                return textbooks  # Return the list of textbooks
            except Exception as e:
                print(f"Error fetching textbooks: {e}")
                return []  # Return an empty list in case of an error
            finally:
                cursor.close()
        return []

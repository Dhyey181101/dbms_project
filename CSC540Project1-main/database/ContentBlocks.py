from utils.db_connector import DatabaseConnectionManager

class ContentBlockCRUD:
    def __init__(self, connection) -> None:
        if DatabaseConnectionManager.check_if_connected():
            self.connection = connection

    def get_block_id_by_content(self, content, section_id, chapter_id, textbook_id):
        """Retrieve the content_block_id based on content, section_id, chapter_id, and textbook_id."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = """
                SELECT content_block_id 
                FROM ContentBlocks 
                WHERE content = %s AND section_number = %s AND chapter_id = %s AND textbook_id = %s
                """
                cursor.execute(query, (content, section_id, chapter_id, textbook_id))
                result = cursor.fetchone()
                if result:
                    return result[0]
                else:
                    print("No content block found with that content.")
                    return None
            except Exception as e:
                print(f"Error fetching content block ID: {e}")
            finally:
                cursor.close()
        return None

    def add_content_block(self, textbook_id, chapter_id, section_number, content_block_id, block_type, content, hidden=False):
        """Add a new content block to a specific section."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = """
                INSERT INTO ContentBlocks (textbook_id, chapter_id, section_number, content_block_id, content_type, content, hidden)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (textbook_id, chapter_id, section_number, content_block_id, block_type, content, hidden))
                self.connection.commit()
                print("Content block created successfully.")
            except Exception as e:
                print(f"Error creating content block: {e}")
            finally:
                cursor.close()

    def modify_content_block(self, content, textbook_id, chapter_id, section_number, content_block_id, new_block_type=None, new_content=None, new_hidden=None):
        """Modify a content block's details using content as identifier."""
        block_id = self.get_block_id_by_content(content, section_number, chapter_id, textbook_id)
        if block_id and self.connection:
            try:
                cursor = self.connection.cursor()
                updates = []
                values = []

                if new_block_type:
                    updates.append("content_type = %s")
                    values.append(new_block_type)
                
                if new_content:
                    updates.append("content = %s")
                    values.append(new_content)
                
                if new_hidden is not None:
                    updates.append("hidden = %s")
                    values.append(new_hidden)

                if updates:
                    query = f"UPDATE ContentBlocks SET {', '.join(updates)} WHERE content_block_id = %s AND section_number = %s AND chapter_id = %s AND textbook_id = %s"
                    values.extend([content_block_id, section_number, chapter_id, textbook_id])
                    cursor.execute(query, tuple(values))
                    self.connection.commit()
                    print("Content block modified successfully.")
                else:
                    print("No modifications provided.")
            except Exception as e:
                print(f"Error modifying content block: {e}")
            finally:
                cursor.close()

    def delete_content_block(self, content, section_id, chapter_id, textbook_id):
        """Delete a content block from the database using content as identifier."""
        block_id = self.get_block_id_by_content(content, section_id, chapter_id, textbook_id)
        if block_id and self.connection:
            try:
                cursor = self.connection.cursor()
                query = "DELETE FROM ContentBlocks WHERE content_block_id = %s AND section_number = %s AND chapter_id = %s AND textbook_id = %s"
                cursor.execute(query, (block_id, section_id, chapter_id, textbook_id))
                self.connection.commit()
                print("Content block deleted successfully.")
            except Exception as e:
                print(f"Error deleting content block: {e}")
            finally:
                cursor.close()

    def get_content_blocks_by_section(self, textbook_id, chapter_id, section_number, include_hidden=False):
        """Fetch all content blocks for a given section ID."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = """
                SELECT content_block_id, content_type, content 
                FROM ContentBlocks 
                WHERE textbook_id = %s AND chapter_id = %s AND section_number = %s
                """
                if not include_hidden:
                    query += " AND hidden = FALSE"
                cursor.execute(query, (textbook_id, chapter_id, section_number))
                content_blocks = cursor.fetchall()
                return content_blocks
            except Exception as e:
                print(f"Error fetching content blocks: {e}")
                return []
            finally:
                cursor.close()
        return []
    
    def hide_content_block(self, content, section_id, chapter_id, textbook_id):
        """Hide a content block from being displayed using content as identifier."""
        block_id = self.get_block_id_by_content(content, section_id, chapter_id, textbook_id)
        if block_id and self.connection:
            try:
                cursor = self.connection.cursor()
                query = "UPDATE ContentBlocks SET hidden = %s WHERE content_block_id = %s AND section_number = %s AND chapter_id = %s AND textbook_id = %s"
                cursor.execute(query, (True, block_id, section_id, chapter_id, textbook_id))
                self.connection.commit()
                print("Content block hidden successfully.")
            except Exception as e:
                print(f"Error hiding content block: {e}")
            finally:
                cursor.close()

    def show_content_block(self, content, section_id, chapter_id, textbook_id):
        """Show a previously hidden content block using content as identifier."""
        block_id = self.get_block_id_by_content(content, section_id, chapter_id, textbook_id)
        if block_id and self.connection:
            try:
                cursor = self.connection.cursor()
                query = "UPDATE ContentBlocks SET hidden = %s WHERE content_block_id = %s AND section_number = %s AND chapter_id = %s AND textbook_id = %s"
                cursor.execute(query, (False, block_id, section_id, chapter_id, textbook_id))
                self.connection.commit()
                print("Content block is now visible.")
            except Exception as e:
                print(f"Error showing content block: {e}")
            finally:
                cursor.close()

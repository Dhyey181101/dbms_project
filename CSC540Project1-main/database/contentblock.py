from utils.db_connector import DatabaseConnectionManager

class ContentBlockCRUD:
    def __init__(self, connection) -> None:
        if DatabaseConnectionManager.check_if_connected():
            self.connection = connection

    def get_block_id_by_content(self, content):
        """Retrieve the Block ID based on Content."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = "SELECT BlockID FROM ContentBlock WHERE Content = %s"
                cursor.execute(query, (content,))
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

    def add_content_block(self, section_id, block_type, content):
        """Add a new content block to a specific section."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = """
                INSERT INTO ContentBlock (SectionID, BlockType, Content)
                VALUES (%s, %s, %s)
                """
                cursor.execute(query, (section_id, block_type, content))
                self.connection.commit()
                print("Content block created successfully.")
            except Exception as e:
                print(f"Error creating content block: {e}")
            finally:
                cursor.close()

    def modify_content_block(self, content, new_block_type=None, new_content=None):
        """Modify a content block's details using content as identifier."""
        block_id = self.get_block_id_by_content(content)
        if block_id and self.connection:
            try:
                cursor = self.connection.cursor()
                updates = []
                values = []

                if new_block_type:
                    updates.append("BlockType = %s")
                    values.append(new_block_type)
                
                if new_content:
                    updates.append("Content = %s")
                    values.append(new_content)

                if updates:
                    query = f"UPDATE ContentBlock SET {', '.join(updates)} WHERE BlockID = %s"
                    values.append(block_id)
                    cursor.execute(query, tuple(values))
                    self.connection.commit()
                    print("Content block modified successfully.")
                else:
                    print("No modifications provided.")
            except Exception as e:
                print(f"Error modifying content block: {e}")
            finally:
                cursor.close()

    def delete_content_block(self, content):
        """Delete a content block from the database using content as identifier."""
        block_id = self.get_block_id_by_content(content)
        if block_id and self.connection:
            try:
                cursor = self.connection.cursor()
                query = "DELETE FROM ContentBlock WHERE BlockID = %s"
                cursor.execute(query, (block_id,))
                self.connection.commit()
                print("Content block deleted successfully.")
            except Exception as e:
                print(f"Error deleting content block: {e}")
            finally:
                cursor.close()

    def get_content_blocks_by_section(self, section_id):
        """Fetch all content blocks for a given section ID."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = "SELECT BlockID, BlockType, Content FROM ContentBlock WHERE SectionID = %s AND IsHidden=False"
                cursor.execute(query, (section_id,))
                content_blocks = cursor.fetchall()
                return content_blocks
            except Exception as e:
                print(f"Error fetching content blocks: {e}")
                return []
            finally:
                cursor.close()
        return []
    
    def hide_content_block(self, content):
        """Hide a content block from being displayed using content as identifier."""
        block_id = self.get_block_id_by_content(content)
        if block_id and self.connection:
            try:
                cursor = self.connection.cursor()
                query = "UPDATE ContentBlock SET IsHidden = %s WHERE BlockID = %s"
                cursor.execute(query, (True, block_id))
                self.connection.commit()
                print("Content block hidden successfully.")
            except Exception as e:
                print(f"Error hiding content block: {e}")
            finally:
                cursor.close()

    def show_content_block(self, content):
        """Show a previously hidden content block using content as identifier."""
        block_id = self.get_block_id_by_content(content)
        if block_id and self.connection:
            try:
                cursor = self.connection.cursor()
                query = "UPDATE ContentBlock SET IsHidden = %s WHERE BlockID = %s"
                cursor.execute(query, (False, block_id))
                self.connection.commit()
                print("Content block is now visible.")
            except Exception as e:
                print(f"Error showing content block: {e}")
            finally:
                cursor.close()

from utils.db_connector import DatabaseConnectionManager

class ContentBlockCRUD:
    def __init__(self, connection) -> None:
        if DatabaseConnectionManager.check_if_connected():
            self.connection = connection

    def get_section_details_by_id(self, section_id):
        """Retrieve textbook_id, chapter_id, and section_id based on section_id."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = """
                SELECT textbook_id, chapter_id, section_id
                FROM Sections
                WHERE section_id = %s
                """
                cursor.execute(query, (section_id,))
                result = cursor.fetchone()

                # Read all remaining results to avoid unread result error
                cursor.fetchall()  # Ensure cursor is clear of unread results

                return result if result else None
            except Exception as e:
                print(f"Error fetching section details by ID: {e}")
                return None
            finally:
                cursor.close()
        return None

    def get_block_id_by_content(self, content, section_id, chapter_id, textbook_id):
        """Retrieve the content_block_id based on content, section_id, chapter_id, and textbook_id."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = """
                SELECT content_block_id 
                FROM ContentBlocks 
                WHERE content = %s AND section_id = %s AND chapter_id = %s AND textbook_id = %s
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
            except Exception as e:
                print(f"Error creating content block: {e}")
            finally:
                cursor.close()

    def modify_content_block(self, content_block_id, textbook_id, chapter_id, section_number, new_block_type=None, new_content=None, new_hidden=None):
        """Modify a content block's details using its ID."""
        if self.connection:
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

    def handle_view_block(self, section_id):
        # Fetch the section details using section_id
        section_details = sectioncrud.get_section_details_by_id(section_id)
        if section_details:
            # Extract textbook_id, chapter_id, and section_number from the details
            textbook_id = section_details['textbook_id']
            chapter_id = section_details['chapter_id']
            section_number = section_details['section_number']

            # Fetch content blocks
            content_blocks = contentblockcrud.get_content_blocks_by_section(
                textbook_id=textbook_id,
                chapter_id=chapter_id,
                section_number=section_number
            )

            # Prepare to print the content blocks in a formatted table
            headings = ['BlockID', 'ContentType', 'Content', 'SequenceNumber', 'IsHidden']
            print_list_as_table(headings=headings, rows=content_blocks)
        else:
            print("Invalid section ID.")


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

    def get_content_blocks_by_section(self, textbook_id, chapter_id, section_number, include_hidden=False):
        """Retrieve all content blocks for a given section based on textbook, chapter, and section."""
        if self.connection:
            try:
                cursor = self.connection.cursor(dictionary=True)
                query = """
                SELECT content_block_id, content_type, content, section_number, hidden
                FROM ContentBlocks
                WHERE textbook_id = %s AND chapter_id = %s AND section_number = %s
                """
                if not include_hidden:
                    query += " AND hidden = FALSE"
                cursor.execute(query, (textbook_id, chapter_id, section_number))
                results = cursor.fetchall()
                return results
            except Exception as e:
                print(f"Error fetching content blocks: {e}")
            finally:
                cursor.close()
        return []


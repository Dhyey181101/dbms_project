from application_flow.flow import Flow
from database.user import *
from database.textbook import *
from database.chapter import *
from database.section import *
from database.contentblock import *
from database.course import *
from database.courseta import *
from database.enrollment import EnrollmentCRUD
from utils.db_connector import DatabaseConnectionManager
usercrud = UserCRUD(DatabaseConnectionManager.get_connection())
textbookcrud = TextbookCRUD(DatabaseConnectionManager.get_connection())
chaptercrud = ChapterCRUD(DatabaseConnectionManager.get_connection())
sectioncrud = SectionCRUD(DatabaseConnectionManager.get_connection())
contentblockcrud = ContentBlockCRUD(DatabaseConnectionManager.get_connection())
coursecrud = CourseCRUD(DatabaseConnectionManager.get_connection())
coursetacrud = CourseTACRUD(DatabaseConnectionManager.get_connection())
enrollmentcrud = EnrollmentCRUD(DatabaseConnectionManager.get_connection())

class AdminFlow(Flow):
    def __init__(self,user_id, email) -> None:
        self.operation=-1
        self.logout = False
        super().__init__(user_id, email)



    def print_menu(self):
        while True:
            print("Admin Menu:")
            print("1. Create a Faculty Account")
            print("2. Create E-textbook")
            print("3. Modify E-textbooks")
            print("4. Create New Active Course")
            print("5. Create New Evaluation Course")
            print("6. Logout")
            choice = int(input(""))  
            if choice==1:
                self.handle_create_faculty_account()
            elif choice==2:
                self.handle_create_textbook()
            elif choice==3:
                self.handle_modify_textbook()
            elif choice==4:
                self.handle_new_course()
            elif choice==5:
                self.handle_create_evaluation_course()
            elif choice==6:
                self.handle_logout()
                break
            else:
                print("Bad Choice")
            
        
    def handle_create_faculty_account(self):
        print("Creating a faculty account...")
        first_name = input("Enter FirstName: ")
        last_name = input("Enter LastName: ")
        email = input("Enter Email: ")
        password = input("Enter Password: ")
        role = "faculty"
        usercrud.create_user(first_name, last_name, email, password, role)



    def handle_create_textbook(self):
        print("Creating an e-textbook...")
        title = input("Enter the title of the new E-textbook: ")
        admin_id = self.user_id
        is_hidden = input("Is the textbook hidden? (yes/no): ").strip().lower() == 'yes'

        # Create the textbook through TextbookCRUD
        textbookcrud.create_etextbook(title, admin_id, is_hidden)
        print("E-textbook created successfully.")

        # Retrieve and display the newly created textbook's menu by title
        textbook_id = textbookcrud.get_textbook_id_by_title(title)
        if textbook_id:
            self.textbook_menu(textbook_id)
        else:
            print("Failed to retrieve the new textbook's ID.")


    def textbook_menu(self, textbook_id):
        print("\nE-textbook Menu:")
        print("1. Add New Chapter")
        print("2. Modify Chapter")
        print("3. Go Back to Admin Menu")
        choice = int(input("Enter your choice (1-3): "))

        if choice == 1:
            self.handle_add_new_chapter(textbook_id)
        elif choice == 2:
            self.handle_modify_new_chapter(textbook_id)
        elif choice == 3:
            print("Returning to Admin Menu.")
        else:
            print("Invalid choice. Returning to Admin Menu.")


    def handle_modify_textbook(self):
        print("Modifying an E-textbook...")

        # Display all textbooks
        textbooks = textbookcrud.get_all_textbooks()
        if not textbooks:
            print("No textbooks found.")
            return

        print("Available E-textbooks:")
        for textbook in textbooks:
            print(f"Title: {textbook['Title']}")

        title = input("Enter the title of the E-textbook you want to modify: ")
        textbook_id = textbookcrud.get_textbook_id_by_title(title)
        if textbook_id is None:
            print("Textbook not found.")
            return

        print("1. Add New Chapter")
        print("2. Modify Chapter")
        print("3. Go Back")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            self.handle_add_new_chapter(textbook_id)
        elif choice == 2:
            self.handle_modify_new_chapter(textbook_id)
        elif choice == 3:
            print("Going back to the previous menu...")


    def handle_add_new_chapter(self, textbook_id):
        print("Adding a new chapter...")
        chapter_title = input("Enter Chapter Title: ")
        chapter_name = input("Enter Chapter Name: ")

        # Create the chapter through ChapterCRUD
        chaptercrud.add_chapter(textbook_id, chapter_title, chapter_name)
        print("Chapter added successfully.")

    def handle_modify_new_chapter(self, textbook_id):
        print("Modifying a chapter...")

        # Fetch chapters for the selected textbook
        chapters = chaptercrud.get_all_chapters(textbook_id)
        if not chapters:
            print("No chapters found for this textbook.")
            return

        print("Available Chapters:")
        for chapter in chapters:
            print(f"ID: {chapter['ChapterID']}, Title: {chapter['Title']}, Chapter Name: {chapter['Chaptername']}")

        chapter_id = input("Enter the Chapter ID you want to modify: ")

        # Check if the chapter ID exists
        selected_chapter = next((chapter for chapter in chapters if str(chapter['ChapterID']) == chapter_id), None)
        if not selected_chapter:
            print("Chapter ID not found. Please try again.")
            return

        new_title = input("Enter new Chapter Title (leave blank if no change): ")
        new_chapter_name = input("Enter new Chapter Name (leave blank if no change): ")

        # Update only the fields that have new values
        updated_title = new_title if new_title else selected_chapter['Title']
        updated_chapter_name = new_chapter_name if new_chapter_name else selected_chapter['Chaptername']
        
        # Modify the chapter in the database
        chaptercrud.modify_chapter(chapter_id, updated_title, updated_chapter_name)
        print("Chapter modified successfully.")


    def handle_add_section(self, chapter_id):
        print("Adding a new section...")
        section_number = input("Enter Section Number: ")
        section_title = input("Enter Section Title: ")

        # Add section
        sectioncrud.add_section(chapter_id, section_number, section_title)

        sections = sectioncrud.get_sections_by_chapter(chapter_id)
        section_id = sections[-1]["SectionID"] if sections else None  # Last section ID

        if section_id:
            self.section_menu(section_id)
        else:
            print("Failed to retrieve the section ID.")
        
        print("\nSection Menu:")
        print("1. Add New Content Block")
        print("2. Go Back")
        print("3. Landing Page")
        
        choice = int(input("Enter your choice (1-3): "))
        if choice == 1:
            self.handle_add_content_block(section_id)  # Redirect to content block addition
        elif choice == 2:
            print("Going back to previous page.")
        elif choice == 3:
            print("Returning to User Landing Page.")
        else:
            print("Invalid choice. Returning to previous menu.")

    def handle_modify_section(self):
        print("Modifying a section...")

        textbook_id = input("Enter E-textbook ID: ")
        chapter_id = input("Enter Chapter ID: ")
        section_number = input("Enter Section Number to modify: ")

        # Retrieve the sections to validate input
        sections = sectioncrud.get_sections_by_chapter(chapter_id)
        selected_section = next((section for section in sections if str(section['SectionNumber']) == section_number), None)

        if not selected_section:
            print("Section not found. Returning to menu.")
            return

        section_id = selected_section['SectionID']
        new_section_number = input("Enter new Section Number (leave blank if no change): ")
        new_section_title = input("Enter new Section Title (leave blank if no change): ")

        # Modify section
        sectioncrud.modify_section(section_id, new_section_number or None, new_section_title or None)
        
        print("\nModify Section Menu:")
        print("1. Add New Content Block")
        print("2. Modify Content Block")
        print("3. Go Back")
        print("4. Landing Page")
        
        choice = int(input("Enter your choice (1-4): "))
        if choice == 1:
            self.handle_add_content_block(section_id)  # Redirect to content block addition
        elif choice == 2:
            self.handle_modify_content_block(section_id)  # Redirect to content block modification
        elif choice == 3:
            print("Going back to previous page.")
        elif choice == 4:
            print("Returning to User Landing Page.")
        else:
            print("Invalid choice. Returning to previous menu.")

    def handle_delete_section(self, section_id):
        print("Are you sure you want to delete this section?")
        print("1. Save")
        print("2. Cancel")
        choice = int(input("Enter your choice (1-2): "))
        
        if choice == 1:
            sectioncrud.delete_section(section_id)
            print("Section deleted successfully.")
        elif choice == 2:
            print("Operation cancelled. Returning to previous menu.")
        else:
            print("Invalid choice. Operation cancelled.")

    def handle_add_content_block(self, section_id):
        print("Adding a new content block...")
        block_type = input("Enter Content Block Type: ")
        content = input("Enter Content: ")

        # Add content block
        contentblockcrud.add_content_block(section_id, block_type, content)
        print("Content block added successfully.")

    def handle_modify_content_block(self, section_id):
        print("Modifying a content block...")

        # Fetch content blocks for the selected section
        content_blocks = contentblockcrud.get_content_blocks_by_section(section_id)
        if not content_blocks:
            print("No content blocks found for this section.")
            return

        print("Available Content Blocks:")
        for block in content_blocks:
            print(f"ID: {block['BlockID']}, Type: {block['BlockType']}, Content: {block['Content']}")

        block_id = input("Enter the Content Block ID you want to modify: ")

        # Check if the block ID exists
        selected_block = next((block for block in content_blocks if str(block['BlockID']) == block_id), None)
        if not selected_block:
            print("Content Block ID not found. Please try again.")
            return

        print(f"Current Type: {selected_block['BlockType']}")
        new_block_type = input("Enter new Content Block Type (leave blank if no change): ")

        print(f"Current Content: {selected_block['Content']}")
        new_content = input("Enter new Content (leave blank if no change): ")

        # Update only the fields that have new values
        updated_type = new_block_type if new_block_type else selected_block['BlockType']
        updated_content = new_content if new_content else selected_block['Content']

        # Modify the content block in the database
        contentblockcrud.modify_content_block(block_id, updated_type, updated_content)
        print("Content block modified successfully.")

    def handle_delete_content_block(self, block_id):
        print("Are you sure you want to delete this content block?")
        print("1. Confirm")
        print("2. Cancel")
        choice = int(input("Enter your choice (1-2): "))

        if choice == 1:
            contentblockcrud.delete_content_block(block_id)
            print("Content block deleted successfully.")
        elif choice == 2:
            print("Operation cancelled. Returning to previous menu.")
        else:
            print("Invalid choice. Operation cancelled.")

    def handle_new_course(self):
        print("Creating a new course...")

    def handle_create_evaluation_course(self):
        print("Creating a new evaluation course...")
    
    def handle_logout(self):
        self.logout = True